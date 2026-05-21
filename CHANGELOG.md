# Changelog

## v0.1.0 — 2026-05-20

### Initial fork from Dex v1.11.0

**Architecture**
- 11 dossiers PARA-inspirés adaptés founder/COMEX (ajout `01-Strategy`, `02-Company`, `05-Operations`, `08-Coaching`)
- Modèle privacy 3 niveaux : `founder` / `comex` / `public` via frontmatter + `System/privacy-rules.yaml`
- GitHub-first : `Flow8w/OpowAI` (privé) source de vérité, local working copy avec auto-sync

**Skills (v0.1 specs, implémentation en cours)**
- `/setup-opowai` — onboarding 5 phases (Connect → Discover → Confirm → Playbooks → First Run)
- `/sync-cowork` — sync hebdo vers Cowork avec filtrage privacy
- `/publish-sop` — page racine Notion "📚 OpowAI SOPs" + arborescence auto
- `/draft-support-reply` — brouillons mail support (P0 use case)
- `/all-hands` — prep all-hands mensuel avec template structuré
- `/context-cards` — cards modulaires pour Cowork
- `/people-intel` — enrichissement people via Scrapling
- `/drift-detection` — détection dérives hebdo

**Playbooks pré-injectés**
- 4 markdown depuis Dex : branding zero-risk, AARRR growth, David Sacks cadence, IA productivity
- 3 HTML à convertir (coaching, SaaS, vente-valeur) — pandoc à installer
- 1 docx à convertir (valeur client)

**Templates**
- `System/templates/allhands-template.md` — template all-hands modifiable

**Notes**
- Agents récurrents en local v0.1 (cron) — migration GitHub Actions prévue v0.2
- Convertir HTML/docx playbooks dès installation pandoc
- Implémentations détaillées des skills à finaliser avant le setup le client vendredi
