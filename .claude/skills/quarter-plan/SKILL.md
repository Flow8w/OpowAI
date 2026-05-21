---
name: quarter-plan
description: Cadrage trimestre — 3-5 OKRs stratégiques alignés sur pillars, key results mesurables, cascade aux equipes COMEX.
status: implemented-v0.1
version: 0.1
category: Rituels trimestriels
required: []
optional: []
---

# /quarter-plan

Pose le cadre stratégique du trimestre. Sortie : OKR set publié pour le founder + COMEX.

## Pré-requis
- Aucun outil bloquant. Recommandé : `01-Strategy/Pillars.yaml` rempli, `01-Strategy/Quarter_Goals.md` du Q précédent (pour continuité).

## Trigger
- Manuel : `/quarter-plan`
- Programmé : aucun (rituel volontaire, planifié 1-2 semaines avant fin de quarter)
- Proactif : si on est dans les 2 dernières semaines du quarter et pas de plan Q+1, Claude suggère

## Workflow

### 1. Recharge stratégique
- Pillars (`01-Strategy/Pillars.yaml`)
- Quarter goals du Q précédent + résultat (lien à `/quarter-review`)
- Industry truths si présent
- Vision 12 mois si documentée

### 2. Brainstorm guidé
Claude propose 5-8 objectifs candidats avec rationale (pillar + impact attendu). Utilisateur sélectionne 3-5.

### 3. Key results
Pour chaque objectif retenu, Claude propose 2-4 key results MESURABLES (chiffré ou binaire). Refuse les KR vagues ("améliorer X").

### 4. Cascade
Suggère pour chaque OKR un owner COMEX (lecture `03-People/Internal/`). Bascule en private:comex.

### 5. Output
Écrit `01-Strategy/Quarter_Goals.md` (overwritten). Archive le Q précédent dans `10-Archives/Quarter_Goals/YYYY-QX.md`.

## Outputs

- `01-Strategy/Quarter_Goals.md` (frontmatter `private: comex`)
- Archive Q précédent
- Notification : "Q3 2026 défini : 4 OKRs, 14 KRs, owners assignés."

## Anti-patterns à éviter
- 8 OKRs : 3-5 max. Au-delà, l'org perd le focus.
- KR non mesurable : "Renforcer la culture" n'est pas un KR. "NPS interne > 8" l'est.
- Plan top-down sans validation COMEX : OpowAI propose, le founder décide, le COMEX ajuste les KRs de leur scope.

## Exemples concrets

```
🎯 Quarter_Goals Q3 2026

OKR 1 — Capital readiness (pillar: Capital)
  KR1 : Data room complète et auditée d'ici 2026-09-15
  KR2 : 15 first meetings investisseurs initiés
  KR3 : Term sheet en main d'ici 2026-12-31
  Owner : Founder

OKR 2 — Pipeline 2x ARR (pillar: Growth)
  KR1 : 2M€ pipeline qualifié end of quarter
  KR2 : 8 deals closed > 50k€ ARR
  Owner : Head of Sales
```

## TODO v0.2
- Connexion à Pipedrive pour KR pipeline auto-tracké
- Health check mensuel mid-quarter (suggestion d'ajustement)
- Mode workshop COMEX collaboratif

## Notes
- Privacy : `private: comex` par défaut. Si OKR fundraising → `private: founder`.
- Réf. playbook `05-okr-operating-model.md`.
