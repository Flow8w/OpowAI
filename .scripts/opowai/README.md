# OpowAI Setup Engine

Implémentation Python du moteur d'orchestration du setup OpowAI.

## Architecture

```
.scripts/opowai/
├── cli.py            # Point d'entrée CLI (subcommands)
├── engine.py         # Cœur : parse YAML, calcule l'état des skills
├── state.py          # Persistance .setup-state.json
├── checklist.py      # Génération de System/setup-checklist.md (temps réel)
├── status.py         # Dashboard /opowai-status (ASCII art)
├── cron.py           # Programmation des agents récurrents
├── thematics.py      # Présentation thématique + name-dropping
├── activation.py     # Calcul du diff d'unlock à chaque connexion
├── connectors/       # Documentation des MCPs (la connexion réelle = Claude Code)
├── tests/            # pytest — 6 tests sur engine + activation
└── requirements.txt
```

## Sources de vérité

| Fichier | Rôle |
|---------|------|
| `System/skill-prerequisites.yaml` | Mapping skills ↔ thématiques ↔ use cases (statique) |
| `System/.setup-state.json` | État utilisateur (dynamique, gitignored) |
| `System/setup-checklist.md` | Vue lisible (régénérée à chaque changement) |
| `.scripts/cron/opowai.cron` | Agents récurrents programmés |

## Usage

### Wrapper shell (recommandé)
```bash
./bin/opowai status
./bin/opowai init
./bin/opowai connect crm --tool pipedrive
./bin/opowai checklist
./bin/opowai resume
```

### Invocation directe
```bash
python3 .scripts/opowai/cli.py status
```

## Sous-commandes

| Commande | Rôle |
|----------|------|
| `init` | Phase 0 — welcome + priorisation 3 cas d'usage |
| `connect [thematic]` | Phase 1 — connexion d'une thématique (avec `--tool [id]`) |
| `discover` | Phase 2 — lance auto-discovery |
| `confirm` | Phase 3 — confirmation profil pré-rempli |
| `activate` | Phase 4 — active skills/agents prêts |
| `first-run` | Phase 5 — page Notion + premier daily-plan |
| `status` | Dashboard complet de l'état système |
| `checklist` | Régénère `System/setup-checklist.md` |
| `resume` | Reprend le setup où on en était |
| `redo [thematic]` | Reconfigure une thématique |
| `add-tool` | Ajoute un outil "Autre" (thématique 10) |
| `change-use-cases` | Re-priorise les cas d'usage sélectionnés |

## Tests

```bash
# Depuis la racine du repo
python3 -m pytest .scripts/opowai/tests/ -v
```

6 tests couvrent :
- `test_compute_skill_states` — catégorisation correcte (activated / pending / dormant / todo)
- `test_thematic_progression` — ordre fixe respecté, next thematic calculé
- `test_summary_counts` — agrégations correctes
- `test_compute_unlock_diff_adds_transcript` — débloque les bons skills à la connexion
- `test_compute_unlock_diff_empty_when_unchanged` — pas de notification parasite
- `test_activate_skill_is_idempotent` — activer 2× = même résultat

## Logique de catégorisation des skills

À chaque appel de `engine.compute_skill_states(state, prereqs)`, chaque skill du YAML reçoit un statut :

| Statut | Condition |
|--------|-----------|
| `🔒 dormant` | Le skill n'appartient à aucun `use_case` sélectionné en phase 0 |
| `✅ activated` | Toutes les `required` thématiques sont dans `completed_thematics` |
| `⏳ pending` | Sélectionné + au moins une `required` est manquante |
| `🔘 todo` | Aucune `required` connectée |

Les `optional` ne bloquent jamais l'activation — elles enrichissent le skill quand connectées.

## Ajouter une nouvelle thématique

1. Ajouter une entrée dans `System/skill-prerequisites.yaml > thematics:` avec `id`, `order`, `tools`, `why_matters`.
2. Si nécessaire, ajouter un `use_case` qui la requiert.
3. Référencer la thématique dans les `required`/`optional` des skills concernés.
4. `pytest` doit toujours passer — sinon, mettre à jour la fixture.

## Ajouter un nouveau skill

1. Ajouter une entrée dans `System/skill-prerequisites.yaml > skills:` avec `required`, `optional`, `unlock_message`, `category`, `schedule` (optionnel).
2. L'inclure dans au moins un `use_case` (sinon il sera permanent dormant).
3. Créer `.claude/skills/[name]/SKILL.md` — sera lu par Claude Code à l'activation.
4. Aucune modif de code Python nécessaire.

## Schéma du state

```jsonc
{
  "current_phase": "0|1|2|3|4|5",
  "current_thematic": "crm|email|...",
  "completed_thematics": {"crm": "pipedrive", "email": "gmail"},
  "skipped_thematics": ["code"],
  "selected_use_cases": ["pipeline-prep", "coaching-sales"],
  "auto_discovery_status": "not_started|running|done",
  "activated_skills": ["friday-close", "draft-support-reply"],
  "user_profile": {...},
  "company_profile": {...},
  "started_at": "ISO",
  "last_update": "ISO"
}
```

`System/.setup-state.json` est **gitignored** — c'est l'état personnel de chaque utilisateur d'OpowAI.

## Limites de la v0.1

- **Connecteurs MCP simulés** : la connexion réelle Pipedrive/Gmail/Notion/etc. se fait via Claude Code, pas via Python. `opowai connect crm --tool pipedrive` ne fait que marquer l'état "connecté" — le vrai auth flow doit être déclenché par Claude Code.
- **Cron macOS uniquement** en v0.1 — sous Linux, l'utilisateur installe manuellement via crontab. Sous Windows, pas supporté.
- **Pas d'UI de progression live** — l'utilisateur lance `opowai status` ou ouvre `System/setup-checklist.md` pour voir l'avancement. Pas de TUI animée en v0.1.

## v0.2 envisagée

- Connecteurs MCP réels (déclenchement des auth flows depuis Python via subprocess Claude Code)
- TUI animée (Rich / Textual)
- Migration vers GitHub Actions pour les agents programmés
- Skill `/opowai-test-connector` pour vérifier qu'un MCP répond
