---
name: quarter-review
description: Revue de fin de trimestre — scoring OKRs, learnings, ajustements stratégiques, prep du quarter-plan suivant.
status: implemented-v0.1
version: 0.1
category: Rituels trimestriels
required: []
optional: [crm, analytics]
---

# /quarter-review

Boucle d'apprentissage stratégique. Ce qu'on n'apprend pas en revue trimestrielle se paie au prochain.

## Pré-requis
- Aucun outil bloquant.
- **Optional** : CRM (vérification objective des KR pipeline), analytics (KR produit/MRR).

## Trigger
- Manuel : `/quarter-review`
- Programmé : aucun (volontaire, dernière semaine du quarter)
- Proactif : si on est dans la dernière semaine et pas de review lancée

## Workflow

### 1. Recharge OKRs du quarter
Charge `01-Strategy/Quarter_Goals.md` et les week-reviews des 12-13 semaines.

### 2. Scoring objectif des KRs
Pour chaque KR :
- Score Google-style 0.0 - 1.0
- Source de vérité (CRM/Analytics si connecté, sinon déclaratif)
- Rationale 1 ligne

### 3. Pattern detection trimestrielle
Synthèse des patterns hebdo récurrents :
- Quels OKRs ont systématiquement glissé ?
- Quels patterns de focus ont marché ?
- Quels signaux faibles ont été ignorés ?

### 4. Learnings stratégiques
Capture 3-5 learnings niveau "stratégie" (pas tactique). Écrit dans `09-Resources/Quarter_Learnings/YYYY-QX.md`.

### 5. Prep transition
Liste les sujets à reprendre dans `/quarter-plan` du Q+1 (OKRs partiellement atteints à pousser, dette technique/stratégique).

## Outputs

- `10-Archives/Quarter_Goals/YYYY-QX.md` (avec scores ajoutés)
- `09-Resources/Quarter_Learnings/YYYY-QX.md`
- Brief de transition pour `/quarter-plan`
- Notification chat

## Anti-patterns à éviter
- Self-congratulation : un quarter "tout vert" est suspect. Soit les OKRs étaient mous, soit le scoring est laxiste.
- Pas d'action : si une review génère 0 ajustement stratégique, c'est cosmétique.
- Oublier le COMEX : les KRs cascadés doivent être scorés par leur owner, pas le founder seul.

## Exemples concrets

```
🔍 Quarter_Review Q2 2026

OKR 1 — Capital readiness : 0.6
  KR1 (data room) : 1.0 ✅
  KR2 (15 first meetings) : 0.5 (8/15)
  KR3 (term sheet) : 0.0 — décalé Q3

OKR 2 — Pipeline 2x ARR : 0.8 ✅
  KR1 : 2.3M€ pipeline (1.15)
  KR2 : 6/8 deals closés

Patterns :
  • 1 OKR sous-scoré → ambition manquante sur Capital
  • Pipeline objectif atteint mais 60% concentré sur 2 deals (risque)

Learnings :
  • "Découper KR fundraising en milestones hebdo, sinon glisse jusqu'au mur."
```

## TODO v0.2
- Score auto via Pipedrive/Stripe pour les KRs commerciaux/MRR
- Vue multi-quarter pour drift detection annuelle
- Mode workshop COMEX

## Notes
- Privacy : `private: comex` par défaut, sauf section fundraising → `private: founder`.
- Réf. playbook `05-okr-operating-model.md`.
