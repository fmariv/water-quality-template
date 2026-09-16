"""
Portable pipeline status registry for SPAI templates.

Copy this file into each template as:
  scripts/<script-name>/src/status_registry.py

Writes a JSON **records** list (one object) so ``storage.read`` / ``pd.read_json``
return a one-row DataFrame — never pandas column-orient on disk:
  [{"status": "Building", "message": "...", "updated_at": "..."}]

Error messages shown to the UI are always generic — keep technical detail in logs only.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

STATUS_PATH = "pipeline_status.json"
MAX_MESSAGE_LEN = 240

IDLE = "Idle"
BUILDING = "Building"
WARNING = "Warning"
ERROR = "Error"
READY = "Ready"

GENERIC_ERROR_MESSAGE = (
    "Error downloading data. Check the logs or contact support."
)
GENERIC_ERROR_TITLE = "Error downloading data"
GENERIC_ERROR_DETAIL = "Check the logs or contact support."

_IDLE = {
    "status": IDLE,
    "message": "No pipeline run yet",
    "updated_at": None,
}


def _clip(message: str) -> str:
    text = " ".join((message or "").split())
    if len(text) > MAX_MESSAGE_LEN:
        return text[: MAX_MESSAGE_LEN - 1].rstrip() + "…"
    return text


def _public_message(status: str, message: str) -> str:
    if status == ERROR:
        return GENERIC_ERROR_MESSAGE
    return _clip(message)


def _unwrap_value(value: Any) -> Any:
    """Flatten pandas column-orient leftovers like ``{"0": "Error"}`` → ``"Error"``."""
    if value is None:
        return None
    if isinstance(value, dict):
        if "0" in value:
            return _unwrap_value(value["0"])
        if len(value) == 1:
            return _unwrap_value(next(iter(value.values())))
        return value
    if isinstance(value, (list, tuple)) and len(value) == 1:
        return _unwrap_value(value[0])
    # pandas / numpy scalars
    try:
        import pandas as pd

        if pd.isna(value):
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


def _normalize_status_payload(raw: Any) -> dict:
    """Accept DataFrame, records list, column-orient dict, or flat dict → flat str dict."""
    if raw is None:
        return dict(_IDLE)

    # DataFrame (from storage.read / pd.read_json)
    if hasattr(raw, "iloc") and hasattr(raw, "empty"):
        if bool(raw.empty):
            return dict(_IDLE)
        raw = raw.iloc[0].to_dict()

    if isinstance(raw, list):
        if not raw:
            return dict(_IDLE)
        raw = raw[0]

    if not isinstance(raw, dict):
        return dict(_IDLE)

    # Column-orient whole payload: {"status":{"0":"Error"}, "message":{"0":"..."}}
    sample = next(iter(raw.values()), None)
    if (
        all(isinstance(v, dict) for v in raw.values() if v is not None)
        and isinstance(sample, dict)
        and ("0" in sample or len(sample) == 1)
    ):
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


def set_status(
    storage: Any,
    status: str,
    message: str = "",
    *,
    path: Optional[str] = None,
) -> None:
    """
    Overwrite current pipeline status in storage.

    Writes a JSON **records** list ``[{...}]`` (not pandas column-orient) so
    ``storage.read`` / the API always see a normal one-row table.
    For ``ERROR``, ``message`` is ignored and ``GENERIC_ERROR_MESSAGE`` is stored.
    """
    status_path = path or STATUS_PATH
    payload = {
        "status": status,
        "message": _public_message(status, message),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        if storage.exists(status_path):
            storage.delete(status_path)
        # records list → one-row DataFrame on read; avoids {"status":{"0":...}} on disk
        storage.create(json.dumps([payload], ensure_ascii=False), status_path)
        logger.info("Pipeline status: %s — %s", payload["status"], payload["message"])
    except Exception as exc:
        logger.warning("Failed to write pipeline status: %s", exc)


def set_error(storage: Any, *, path: Optional[str] = None) -> None:
    """Mark pipeline as Error with the generic user-facing message."""
    set_status(storage, ERROR, path=path)


def get_status(storage: Any, *, path: Optional[str] = None) -> dict:
    """Read current pipeline status from storage (always returns a flat str dict)."""
    status_path = path or STATUS_PATH
    try:
        if not storage.exists(status_path):
            return dict(_IDLE)
        raw = storage.read(status_path)
        return _normalize_status_payload(raw)
    except Exception as exc:
        logger.warning("Failed to read pipeline status: %s", exc)
        return dict(_IDLE)
