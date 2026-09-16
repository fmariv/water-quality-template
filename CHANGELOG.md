# Changelog

All notable changes to this project are documented in this file.

Releases use date-based versions: `YYYY.MM.dd`.

## [2026.09.16]

### Added

- Friendly `GET /` response (`service: "SPAI API"`) instead of a bare 404.
- Pipeline status edge-case hardening: Storage failures on `/pipeline/status` return Idle; banner guards missing `api_url` and keeps polling after Ready/Error.
- UI Docker build uses `yarn.lock` when present.

### Fixed

- Bootstrap robustness: LazyObject Storage/Vars in the API; safe SSR fetches; scripts write `set_error` on early Storage failure.
- Generic pipeline error messages for the UI banner.

### Changed

- Ready status banner only appears on a live Building→Ready transition (not on every dashboard visit).
- UI Docker images overwrite `.env` with `VITE_ENV=PRO` only (no MapTiler keys baked into images).
- API error responses no longer leak internal exception strings (generic 503/400/404 messages).

### Fixed

- SSR bootstrap: landslide + EWS use safe fetches; renewable no longer treats `GET /` as images.
- Banner does not escalate to Unreachable after a successful Ready status (transient API blips).

## [2026.09.15]

### Added

- Docker images pinned via `image: …/:latest` in `spai.config.yaml` (Artifact Registry).
- End-to-end pipeline status wiring: script registry → storage → `GET /pipeline/status` → UI banner.
- UI Dockerfiles switched to yarn; `.env` with `VITE_ENV=PRO` copied into the image for HTTPS API URLs.
