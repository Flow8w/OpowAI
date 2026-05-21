#!/usr/bin/env python3
"""OpowAI CLI — subcommands wrapping the engine.

Usage:
    opowai <subcommand> [args]

Run ``opowai --help`` for the full list.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Allow running as a script (no package import) by inserting parent dir on path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from opowai import activation, checklist, cron, engine, state, status, thematics
else:
    from . import activation, checklist, cron, engine, state, status, thematics


def _load(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    st = state.load_state(args.state) if args.state else state.load_state()
    prereqs = engine.load_prerequisites(args.prereqs) if args.prereqs else engine.load_prerequisites()
    return st, prereqs


def cmd_status(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    print(status.generate_status_report(st, prereqs))
    return 0


def cmd_checklist(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    path = checklist.write_checklist(st, prereqs)
    print(f"Wrote {path}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    st = state.empty_state()
    if args.use_cases:
        st["selected_use_cases"] = [uc.strip() for uc in args.use_cases.split(",") if uc.strip()]
    st["current_phase"] = "1" if st["selected_use_cases"] else "0"
    state.save_state(st)
    prereqs = engine.load_prerequisites()
    checklist.write_checklist(st, prereqs)
    print("Initialized OpowAI setup state.")
    print(f"  Selected use cases: {st['selected_use_cases'] or '(none)'}")
    print(f"  Current phase: {st['current_phase']}")
    print("Next: bin/opowai connect [thematic_id]")
    return 0


def cmd_connect(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    thematic_id = args.thematic or (
        (engine.get_next_thematic(st, prereqs) or {}).get("id")
    )
    if not thematic_id:
        print("All thematics handled. Nothing to connect.")
        return 0

    if not args.tool:
        # Print the prompt and exit — Claude/the user picks a tool.
        print(thematics.format_thematic_prompt(thematic_id, prereqs))
        print("\nRun again with --tool <tool_id> to record the connection.")
        return 0

    before = json.loads(json.dumps(st))  # deep copy
    if args.tool == "skip":
        skipped = list(st.get("skipped_thematics") or [])
        if thematic_id not in skipped:
            skipped.append(thematic_id)
        st["skipped_thematics"] = skipped
    else:
        completed = dict(st.get("completed_thematics") or {})
        completed[thematic_id] = args.tool
        st["completed_thematics"] = completed

    # Re-activate any newly-eligible skill
    skill_states = engine.compute_skill_states(st, prereqs)
    for sid, s in skill_states.items():
        if s == engine.ACTIVATED:
            activation.activate_skill(sid, st, prereqs)

    st["current_phase"] = "1"
    state.save_state(st)
    checklist.write_checklist(st, prereqs)
    cron.write_cron_file(st["activated_skills"], prereqs)

    print(thematics.format_unlock_notification(args.tool, prereqs, before, st))
    nxt = engine.get_next_thematic(st, prereqs)
    if nxt:
        print(f"Prochaine thématique : {nxt['name']} (`bin/opowai connect {nxt['id']}`)")
    else:
        print("Toutes les thématiques sont traitées. → `bin/opowai discover`")
    return 0


def cmd_discover(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    st["auto_discovery_status"] = "done"  # v0.1 stub
    st["current_phase"] = "2"
    state.save_state(st)
    checklist.write_checklist(st, prereqs)
    print("Auto-discovery marqué comme terminé (stub v0.1).")
    print("Lance `bin/opowai confirm` pour passer en phase 3.")
    return 0


def cmd_confirm(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    st["current_phase"] = "3"
    state.save_state(st)
    checklist.write_checklist(st, prereqs)
    print("Phase 3 (confirmation) marquée comme terminée.")
    return 0


def cmd_activate(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    skill_states = engine.compute_skill_states(st, prereqs)
    activated_now = []
    for sid, s in skill_states.items():
        if s == engine.ACTIVATED and sid not in (st.get("activated_skills") or []):
            activation.activate_skill(sid, st, prereqs)
            activated_now.append(sid)
    st["current_phase"] = "4"
    state.save_state(st)
    checklist.write_checklist(st, prereqs)
    cron.write_cron_file(st["activated_skills"], prereqs)
    if activated_now:
        print(f"Activated {len(activated_now)} skill(s):")
        for sid in activated_now:
            print(f"  ✅ /{sid}")
    else:
        print("No new skills to activate.")
    return 0


def cmd_first_run(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    st["current_phase"] = "5"
    state.save_state(st)
    checklist.write_checklist(st, prereqs)
    print("🎉 OpowAI setup terminé. Tape `bin/opowai status` pour la vue d'ensemble.")
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    nxt = engine.get_next_thematic(st, prereqs)
    print(f"Phase courante : {st['current_phase']}")
    print(f"Thématiques connectées : {list((st.get('completed_thematics') or {}).keys())}")
    if nxt:
        print(f"Prochaine étape : connecter {nxt['name']} → `bin/opowai connect {nxt['id']}`")
    else:
        print("Toutes les thématiques sont traitées. → `bin/opowai discover`")
    return 0


def cmd_redo(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    completed = dict(st.get("completed_thematics") or {})
    completed.pop(args.thematic, None)
    skipped = [t for t in (st.get("skipped_thematics") or []) if t != args.thematic]
    st["completed_thematics"] = completed
    st["skipped_thematics"] = skipped
    state.save_state(st)
    checklist.write_checklist(st, prereqs)
    print(f"Thématique '{args.thematic}' réinitialisée. → `bin/opowai connect {args.thematic}`")
    return 0


def cmd_add_tool(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    completed = dict(st.get("completed_thematics") or {})
    completed[args.thematic] = args.tool
    st["completed_thematics"] = completed
    state.save_state(st)
    checklist.write_checklist(st, prereqs)
    print(f"Tool '{args.tool}' ajouté à la thématique '{args.thematic}'.")
    return 0


def cmd_change_use_cases(args: argparse.Namespace) -> int:
    st, prereqs = _load(args)
    st["selected_use_cases"] = [uc.strip() for uc in args.use_cases.split(",") if uc.strip()]
    state.save_state(st)
    checklist.write_checklist(st, prereqs)
    print(f"Use cases mis à jour : {st['selected_use_cases']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opowai", description="OpowAI setup orchestration")
    parser.add_argument("--state", help="Custom state file path")
    parser.add_argument("--prereqs", help="Custom skill-prerequisites.yaml path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show OpowAI status dashboard").set_defaults(func=cmd_status)
    sub.add_parser("checklist", help="Regenerate System/setup-checklist.md").set_defaults(func=cmd_checklist)

    p_init = sub.add_parser("init", help="Initialize setup (phase 0)")
    p_init.add_argument("--use-cases", help="Comma-separated use case IDs")
    p_init.set_defaults(func=cmd_init)

    p_connect = sub.add_parser("connect", help="Connect a thematic")
    p_connect.add_argument("thematic", nargs="?", help="Thematic ID (defaults to next)")
    p_connect.add_argument("--tool", help="Tool ID, or 'skip' to skip the thematic")
    p_connect.set_defaults(func=cmd_connect)

    sub.add_parser("discover", help="Mark auto-discovery as done").set_defaults(func=cmd_discover)
    sub.add_parser("confirm", help="Mark phase 3 (confirmation) as done").set_defaults(func=cmd_confirm)
    sub.add_parser("activate", help="Activate eligible skills (phase 4)").set_defaults(func=cmd_activate)
    sub.add_parser("first-run", help="Mark phase 5 as done").set_defaults(func=cmd_first_run)
    sub.add_parser("resume", help="Show where we left off").set_defaults(func=cmd_resume)

    p_redo = sub.add_parser("redo", help="Reconfigure a thematic")
    p_redo.add_argument("thematic", help="Thematic ID to redo")
    p_redo.set_defaults(func=cmd_redo)

    p_add = sub.add_parser("add-tool", help="Add an 'Autre' tool to a thematic")
    p_add.add_argument("thematic", help="Thematic ID")
    p_add.add_argument("tool", help="Tool ID / free-form name")
    p_add.set_defaults(func=cmd_add_tool)

    p_chg = sub.add_parser("change-use-cases", help="Re-prioritise use cases")
    p_chg.add_argument("use_cases", help="Comma-separated use case IDs")
    p_chg.set_defaults(func=cmd_change_use_cases)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
