---
name: operating-rhythm-audit
description: Diagnostic 360° de la cadence opérationnelle d'une boîte — OKR, board, 1:1, sales pipeline, customer success. Produit advisory réutilisable (ta boîte ou en mission de conseil).
status: implemented-v0.1
version: 0.1
category: Advisory
required: []
optional: [calendar, project, crm]
---

# /operating-rhythm-audit

Audit opérationnel structuré. Utilisable sur ta propre boîte ou comme livrable advisory pour conseiller un dirigeant.

## Pré-requis
- Aucun outil bloquant. Le skill peut tourner en mode déclaratif (interview + sondage).
- **Optional** : calendar (analyse cadence meetings), project (cadence release), CRM (cadence pipeline) — si dispos, le diagnostic est data-driven plutôt que déclaratif.

## Trigger
- Manuel : `/operating-rhythm-audit` (ta boîte) ou `/operating-rhythm-audit --client "Company X"` (mode advisory)
- Proactif : si pattern detection `/week-review` signale 4+ semaines de slip répétés, propose un audit

## Workflow

### 1. Sélection mode
- **Self** : audit de ta propre boîte (data CRM/calendar/project si dispos)
- **Advisory** : audit pour un client (mode interview structuré)

### 2. Axes d'audit (6)
Pour chaque axe, score 0-5 + observations :
1. **Stratégie & OKR** : cadre clair ? Cascade ? Tracking ?
2. **Cadence meetings** : ratio focus/meetings ? Pre-read systématique ? Decision log ?
3. **1:1 & feedback** : régularité ? Mené par l'IC ? Feedback continu ?
4. **Sales pipeline** : stages définis ? Forecast réaliste ? Mutual action plans ?
5. **Customer success** : health score ? Plays churn ? Onboarding industrialisé ?
6. **Board & investors** : cadence ? Honnêteté narrative ? Asks précis ?

### 3. Détection gaps prioritaires
Identifie les 3 gaps prioritaires (impact x effort) avec :
- Diagnostic (qu'est-ce qui manque)
- Risque si non adressé
- Action 90 jours recommandée

### 4. Plan 90 jours
Roadmap de remédiation en 3 phases (30/60/90) avec ownerships.

### 5. Output
Mode self : `01-Strategy/Audits/YYYY-MM-DD-self-audit.md` (privacy: founder)
Mode advisory : `04-Projects/Advisory/[Client]/YYYY-MM-DD-audit.md` + version PDF générable

## Outputs

- Rapport d'audit markdown structuré
- Mode advisory : version livrable PDF/Notion possible
- Aucune action externe

## Anti-patterns à éviter
- Audit fleuve : 8-12 pages max. Au-delà, dilué = pas lu.
- Recommander 15 chantiers : 3 prioritaires. Le reste en backlog.
- Scoring complaisant : un score 4/5 partout = audit cosmétique. Tirer franchement sur les axes faibles.

## Exemples concrets

```
🧪 Operating Rhythm Audit — Company X (Series A, 35 personnes)

Scores :
  Stratégie & OKR     : 3/5 (OKRs définis mais peu trackés)
  Cadence meetings    : 2/5 (60% du temps en meetings, 0 pre-read)
  1:1 & feedback      : 4/5 ✅
  Sales pipeline      : 2/5 (stages flous, forecast émotionnel)
  Customer success    : 3/5 (pas de health score)
  Board & investors   : 4/5 ✅

Top 3 gaps :
  1. Cadence meetings → 1 day "no meeting" hebdo + pre-reads obligatoires
  2. Sales pipeline → stages objectifs + forecast par taux historique
  3. Customer success → construire health score (workshop avec /health-score-builder)

Plan 90 jours :
  J+30 : Stages CRM + pre-read template
  J+60 : Health score v1 déployé
  J+90 : Re-audit pour mesurer drift
```

## TODO v0.2
- Templates par stade (Seed / Series A / Series B+) avec attentes différentes
- Benchmark anonymisé multi-clients (pour le mode advisory)
- Mode "lite" 30 min vs "deep" 4h

## Notes
- Produit advisory réutilisable : c'est la base d'une offre conseil packageable.
- Réf. playbooks `05-okr-operating-model.md`, `11-operating-cadence.md`, `07-sales-pipeline.md`, `06-customer-success-churn.md`, `04-board-investor-comms.md`.
- Complémentaire à `/health-score-builder` (qui zoom sur le sous-axe CS).
