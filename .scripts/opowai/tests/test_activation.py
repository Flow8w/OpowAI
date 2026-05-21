"""Tests for the activation module."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
PKG_PARENT = TESTS_DIR.parents[1]
if str(PKG_PARENT) not in sys.path:
    sys.path.insert(0, str(PKG_PARENT))

from opowai import activation, engine  # noqa: E402

FIXTURE = TESTS_DIR / "fixtures" / "sample_state.json"


def test_compute_unlock_diff_adds_transcript():
    """Connecting transcript should activate coach-team-member (was pending)."""
    prereqs = engine.load_prerequisites()
    before = json.loads(FIXTURE.read_text())
    after = copy.deepcopy(before)
    after["completed_thematics"]["transcript"] = "granola"

    diff = activation.compute_unlock_diff(before, after, prereqs)
    assert "coach-team-member" in diff["newly_activated"]


def test_compute_unlock_diff_empty_when_unchanged():
    prereqs = engine.load_prerequisites()
    state = json.loads(FIXTURE.read_text())
    diff = activation.compute_unlock_diff(state, state, prereqs)
    assert diff["newly_activated"] == []
    assert diff["newly_pending"] == []


def test_activate_skill_is_idempotent(tmp_path):
    prereqs = engine.load_prerequisites()
    state = {"activated_skills": []}
    skills_dir = tmp_path / "skills"
    activation.activate_skill("daily-plan", state, prereqs, skills_dir=skills_dir)
    activation.activate_skill("daily-plan", state, prereqs, skills_dir=skills_dir)
    assert state["activated_skills"] == ["daily-plan"]
    assert (skills_dir / "daily-plan" / "SKILL.md").exists()
