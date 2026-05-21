---
name: fundraising-tracker
description: Pipeline investisseurs (private:founder) — tracking first meetings, follow-ups, due diligence, term sheets. Le CRM du founder pour son tour de table.
status: implemented-v0.1
version: 0.1
category: Stratégie & capital
required: []
optional: [email, calendar]
---

# /fundraising-tracker

CRM dédié fundraising. Privé au founder, jamais sync ailleurs.

## Pré-requis
- Aucun outil bloquant (peut fonctionner en mode déclaratif).
- **Optional** : email (logging des threads investisseurs), calendar (logging des meetings).

## Trigger
- Manuel : `/fundraising-tracker` (vue d'ensemble) ou `/fundraising-tracker add "Sequoia"` (ajout)
- Programmé : aucun
- Proactif : si email reçu d'un investisseur tracké, suggère de logger l'interaction

## Workflow

### 1. Structure stockage
Fichier central : `01-Strategy/Fundraising/investors.yaml` (privacy: founder).
Format :
```yaml
investors:
  - id: sequoia
    name: "Sequoia"
    stage_fit: "Series A"
    contact: "..."
    status: "first_meeting"
    last_interaction: 2026-05-15
    next_step: "Follow-up call 2026-05-28"
    intro_via: "Board member X"
    private_notes: "..."
```

### 2. Vue d'ensemble
Quand lancé sans argument, affiche :
- Funnel : Sourcing → First meeting → Deep dive → DD → Term sheet
- Top 5 plus avancés
- Stalled : pas d'interaction depuis > 14 jours

### 3. Ajout / update
Mode interactif pour ajouter un investisseur ou mettre à jour un statut.

### 4. Logging interactions
Si email/calendar connectés, scanne les threads/meetings avec investisseurs trackés et propose de logger l'interaction.

### 5. Sync avec exec-summary
Quand `/exec-summary` est lancé, ce skill peut alimenter la section "Asks" (intros manquantes) automatiquement.

## Outputs

- `01-Strategy/Fundraising/investors.yaml` (privacy: founder)
- Notes par investisseur dans `01-Strategy/Fundraising/Notes/[Investor]/*.md`
- Aucune action externe

## Anti-patterns à éviter
- Tracker en CRM partagé : c'est de l'info personnelle stratégique du founder, jamais en COMEX sauf décision explicite.
- Surentry : 50 investisseurs trackés = 0 investisseur travaillé. Cible 15-20 actifs max sur un tour.
- Confondre intérêt et engagement : un "very interesting" n'est pas un term sheet.

## Exemples concrets

```
💰 Fundraising tracker — Vue d'ensemble

Funnel Series A (8M€ target) :
  Sourcing       : 32 investisseurs
  First meeting  : 14 (en cours)
  Deep dive      : 5
  DD             : 2
  Term sheet     : 0

Top 5 plus avancés :
  1. Investor X — DD (data room shared 2026-05-12, attente questions)
  2. Investor Y — Deep dive (2nd meeting 2026-05-23)
  3. Investor Z — Deep dive (partner meeting 2026-05-28)
  4. Investor A — 1st meeting (J+8, follow-up à envoyer)
  5. Investor B — 1st meeting (J+12, à relancer ⚠️)

Stalled (>14j sans interaction) :
  • Investor C (24j) — relance ?
  • Investor D (18j) — passer ?
```

## TODO v0.2
- Templates de relance par stage
- Tracking automatique deal velocity (jours entre stages)
- Intégration aux exec summaries pour Asks investisseurs

## Notes
- Privacy : `private: founder` STRICT. Le fichier vit dans `01-Strategy/Fundraising/` qui est en sortie de tout sync.
- Réf. playbook `09-fundraising-readiness.md`.
- Complémentaire à `/board-prep` (qui informe les boards et donc les futurs investisseurs).
