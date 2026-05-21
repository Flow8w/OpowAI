"""ASCII dashboard rendered by ``bin/opowai status``."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .cron import list_next_runs
from .engine import (
    ACTIVATED,
    DORMANT,
    PENDING,
    TODO,
    compute_skill_states,
    summary,
)
from .thematics import list_thematic_progress

BAR_WIDTH = 20
SEP = "━" * 60


def _bar(pct: int) -> str:
    filled = int(round(pct / 100 * BAR_WIDTH))
    return "▓" * filled + "░" * (BAR_WIDTH - filled)


def _symbol(state_str: str) -> str:
    return {
        ACTIVATED: "✅",
        PENDING: "⏳",
        TODO: "🔘",
        DORMANT: "🔒",
        "skipped": "⏭",
    }.get(state_str, "?")


def generate_status_report(state: dict[str, Any], prereqs: dict[str, Any]) -> str:
    """Return the full status report as a string ready for stdout."""
    summ = summary(state, prereqs)
    skill_states = compute_skill_states(state, prereqs)
    skills_spec = prereqs.get("skills") or {}
    use_cases_map = {uc["id"]: uc["name"] for uc in prereqs.get("use_cases") or []}

    selected = summ["selected_use_cases"]
    uc_label = (
        ", ".join(use_cases_map.get(u, u) for u in selected) if selected else "_aucun_"
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = [f"📊 OpowAI Status — {now}", ""]

    out += [
        SEP,
        "SETUP",
        SEP,
        "",
        f"  Avancement   {_bar(summ['phase_pct'])} {summ['phase_pct']}%",
        f"  Phase        Phase {summ['phase']} / 5",
        f"  Cas d'usage  {len(selected)} sélectionnés : {uc_label}",
        "",
    ]

    # Thematics
    out += [
        SEP,
        f"THÉMATIQUES ({summ['thematics_connected']} / {summ['thematics_total']})",
        SEP,
        "",
    ]
    for row in list_thematic_progress(state, prereqs):
        sym = _symbol(row["status"]) if row["status"] != "activated" else "✅"
        opt = " (optionnel)" if row["optional"] else ""
        out.append(f"  {sym} {row['order']}. {row['name']}{opt} → {row['tool_label']}")
    out.append("")

    # Skills grouped by category
    out += [
        SEP,
        f"SKILLS ({summ['skills_activated']} activés / {summ['skills_total']} total)",
        SEP,
        "",
    ]

    activated_ids = [sid for sid, s in skill_states.items() if s == ACTIVATED]
    pending_ids = [sid for sid, s in skill_states.items() if s == PENDING]
    todo_ids = [sid for sid, s in skill_states.items() if s == TODO]
    dormant_ids = [sid for sid, s in skill_states.items() if s == DORMANT]

    # Group activated by category
    by_cat: dict[str, list[str]] = {}
    for sid in activated_ids:
        cat = (skills_spec.get(sid) or {}).get("category", "Autres")
        by_cat.setdefault(cat, []).append(sid)
    for cat in sorted(by_cat.keys()):
        out.append(f"  {cat}")
        for sid in sorted(by_cat[cat]):
            spec = skills_spec.get(sid) or {}
            sched = spec.get("schedule")
            sched_str = f"        📅 {sched}" if sched else ""
            out.append(f"    ✅ /{sid}{sched_str}")
        out.append("")

    if pending_ids:
        out.append(f"  En attente d'autres outils ({len(pending_ids)})")
        connected = set((state.get("completed_thematics") or {}).keys())
        for sid in sorted(pending_ids):
            spec = skills_spec.get(sid) or {}
            waiting = [r for r in (spec.get("required") or []) if r not in connected]
            out.append(f"    ⏳ /{sid} → attend {', '.join(waiting)}")
        out.append("")

    if todo_ids:
        out.append(f"  Aucun prérequis connecté ({len(todo_ids)})")
        for sid in sorted(todo_ids):
            spec = skills_spec.get(sid) or {}
            required = ", ".join(spec.get("required") or []) or "—"
            out.append(f"    🔘 /{sid} → requis : {required}")
        out.append("")

    if dormant_ids:
        out.append(f"  Dormants — non sélectionnés en phase 0 ({len(dormant_ids)})")
        out.append("    🔒 " + ", ".join(f"/{sid}" for sid in sorted(dormant_ids)))
        out.append("")

    # Next runs
    next_runs = list_next_runs(activated_ids, prereqs)
    if next_runs:
        out += [SEP, "PROCHAINES EXÉCUTIONS", SEP, ""]
        for run in next_runs:
            out.append(f"  {run['schedule']:<28} /{run['skill']}")
        out.append("")

    # Suggestions
    suggestions = _generate_suggestions(state, prereqs, skill_states)
    if suggestions:
        out += [SEP, "SUGGESTIONS", SEP, ""]
        out.extend(f"  {s}" for s in suggestions)
        out.append("")

    out.append(SEP)
    return "\n".join(out)


def _generate_suggestions(
    state: dict[str, Any],
    prereqs: dict[str, Any],
    skill_states: dict[str, str],
) -> list[str]:
    """Heuristic suggestions: missing tools that would unlock pending skills."""
    suggestions: list[str] = []
    connected = set((state.get("completed_thematics") or {}).keys())

    # For each pending skill, list missing required thematic
    missing_count: dict[str, list[str]] = {}
    for sid, s in skill_states.items():
        if s != PENDING:
            continue
        spec = (prereqs.get("skills") or {}).get(sid) or {}
        for req in spec.get("required") or []:
            if req not in connected:
                missing_count.setdefault(req, []).append(sid)

    # Sort by # of skills unlocked desc
    ranked = sorted(missing_count.items(), key=lambda kv: -len(kv[1]))[:3]
    for thematic_id, skills in ranked:
        suggestions.append(
            f"💡 Connecter [{thematic_id}] débloquerait {len(skills)} skill(s) : "
            f"{', '.join('/' + s for s in skills)}"
        )

    # Detect should-be-activated bugs (no required missing but still pending — shouldn't happen)
    for sid, s in skill_states.items():
        if s != PENDING:
            continue
        spec = (prereqs.get("skills") or {}).get(sid) or {}
        required = spec.get("required") or []
        if required and all(r in connected for r in required):
            suggestions.append(
                f"⚠️  /{sid} devrait être activé (tous les prérequis sont connectés)"
            )

    return suggestions
