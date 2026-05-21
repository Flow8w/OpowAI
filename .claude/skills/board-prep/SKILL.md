---
name: board-prep
description: Préparation du board meeting — KPIs trackés, narrative consistant avec board précédent, Highlights/Lowlights/Asks, anticipation des Q&A.
status: implemented-v0.1
version: 0.1
category: Stratégie & capital
required: [crm]
optional: [analytics, project, docs]
---

# /board-prep

Génère le draft du board deck à partir de la matière disponible. Le founder valide et raffine — OpowAI ne va PAS au board à ta place.

## Pré-requis
- **Required** : CRM (KPIs pipeline et ARR).
- **Optional** : analytics (MRR, churn $, retention), project (roadmap status), docs (board précédent dans Notion).

## Trigger
- Manuel : `/board-prep` ou `/board-prep --date 2026-06-15`
- Programmé : aucun. Recommandé : 1 semaine avant le board.
- Proactif : si board détecté dans le calendar à < 7 jours, suggère

## Workflow

### 1. Recharge contexte board précédent
- Lit le board deck précédent (Notion ou `06-Meetings/Board/`)
- Extrait les asks faits / commitments donnés
- Extrait les KPIs trackés pour assurer consistency (mêmes définitions, mêmes scopes)

### 2. Fetch KPIs actuels
- ARR / NRR / GRR (CRM + analytics)
- Cash position + runway (manuel ou data analytics)
- Pipeline coverage
- Roadmap : shipped / in-progress / at-risk (project mgmt)
- Team : hires, departures

### 3. Draft narrative
Structure :
- **TL;DR** (3 bullets)
- **Highlights** (3-5 wins concrets avec data)
- **Lowlights** (2-3 — honnêteté > spin)
- **KPI dashboard** (mêmes KPIs que board précédent)
- **Roadmap update**
- **Asks au board** (1-3 demandes précises)
- **Risks** (top 3 avec mitigations)

### 4. Anticipation Q&A
Sur la base des lowlights/asks, Claude propose 5-8 questions probables avec réponses brèves draftées.

### 5. Output
Écrit `06-Meetings/Board/YYYY-MM-DD-board-draft.md` (privacy: founder).
Optionnel : génère deck Google Slides / PPTX si template configuré.

## Outputs

- `06-Meetings/Board/YYYY-MM-DD-board-draft.md` (privacy: founder)
- Notification au founder uniquement
- Aucune publication automatique vers les investisseurs

## Anti-patterns à éviter
- Spin sur les lowlights : un board sent le spin à 1km. Honnêteté > polish.
- Changer la définition d'un KPI sans signaler : ARR doit être calculé pareil qu'au board précédent (sinon le noter explicitement).
- Asks vagues : "On a besoin de support" n'est pas un ask. "Intro à 3 prospects ICP Series B" en est un.

## Exemples concrets

```
🎩 Board prep — 2026-06-15

TL;DR :
  • ARR 1.4M€ (+18% QoQ), runway 14 mois post next fundraise
  • Customer Success en train de se restructurer (un risque court terme)
  • Demande au board : 5 intros investisseurs Series A

Highlights :
  • Acme deal signé (180k€ ARR, biggest to date)
  • NRR 118% (vs 105% au board précédent)
  • Time-to-value moyen passé de 6 sem à 3 sem

Lowlights :
  • Churn $ +40% Q3 vs Q2 (3 départs concentrés)
  • Head of CS départ surprise (recrutement en cours)

Asks :
  1. Intros investisseurs Series A (cible : closer term sheet Q4)
  2. Validation pivot positionnement enterprise (slide #12)
  3. Connexion à 2-3 candidats Head of CS
```

## TODO v0.2
- Génération automatique du deck (PPTX/Slides) avec template board
- Comparaison auto avec boards précédents (drift de narrative)
- Mode "post-board" : extraction des décisions et asks à tracker

## Notes
- Privacy : `private: founder` strict. Jamais sync vers Cowork ou Notion public.
- Réf. playbooks `04-board-investor-comms.md`, `09-fundraising-readiness.md`.
