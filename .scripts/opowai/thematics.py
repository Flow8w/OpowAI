"""Thematic prompt formatting for phase 1.

Produces the human-readable text Claude shows the user when presenting a
thematic, and the "unlock" notification once a tool is connected.
"""

from __future__ import annotations

from typing import Any

from .activation import compute_unlock_diff
from .engine import get_thematics_ordered


def format_thematic_prompt(thematic_id: str, prereqs: dict[str, Any]) -> str:
    """Generate the prompt text for a single thematic.

    Format follows the spec in setup-opowai SKILL.md.
    """
    thematics = {t["id"]: t for t in prereqs.get("thematics", [])}
    thematic = thematics.get(thematic_id)
    if not thematic:
        return f"Thématique inconnue : {thematic_id}"
    order = thematic.get("order", "?")
    total = len(thematics)
    name = thematic.get("name", thematic_id)
    description = thematic.get("description", "")
    why = thematic.get("why_matters", "")

    lines = [
        "─────────────────────────────────────────────────────",
        f"THÉMATIQUE {order}/{total} — {name}",
        "─────────────────────────────────────────────────────",
        "",
        description,
        "",
        why,
        "",
        "Les outils dans cette catégorie :",
    ]
    for tool in thematic.get("tools") or []:
        suffix = " (populaire)" if tool.get("popular") else ""
        note = f" — {tool['note']}" if tool.get("note") else ""
        lines.append(f"  • {tool['name']}{suffix}{note}")
    if thematic.get("free_form"):
        lines.append("  • (connecteur libre — décris ton outil)")
    lines.append("  • Skip — je n'ai pas cet outil")
    lines.append("")
    lines.append("Quel est ton outil principal ?")
    return "\n".join(lines)


def format_unlock_notification(
    tool_id: str,
    prereqs: dict[str, Any],
    before_state: dict[str, Any],
    after_state: dict[str, Any],
) -> str:
    """Generate the 'X connecté. Voici ce que ça débloque' notification text."""
    diff = compute_unlock_diff(before_state, after_state, prereqs)
    skills = prereqs.get("skills") or {}

    # Find tool display name
    tool_label = tool_id
    for thematic in prereqs.get("thematics") or []:
        for tool in thematic.get("tools") or []:
            if tool.get("id") == tool_id:
                tool_label = tool.get("name", tool_id)
                break

    out = [f"✅ {tool_label} connecté.", ""]

    newly_activated = diff["newly_activated"]
    if newly_activated:
        out.append(f"🎉 Ce que ça débloque immédiatement :")
        out.append("")
        out.append(f"  ✅ Skills activés ({len(newly_activated)})")
        for sid in newly_activated:
            spec = skills.get(sid, {})
            msg = spec.get("unlock_message", sid)
            out.append(f"     • /{sid} — {msg}")

    newly_pending = diff["newly_pending"]
    if newly_pending:
        out.append("")
        out.append(f"  ⏳ Skills en attente d'autres outils ({len(newly_pending)})")
        for sid in newly_pending:
            spec = skills.get(sid, {})
            required = spec.get("required") or []
            connected = set((after_state.get("completed_thematics") or {}).keys())
            waiting = [r for r in required if r not in connected]
            out.append(f"     • /{sid} — attend : {', '.join(waiting)}")

    if not newly_activated and not newly_pending:
        out.append("Aucun nouveau skill débloqué pour l'instant.")

    out.append("")
    return "\n".join(out)


def list_thematic_progress(
    state: dict[str, Any], prereqs: dict[str, Any]
) -> list[dict[str, Any]]:
    """Return per-thematic status rows used by checklist/status output."""
    completed = state.get("completed_thematics") or {}
    skipped = set(state.get("skipped_thematics") or [])
    tool_names: dict[str, str] = {}
    for thematic in prereqs.get("thematics") or []:
        for tool in thematic.get("tools") or []:
            tool_names[tool["id"]] = tool.get("name", tool["id"])

    rows = []
    for thematic in get_thematics_ordered(prereqs):
        tid = thematic["id"]
        tool_id = completed.get(tid)
        if tool_id:
            status = "activated"
            tool_label = tool_names.get(tool_id, tool_id)
        elif tid in skipped:
            status = "skipped"
            tool_label = "skipped"
        else:
            status = "todo"
            tool_label = "—"
        rows.append(
            {
                "id": tid,
                "order": thematic.get("order"),
                "name": thematic.get("name", tid),
                "tool_id": tool_id,
                "tool_label": tool_label,
                "status": status,
                "optional": bool(thematic.get("optional")),
            }
        )
    return rows
