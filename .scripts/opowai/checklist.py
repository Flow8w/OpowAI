"""Generation of ``System/setup-checklist.md``.

The checklist is regenerated fully each time — never patched. This keeps the
function pure and idempotent (``write_checklist`` called twice in a row
produces the same byte content modulo timestamps).
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .engine import (
    ACTIVATED,
    DORMANT,
    PENDING,
    TODO,
    compute_skill_states,
    summary,
)
from .state import REPO_ROOT
from .thematics import list_thematic_progress

DEFAULT_CHECKLIST_PATH = REPO_ROOT / "System" / "setup-checklist.md"

SYMBOLS = {
    ACTIVATED: "✅",
    PENDING: "⏳",
    TODO: "🔘",
    DORMANT: "🔒",
    "skipped": "⏭",
}


def _progress_bar(pct: int, width: int = 20) -> str:
    filled = int(round(pct / 100 * width))
    return "[" + "▓" * filled + "░" * (width - filled) + f"] {pct}%"


def _phase_symbol(phase_num: int, target_phase: int) -> str:
    if phase_num > target_phase:
        return "✅"
    if phase_num == target_phase:
        return "🔵"
    return "🔘"


def generate_checklist(state: dict[str, Any], prereqs: dict[str, Any]) -> str:
    """Produce the markdown content of ``setup-checklist.md``."""
    summ = summary(state, prereqs)
    phase = summ["phase"]
    skill_states = compute_skill_states(state, prereqs)
    skills_spec = prereqs.get("skills") or {}

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    selected = summ["selected_use_cases"]
    use_cases_map = {uc["id"]: uc["name"] for uc in prereqs.get("use_cases", [])}
    selected_labels = (
        "\n".join(f"- {use_cases_map.get(u, u)}" for u in selected)
        if selected
        else "_à venir_"
    )

    # Thematics table
    rows = list_thematic_progress(state, prereqs)
    table_lines = [
        "| # | Thématique | Outil principal | Statut |",
        "|---|-----------|-----------------|--------|",
    ]
    for row in rows:
        if row["status"] == "activated":
            status_str = "✅ activated"
        elif row["status"] == "skipped":
            status_str = "⏭ skipped"
        else:
            status_str = "🔘 todo"
        name = row["name"] + (" *(optionnel)*" if row["optional"] else "")
        table_lines.append(
            f"| {row['order']} | {name} | {row['tool_label']} | {status_str} |"
        )

    # Skills sections
    by_state: dict[str, list[str]] = {ACTIVATED: [], PENDING: [], DORMANT: [], TODO: []}
    for sid, s in skill_states.items():
        by_state[s].append(sid)

    def render_skill_list(ids: list[str]) -> str:
        if not ids:
            return "_Aucun pour l'instant._"
        lines = []
        for sid in sorted(ids):
            spec = skills_spec.get(sid, {})
            schedule = spec.get("schedule")
            suffix = f" — 📅 {schedule}" if schedule else ""
            unlock = spec.get("unlock_message", "")
            lines.append(f"- ✅ `/{sid}`{suffix} — {unlock}")
        return "\n".join(lines)

    def render_pending_list(ids: list[str]) -> str:
        if not ids:
            return "_Aucun pour l'instant._"
        connected = set((state.get("completed_thematics") or {}).keys())
        lines = []
        for sid in sorted(ids):
            spec = skills_spec.get(sid, {})
            required = spec.get("required") or []
            waiting = [r for r in required if r not in connected]
            lines.append(f"- ⏳ `/{sid}` — attend : {', '.join(waiting) or '—'}")
        return "\n".join(lines)

    def render_dormant_list(ids: list[str]) -> str:
        if not ids:
            return "_Aucun._"
        return ", ".join(f"`/{sid}`" for sid in sorted(ids))

    # Scheduled agents
    scheduled = [
        sid
        for sid in by_state[ACTIVATED]
        if (skills_spec.get(sid) or {}).get("schedule")
    ]
    scheduled_md = (
        "\n".join(
            f"- 📅 `/{sid}` — {skills_spec[sid]['schedule']}" for sid in sorted(scheduled)
        )
        if scheduled
        else "_Aucun pour l'instant._"
    )

    phase_syms = {i: _phase_symbol(phase, i) for i in range(6)}

    lines = [
        "---",
        "template: setup-checklist",
        "version: 0.1",
        "auto_generated: true",
        f"last_updated: \"{now}\"",
        "---",
        "",
        "# 🚀 OpowAI Setup — Checklist",
        "",
        "> Cette checklist se met à jour automatiquement à chaque étape. "
        "Tu peux la quitter à tout moment et reprendre où tu en étais en "
        "relançant `/setup-opowai`. Pour un statut rapide : `/opowai-status`.",
        "",
        "## 📊 Avancement global",
        "",
        f"**{phase} / 5 phases · {summ['phase_pct']}% complété**",
        "",
        "```",
        _progress_bar(summ["phase_pct"]),
        "```",
        "",
        "---",
        "",
        f"## Phase 0 — Bienvenue & priorisation {phase_syms[0]}",
        "",
        f"- [{'x' if phase >= 1 else ' '}] Lecture du `WELCOME.md`",
        f"- [{'x' if phase >= 1 else ' '}] Sélection des cas d'usage prioritaires",
        "",
        f"**Cas d'usage sélectionnés :**",
        "",
        selected_labels,
        "",
        "---",
        "",
        f"## Phase 1 — Connexion thématique {phase_syms[1]}",
        "",
        "Cocher au fur et à mesure des connexions. Chaque connexion débloque "
        "immédiatement des skills (voir Phase 4).",
        "",
        *table_lines,
        "",
        "---",
        "",
        f"## Phase 2 — Auto-discovery {phase_syms[2]}",
        "",
        f"Statut : `{state.get('auto_discovery_status', 'not_started')}`",
        "",
        "---",
        "",
        f"## Phase 3 — Confirmation guidée {phase_syms[3]}",
        "",
        f"- [{'x' if phase >= 4 else ' '}] Profil utilisateur confirmé",
        f"- [{'x' if phase >= 4 else ' '}] Company profile confirmé",
        f"- [{'x' if phase >= 4 else ' '}] COMEX confirmé",
        f"- [{'x' if phase >= 4 else ' '}] Pillars stratégiques validés",
        f"- [{'x' if phase >= 4 else ' '}] Privacy rules confirmées",
        "",
        "---",
        "",
        f"## Phase 4 — Activation des skills & agents {phase_syms[4]}",
        "",
        f"### Skills activés ({len(by_state[ACTIVATED])})",
        "",
        render_skill_list(by_state[ACTIVATED]),
        "",
        f"### Skills en attente ({len(by_state[PENDING])})",
        "",
        render_pending_list(by_state[PENDING]),
        "",
        f"### Skills dormants — non sélectionnés en phase 0 ({len(by_state[DORMANT])})",
        "",
        render_dormant_list(by_state[DORMANT]),
        "",
        f"### Agents récurrents programmés ({len(scheduled)})",
        "",
        scheduled_md,
        "",
        "---",
        "",
        f"## Phase 5 — Premier run {phase_syms[5]}",
        "",
        f"- [{'x' if phase >= 5 else ' '}] Page Notion racine \"📚 OpowAI SOPs\" créée",
        f"- [{'x' if phase >= 5 else ' '}] Premier `/daily-plan` lancé en démo",
        f"- [{'x' if phase >= 5 else ' '}] Routing modèle configuré dans `settings.json`",
        "",
        "---",
        "",
        "## 💡 Aide",
        "",
        "- `bin/opowai status` — vue rapide de l'état système",
        "- `bin/opowai resume` — reprendre où tu en étais",
        "- `bin/opowai redo <thematic>` — reconfigurer une thématique",
        "- `bin/opowai add-tool` — ajouter un outil \"Autre\"",
        "",
    ]
    return "\n".join(lines)


def write_checklist(
    state: dict[str, Any],
    prereqs: dict[str, Any],
    path: Path | str | None = None,
) -> Path:
    """Write the checklist markdown to disk and return the path."""
    target = Path(path) if path else DEFAULT_CHECKLIST_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(generate_checklist(state, prereqs), encoding="utf-8")
    return target
