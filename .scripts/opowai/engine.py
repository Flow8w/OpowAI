"""Core engine: computes the state of skills and thematic progression.

The engine is **read-only** — it never mutates state. Mutations are caller
responsibility (typically via :mod:`activation` or :mod:`cli`).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .state import REPO_ROOT

DEFAULT_PREREQS_PATH = REPO_ROOT / "System" / "skill-prerequisites.yaml"

# Skill states
ACTIVATED = "activated"
PENDING = "pending"
TODO = "todo"
DORMANT = "dormant"

VALID_STATES = (ACTIVATED, PENDING, TODO, DORMANT)


def load_prerequisites(path: Path | str | None = None) -> dict[str, Any]:
    """Parse ``skill-prerequisites.yaml`` into a plain dict.

    Raises :class:`FileNotFoundError` if the file is missing.
    """
    prereqs_path = Path(path) if path else DEFAULT_PREREQS_PATH
    with prereqs_path.open("r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def _selected_skill_ids(state: dict[str, Any], prereqs: dict[str, Any]) -> set[str]:
    """Compute the union of skills covered by the user's selected use cases.

    If no use case is selected (early phase 0), all skills are considered
    selected — we don't want everything to look dormant before phase 0
    completes.
    """
    use_cases = {uc["id"]: uc for uc in prereqs.get("use_cases", [])}
    selected = state.get("selected_use_cases") or []
    if not selected:
        return set(prereqs.get("skills", {}).keys())
    out: set[str] = set()
    for uc_id in selected:
        uc = use_cases.get(uc_id)
        if uc:
            out.update(uc.get("skills", []))
    return out


def _connected_thematics(state: dict[str, Any]) -> set[str]:
    """Set of thematic ids that have at least one connected tool."""
    completed = state.get("completed_thematics") or {}
    return {tid for tid, tool in completed.items() if tool}


def compute_skill_states(
    state: dict[str, Any], prereqs: dict[str, Any]
) -> dict[str, str]:
    """Return ``{skill_id: state}`` where ``state`` is one of :data:`VALID_STATES`.

    Rules:
        - If the skill is not in the user's selected use cases → ``dormant``
        - If all required thematics are connected → ``activated``
        - If at least one required thematic is connected (but not all) → ``pending``
        - If no required thematic is connected → ``todo``
        - Skills with no required thematic and selected → ``activated``
    """
    skills = prereqs.get("skills", {})
    connected = _connected_thematics(state)
    selected = _selected_skill_ids(state, prereqs)

    out: dict[str, str] = {}
    for skill_id, spec in skills.items():
        if skill_id not in selected:
            out[skill_id] = DORMANT
            continue
        required = spec.get("required") or []
        if not required:
            out[skill_id] = ACTIVATED
            continue
        have = [t for t in required if t in connected]
        if len(have) == len(required):
            out[skill_id] = ACTIVATED
        elif have:
            out[skill_id] = PENDING
        else:
            out[skill_id] = TODO
    return out


def get_unlocked_by_tool(
    tool_id: str, prereqs: dict[str, Any], state: dict[str, Any]
) -> list[str]:
    """List skills whose ``required`` set includes ``tool_id`` and are now activated.

    Useful for the "what does this connection unlock?" notification. The caller
    is expected to pass a *post-connection* state.
    """
    skill_states = compute_skill_states(state, prereqs)
    skills = prereqs.get("skills", {})
    out = []
    for skill_id, spec in skills.items():
        if tool_id in (spec.get("required") or []) and skill_states[skill_id] == ACTIVATED:
            out.append(skill_id)
    return out


def get_thematics_ordered(prereqs: dict[str, Any]) -> list[dict[str, Any]]:
    """Return thematics sorted by their ``order`` field."""
    return sorted(prereqs.get("thematics", []), key=lambda t: t.get("order", 999))


def get_next_thematic(
    state: dict[str, Any], prereqs: dict[str, Any]
) -> dict[str, Any] | None:
    """Return the next thematic to address, or ``None`` if all are handled.

    A thematic is "handled" if it appears in ``completed_thematics`` or
    ``skipped_thematics``.
    """
    completed = set((state.get("completed_thematics") or {}).keys())
    skipped = set(state.get("skipped_thematics") or [])
    handled = completed | skipped
    for thematic in get_thematics_ordered(prereqs):
        if thematic["id"] not in handled:
            return thematic
    return None


def summary(state: dict[str, Any], prereqs: dict[str, Any]) -> dict[str, Any]:
    """High-level numbers for dashboards.

    Returns a dict with counts, percentages, and the current phase label.
    """
    thematics = prereqs.get("thematics", [])
    skill_states = compute_skill_states(state, prereqs)

    total_thematics = len(thematics)
    connected_count = len(_connected_thematics(state))

    by_state: dict[str, list[str]] = {s: [] for s in VALID_STATES}
    for skill_id, s in skill_states.items():
        by_state[s].append(skill_id)

    total_skills = len(skill_states)
    activated_count = len(by_state[ACTIVATED])

    # Phase progress: 5 phases total (0..5), driven by current_phase string
    try:
        phase_num = int(state.get("current_phase", "0"))
    except (TypeError, ValueError):
        phase_num = 0
    phase_pct = int(round(min(phase_num, 5) / 5 * 100))

    return {
        "phase": phase_num,
        "phase_pct": phase_pct,
        "thematics_total": total_thematics,
        "thematics_connected": connected_count,
        "skills_total": total_skills,
        "skills_activated": activated_count,
        "skills_pending": len(by_state[PENDING]),
        "skills_todo": len(by_state[TODO]),
        "skills_dormant": len(by_state[DORMANT]),
        "by_state": by_state,
        "selected_use_cases": state.get("selected_use_cases") or [],
    }
