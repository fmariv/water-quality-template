"""
Portable FastAPI helpers for pipeline status.

Copy into each template as ``apis/<name>/src/pipeline_status.py``.

Never raise HTTP 500 from the status poller — the UI must keep working.
Always return a **flat** JSON-safe dict:
  {"status": "Error", "message": "...", "updated_at": "..."}
Never return pandas column-orient: {"status": {"0": "Error"}, ...}.
"""

from __future__ import annotations

from typing import Any, Optional

import pandas as pd

DEFAULT_STATUS_PATH = "pipeline_status.json"

_IDLE = {
    "status": "Idle",
    "message": "No pipeline run yet",
    "updated_at": None,
}


def _unwrap_value(value: Any) -> Any:
    """Flatten pandas column-orient leftovers like ``{"0": "Error"}`` → ``"Error"``."""
    if value is None:
        return None
    if isinstance(value, dict):
        if "0" in value:
            return _unwrap_value(value["0"])
        if 0 in value:
            return _unwrap_value(value[0])
        if len(value) == 1:
            return _unwrap_value(next(iter(value.values())))
        return value
    if isinstance(value, (list, tuple)) and len(value) == 1:
        return _unwrap_value(value[0])
    try:
        if not isinstance(value, (str, bytes, dict, list)) and pd.isna(value):
            return None
    except Exception:
        pass
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    return value


def _looks_column_orient(raw: dict) -> bool:
    """True for payloads like {"status": {"0": "Error"}, "message": {"0": "..."}}."""
    if not raw:
        return False
    nested = [v for v in raw.values() if isinstance(v, dict)]
    if len(nested) < 1:
        return False
    return all(
        ("0" in v or 0 in v or len(v) == 1) for v in nested
    )


def normalize_status_payload(raw: Any) -> dict:
    """Accept DataFrame, records list, column-orient dict, or flat dict → flat str dict."""
    if raw is None:
        return dict(_IDLE)

    if isinstance(raw, pd.DataFrame):
        if raw.empty:
            return dict(_IDLE)
        raw = raw.iloc[0].to_dict()

    if isinstance(raw, pd.Series):
        raw = raw.to_dict()

    if isinstance(raw, list):
        if not raw:
            return dict(_IDLE)
        raw = raw[0]

    if not isinstance(raw, dict):
        return dict(_IDLE)

    if _looks_column_orient(raw):
        raw = {k: _unwrap_value(v) for k, v in raw.items()}

    status = _unwrap_value(raw.get("status"))
    message = _unwrap_value(raw.get("message"))
    updated_at = _unwrap_value(raw.get("updated_at"))

    if status is None or status == "":
        return dict(_IDLE)

    return {
        "status": str(status).strip(),
        "message": None if message is None else str(message),
        "updated_at": None if updated_at is None else str(updated_at),
    }


def read_pipeline_status(
    storage: Any,
    path: str = DEFAULT_STATUS_PATH,
) -> dict:
    """Read ``pipeline_status.json`` from storage as a flat JSON-serializable dict.

    Never raises — Storage/LazyObject failures return Idle so the UI poller stays healthy.
    """
    try:
        if not storage.exists(path):
            return dict(_IDLE)
        raw = storage.read(path)
        return normalize_status_payload(raw)
    except Exception:
        return dict(_IDLE)


def data_available_payload(pipeline: Optional[dict] = None) -> dict:
    """Build the standard ``/data_available`` response from a status dict."""
    pipeline = pipeline or dict(_IDLE)
    ready = pipeline.get("status") == "Ready"
    return {
        "status": "healthy",
        "data_available": ready,
        "data_status": "ready" if ready else "no_data",
        "pipeline_status": pipeline.get("status"),
        "message": pipeline.get("message"),
    }
