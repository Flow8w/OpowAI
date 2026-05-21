"""Tests for the engine module."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Make the .scripts/ directory importable so `import opowai` works.
TESTS_DIR = Path(__file__).resolve().parent
PKG_PARENT = TESTS_DIR.parents[1]
if str(PKG_PARENT) not in sys.path:
    sys.path.insert(0, str(PKG_PARENT))

from opowai import engine  # noqa: E402

FIXTURE = TESTS_DIR / "fixtures" / "sample_state.json"


def _load_fixture() -> dict:
    return json.loads(FIXTURE.read_text())


def test_compute_skill_states():
    state = _load_fixture()
    prereqs = engine.load_prerequisites()
    states = engine.compute_skill_states(state, prereqs)

    # Sanity: every skill in the yaml gets a status
    assert set(states.keys()) == set(prereqs["skills"].keys())
    assert all(v in engine.VALID_STATES for v in states.values())

    # daily-plan requires calendar (connected) → activated
    assert states["daily-plan"] == engine.ACTIVATED

    # friday-close requires crm + calendar (both connected) → activated
    assert states["friday-close"] == engine.ACTIVATED

    # all-hands requires docs (not connected) AND is NOT in selected use cases → dormant
    assert states["all-hands"] == engine.DORMANT

    # coach-team-member is selected (coaching-sales) but transcript not connected → pending
    assert states["coach-team-member"] == engine.PENDING


def test_thematic_progression():
    state = _load_fixture()
    prereqs = engine.load_prerequisites()

    ordered = engine.get_thematics_ordered(prereqs)
    assert [t["id"] for t in ordered[:3]] == ["crm", "email", "calendar"]

    # The next thematic should be docs (order 4) since crm/email/calendar are completed
    nxt = engine.get_next_thematic(state, prereqs)
    assert nxt is not None
    assert nxt["id"] == "docs"


def test_summary_counts():
    state = _load_fixture()
    prereqs = engine.load_prerequisites()
    summ = engine.summary(state, prereqs)

    assert summ["thematics_connected"] == 3
    assert summ["thematics_total"] == 10
    assert summ["skills_total"] == len(prereqs["skills"])
    # at least daily-plan activated
    assert summ["skills_activated"] >= 1
