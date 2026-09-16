# Changelog

All notable changes to this project are documented in this file.

Releases use date-based versions: `YYYY.MM.dd`.

## [2026.09.16]

### Added

- Friendly `GET /` response (`service: "SPAI API"`, name: `water-quality`).
- Pipeline status hardening: `/pipeline/status` never raises; banner guards missing `api_url` and keeps polling after Ready/Error (cron-friendly).
- UI Docker build uses `yarn.lock` when present (`--frozen-lockfile` with install fallback).
- `.env.example` with `VITE_ENV=PRO` only (no secrets).

### Changed

- Ready banner only appears on a live transition (e.g. Building → Ready), not on every dashboard visit or poll.
- After Ready, transient API blips no longer escalate to Unreachable.
- UI Docker images overwrite `.env` with `VITE_ENV=PRO` only (no MapTiler/API keys baked into images).
- API error responses use generic messages (no `detail=str(e)` leaks); data endpoints return 503 when Storage/vars fail.

### Fixed

- Bootstrap robustness: LazyObject Storage/Vars in the API; safe SSR where applicable; scripts write `set_error` even if Storage fails early.
- Generic pipeline error messages for the UI banner (technical detail stays in logs).
- SSR bootstrap uses `safeFetch` for images/analytics/aoi.
- Removed the red “No images or layers have been found” banner while the pipeline is still preparing data; Analytics sidebar stays visible and layout no longer clips the right panel (`w-screen` → flex).
- Water analytics pie/layers only render when dates and series are available (no broken requests during empty bootstrap).
- UI Docker image rebuilt for `linux/amd64` (cloud-compatible) and published as `…-ui:latest`.

## [2026.09.15]

### Added

- Docker images pinned via `image: …/:latest` in `spai.config.yaml` (Artifact Registry).
- End-to-end pipeline status wiring: script registry → storage → `GET /pipeline/status` → UI banner.
- UI Dockerfiles switched to yarn; `VITE_ENV=PRO` for HTTPS API URLs in cloud.
