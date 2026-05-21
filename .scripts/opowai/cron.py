"""Cron file generation for scheduled OpowAI agents.

Maps the human-friendly ``schedule`` strings in ``skill-prerequisites.yaml``
(e.g. ``Mon-Fri 08:00``, ``Last Fri of month 14:00``) to standard cron lines.

For schedules that crontab cannot express precisely (e.g. "last Friday of
month"), we emit an over-approximation (``22-28``) and rely on the invoked
script to bail out if today is not the right date.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from .state import REPO_ROOT

DEFAULT_CRON_PATH = REPO_ROOT / ".scripts" / "cron" / "opowai.cron"

DAY_MAP = {
    "Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6,
}


def parse_schedule(schedule: str) -> list[str]:
    """Convert a human-friendly schedule into one or more cron lines.

    Returns a list because a single schedule can produce multiple lines
    (e.g. ``Mon-Fri 09:00, 14:00`` → two cron entries).

    Unrecognized schedules return an empty list — callers are expected to
    fall back to a comment in the cron file.
    """
    if not schedule:
        return []
    schedule = schedule.strip()

    # Extract all HH:MM occurrences
    times = re.findall(r"(\d{1,2}):(\d{2})", schedule)
    if not times:
        return []

    lines: list[str] = []
    lower = schedule.lower()

    # Day-of-week parsing
    def emit(dom: str, month: str, dow: str) -> None:
        for hh, mm in times:
            lines.append(f"{int(mm)} {int(hh)} {dom} {month} {dow}")

    if "last fri" in lower and "of month" in lower:
        # Last Friday of month: day-of-month 22-28 AND DOW=Fri
        # crontab AND semantics differ across implementations; on macOS,
        # the OR-of-DOM-DOW means we restrict to DOM and let the runner check DOW.
        emit("22-28", "*", "5")
        return lines

    # Range Mon-Fri or single day or comma list
    range_match = re.search(r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)-(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b", schedule)
    single_days = re.findall(r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b", schedule)

    if range_match:
        start = DAY_MAP[range_match.group(1)]
        end = DAY_MAP[range_match.group(2)]
        emit("*", "*", f"{start}-{end}")
        return lines

    if single_days:
        dow = ",".join(str(DAY_MAP[d]) for d in single_days)
        emit("*", "*", dow)
        return lines

    # Default: daily
    emit("*", "*", "*")
    return lines


def write_cron_file(
    activated_skills: list[str],
    prereqs: dict[str, Any],
    path: Path | str | None = None,
) -> Path:
    """Write the OpowAI cron file from activated skills with schedules.

    The generated file is *not* installed in the user's crontab; install it
    explicitly with :func:`install_cron`.
    """
    target = Path(path) if path else DEFAULT_CRON_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    skills_spec = prereqs.get("skills") or {}
    lines = [
        "# OpowAI scheduled agents — generated, do not edit by hand",
        "# To install: crontab .scripts/cron/opowai.cron",
        "",
    ]
    bin_path = REPO_ROOT / "bin" / "opowai"
    for sid in sorted(activated_skills):
        spec = skills_spec.get(sid) or {}
        schedule = spec.get("schedule")
        if not schedule:
            continue
        cron_entries = parse_schedule(schedule)
        lines.append(f"# /{sid} — {schedule}")
        if not cron_entries:
            lines.append(f"# (unparsed schedule '{schedule}' — manual entry needed)")
            continue
        for entry in cron_entries:
            lines.append(f"{entry} {bin_path} run-skill {sid}")
        lines.append("")

    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def install_cron(cron_file: Path | str | None = None) -> str:
    """Return the shell command that would install the cron file.

    The function never installs silently — installation is the user's
    explicit decision. Use the returned string as a confirmation prompt.
    """
    path = Path(cron_file) if cron_file else DEFAULT_CRON_PATH
    return f"crontab {path}"


def list_next_runs(activated_skills: list[str], prereqs: dict[str, Any]) -> list[dict[str, Any]]:
    """Return scheduled skills with their raw schedule string (for /status).

    Computing exact next-run timestamps would require a cron lib; the v0.1
    surface just shows the human schedule, sorted alphabetically.
    """
    skills_spec = prereqs.get("skills") or {}
    out = []
    for sid in activated_skills:
        spec = skills_spec.get(sid) or {}
        sched = spec.get("schedule")
        if sched:
            out.append({"skill": sid, "schedule": sched})
    return sorted(out, key=lambda r: r["schedule"])
