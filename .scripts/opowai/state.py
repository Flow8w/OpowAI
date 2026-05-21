"""Persistence layer for OpowAI setup state.

The state lives in ``System/.setup-state.json`` (gitignored). It is the single
source of truth for "where is the user in the setup". The schema is documented
in the package README.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Repo root resolution — this file is at
# <repo>/.scripts/opowai/state.py, so repo root is two parents up from the
# containing package.
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATE_PATH = REPO_ROOT / "System" / ".setup-state.json"


def _utcnow() -> str:
    """Return current UTC time as an ISO8601 string (Z-suffixed)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def empty_state() -> dict[str, Any]:
    """Return a fresh state with all fields initialized."""
    now = _utcnow()
    return {
        "current_phase": "0",
        "current_thematic": None,
        "completed_thematics": {},  # {thematic_id: tool_id}
        "skipped_thematics": [],
        "selected_use_cases": [],
        "auto_discovery_status": "not_started",
        "activated_skills": [],
        "user_profile": {},
        "company_profile": {},
        "started_at": now,
        "last_update": now,
    }


def load_state(path: Path | str | None = None) -> dict[str, Any]:
    """Load state from disk; return a fresh empty state if the file is absent.

    Missing or unknown fields are filled in from :func:`empty_state` so that
    upgrades remain backward-compatible.
    """
    state_path = Path(path) if path else DEFAULT_STATE_PATH
    if not state_path.exists():
        return empty_state()
    with state_path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    base = empty_state()
    base.update(data)
    return base


def save_state(state: dict[str, Any], path: Path | str | None = None) -> Path:
    """Persist state to disk, refreshing ``last_update``. Returns the file path."""
    state_path = Path(path) if path else DEFAULT_STATE_PATH
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state = dict(state)
    state["last_update"] = _utcnow()
    tmp = state_path.with_suffix(state_path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fp:
        json.dump(state, fp, indent=2, ensure_ascii=False)
        fp.write("\n")
    os.replace(tmp, state_path)
    return state_path
