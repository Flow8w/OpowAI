"""OpowAI setup orchestration engine.

Python implementation of the engine spec'd in `.claude/skills/setup-opowai/SKILL.md`
and `System/skill-prerequisites.yaml`.

Public entry points live in :mod:`cli`. Logic is split across:

- :mod:`state` — persistence of `.setup-state.json`
- :mod:`engine` — skill-state computation and progression
- :mod:`activation` — skill activation diffs
- :mod:`thematics` — thematic prompt formatting
- :mod:`checklist` — markdown checklist generation
- :mod:`status` — `/opowai-status` dashboard
- :mod:`cron` — agent scheduling
"""

__version__ = "0.1.0"
