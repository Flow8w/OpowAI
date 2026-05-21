---
name: week-plan
description: Planification hebdo le dimanche soir ou lundi matin — top 3 priorités stratégiques, allocation focus blocks, anticipation des frictions calendar.
status: implemented-v0.1
version: 0.1
category: Rituels hebdo
required: [calendar]
optional: [crm, project]
---

# /week-plan

Pose le cadre de la semaine : 3 priorités max alignées sur quarter goals + identification des fenêtres de focus.

## Pré-requis
- **Required** : calendar — sans visibilité agenda, pas de plan crédible.
- **Optional** : CRM (deals à pousser cette semaine), project (sprint en cours).

## Trigger
- Manuel : `/week-plan`
- Programmé : aucun en v0.1 (rituel volontaire). Recommandé dimanche 20h ou lundi 8h.
- Proactif : si lundi 9h et pas de Week_Priorities mis à jour, Claude propose

## Workflow

### 1. Recharge contexte
- Quarter_Goals actuels (`01-Strategy/Quarter_Goals.md`)
- Week_Review de la semaine précédente (carry-over identifiés)
- Calendar de la semaine à venir (densité, blocages)

### 2. Diagnostic capacité
Calcule heures de focus disponibles vs heures meetings. Alerte si > 60% en meetings.

### 3. Proposition Top 3
Claude propose 3 priorités stratégiques avec rationale (lien à quarter goals). Utilisateur valide ou modifie.

### 4. Allocation focus blocks
Identifie 2-4 créneaux > 90 min dans la semaine et suggère un objectif par bloc.

### 5. Output
Écrit `02-Strategy/Week_Priorities.md` (overwritten chaque semaine, archive précédente dans `10-Archives/Week_Priorities/YYYY-WW.md`).

## Outputs

- `02-Strategy/Week_Priorities.md` (current week)
- Archive de la semaine précédente
- Notification synthétique en chat

## Anti-patterns à éviter
- 7 priorités : si tout est P0, rien ne l'est. Hard limit 3.
- Re-planifier le carry-over à l'identique : si une priorité a slippé 2 semaines, c'est un signal (à breakdown ou drop).
- Ignorer la densité meetings : un lundi à 80% meetings ne peut pas porter 3 Must.

## Exemples concrets

```
📆 Week_Priorities — Semaine 21 (2026-05-18 → 2026-05-24)

Top 3 :
1. Finaliser deck board (board le 28/05) → lien à QG "Capital readiness"
2. Closer Acme deal (signé ou churn cette semaine) → lien à QG "ARR 1M€"
3. Recruter Head of CS (shortlist 3 candidats) → lien à QG "Team scale"

Focus blocks identifiés :
- Mardi 14h-17h : deck board (3h libres)
- Jeudi 9h-12h : prep entretiens CS (3h libres)
```

## TODO v0.2
- Détection automatique des conflits entre priorités et calendar (ex : priorité = deck board, mais 0 focus dispo)
- Intégration mood/énergie depuis daily-reviews
- Suggestion de meetings à canceller / déplacer pour libérer focus

## Notes
- Le skill consomme l'output de `/week-review` et `/quarter-plan`.
- Réf. playbooks `05-okr-operating-model.md`, `11-operating-cadence.md`.
