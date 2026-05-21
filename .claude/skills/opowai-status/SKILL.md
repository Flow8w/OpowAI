---
name: opowai-status
description: Affiche un statut complet du système OpowAI — thématiques connectées, skills activés / en attente / dormants, agents programmés, prochaines exécutions, suggestions d'amélioration.
status: implemented-v0.1
version: 0.1
implementation: .scripts/opowai/status.py
cli: bin/opowai status
---

## Usage rapide

```bash
./bin/opowai status
```

Implémenté en Python dans `.scripts/opowai/status.py`. Lecture des 4 sources (yaml, state.json, checklist, cron) et génération d'un dashboard ASCII.

---


# /opowai-status

Vue rapide de l'état du système. Lisible à tout moment, jamais bloquant.

## Trigger
- Manuel : `/opowai-status`
- Auto-trigger discret en fin de chaque autre skill majeur (option `--show-status`)

## Workflow

1. Lit `System/skill-prerequisites.yaml` (mapping)
2. Lit `System/.setup-state.json` (état actuel)
3. Lit `System/setup-checklist.md` (avancement)
4. Lit `.scripts/cron/opowai.cron` (agents programmés)
5. Génère un rapport structuré

## Output exemple

```
📊 OpowAI Status — 2026-05-21 14:32

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Avancement   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 70%
  Phase        Phase 4 / 5 — Activation en cours
  Cas d'usage  3 sélectionnés : Pipeline, Coaching, Support

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THÉMATIQUES (7 / 10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✅ 1. CRM & Sales         → Pipedrive
  ✅ 2. Email               → Gmail
  ✅ 3. Calendar            → Google Calendar
  ✅ 4. Knowledge & docs    → Notion
  ✅ 5. Communication chat  → Slack
  ✅ 6. Project & Roadmap   → Jira
  🔘 7. Data & Analytics    → todo
  ✅ 8. Transcript          → Granola
  🔘 9. Code & Dev          → todo (optionnel)
  🔘 10. Autre              → todo (optionnel)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILLS (14 activés / 24 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Rituels quotidiens
    ✅ /daily-plan          📅 Mon-Fri 08:00
    ✅ /daily-review
    ✅ /meeting-prep
    ✅ /process-meetings
    ✅ /triage

  Sales & pipeline
    ✅ /friday-close        📅 Fri 16:00
    ✅ /coach-sales-self    📅 Fri 15:30
    ✅ /coach-team-member
    ✅ /pipeline-monitor    📅 Mon 09:00
    ✅ /prep-meeting

  Support client
    ✅ /draft-support-reply 📅 Mon-Fri 09:00, 14:00

  Communication interne
    ✅ /all-hands           📅 Last Fri 14:00
    ✅ /publish-sop
    ✅ /sync-cowork         📅 Sun 22:00

  En attente d'autres outils (4)
    ⏳ /board-prep          → attend Data & Analytics
    ⏳ /exec-summary        → attend Data & Analytics
    ⏳ /roadmap-sync        → attend Project (✅ déjà connecté — devrait s'activer)
    ⏳ /mockup-from-repo    → attend Code & Dev

  Dormants (non sélectionnés en phase 0) (6)
    🔒 /quarter-plan, /quarter-review, /fundraising-tracker,
       /competitor-watch, /operating-rhythm-audit, /health-score-builder

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLAYBOOKS (5 activés / 18 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✅ 05-okr-operating-model
  ✅ 06-customer-success-churn
  ✅ 07-sales-stage-gates
  ✅ 11-operating-cadence
  ✅ 13-gtm-foundations

  13 playbooks disponibles non activés
  → /opowai-playbooks list pour voir, /opowai-playbooks activate [num] pour activer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROCHAINES EXÉCUTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Aujourd'hui 14:00  /draft-support-reply (scan support)
  Demain 08:00       /daily-plan
  Vendredi 15:30     /coach-sales-self
  Vendredi 16:00     /friday-close
  Vendredi 17:00     /drift-detection
  Dimanche 22:00     /sync-cowork
  29 mai 14:00       /all-hands (premier vrai run)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUGGESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  💡 Connecter Stripe (Data) débloquerait /board-prep et /exec-summary
     → /setup-opowai --add-tool stripe

  ⚠️  /roadmap-sync devrait être activé (Project connecté) — bug à vérifier
     → /setup-opowai --redo phase-4

  📚 13 playbooks dispos non actifs — pertinents pour toi :
     • 03-pricing-monetization (tu cherches à itérer ton pricing ?)
     • 04-board-investor-comm (utile pour /board-prep)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## TODO d'implémentation v0.1
- [ ] Lecture et parsing des 4 sources (yaml, json, md, cron)
- [ ] Calcul du % d'avancement
- [ ] Détection des "should be activated but isn't" (bug check)
- [ ] Génération des suggestions intelligentes (skills non activés, playbooks pertinents)
- [ ] Format console clean (ASCII art ou Unicode box-drawing)
