---
name: week-review
description: Revue hebdo le vendredi soir — bilan des 3 priorités, pattern detection sur la semaine, learnings, et prep mentale du week-end.
status: implemented-v0.1
version: 0.1
category: Rituels hebdo
required: []
optional: []
---

# /week-review

Clôture de semaine. Permet de raisonner sur la cadence et pas juste les tasks.

## Pré-requis
- Aucun. Le skill consomme les daily-reviews + Week_Priorities locaux.

## Trigger
- Manuel : `/week-review`
- Programmé : aucun en v0.1 (volontaire, vendredi soir ou samedi matin)
- Proactif : si vendredi 18h+ et pas de week-review, Claude suggère

## Workflow

### 1. Agrégation des daily-reviews
Charge les 5 daily-reviews de la semaine (lundi → vendredi) et extrait :
- Tasks complétées vs planifiées (ratio)
- Carry-over récurrents (signal)
- Learnings agrégés
- Mood/énergie si trackée

### 2. Bilan des Top 3
Pour chaque priorité de la semaine :
- ✅ done | 🔄 progress | ❌ slipped
- 1 ligne de rationale

### 3. Pattern detection
Claude lit la semaine et propose 2-3 observations :
- "3 carry-over sur 'prep board' → bloc dédié manquant"
- "Énergie en chute sur jeudi/vendredi → meetings trop denses après mercredi"
- "Aucun focus block > 90 min réalisé"

### 4. Capture learnings semaine
1-3 learnings de niveau "semaine" (différent du daily). Écrit dans `09-Resources/Weekly_Learnings/YYYY-WW.md`.

### 5. Archive + prep prochaine semaine
Archive `02-Strategy/Week_Priorities.md` vers `10-Archives/Week_Priorities/YYYY-WW.md`. Prépare le terrain pour `/week-plan` dimanche.

## Outputs

- `10-Archives/Week_Priorities/YYYY-WW.md` (archive)
- `09-Resources/Weekly_Learnings/YYYY-WW.md` (learnings)
- Notification chat avec synthèse

## Anti-patterns à éviter
- Cosmétique : la review n'a de valeur que si on regarde les patterns. Ne pas se contenter d'un "tout va bien".
- Fast review : si tu finis en < 5 min, tu as zappé l'étape pattern detection.

## Exemples concrets

```
🔁 Week_Review — S21 (2026-05-18 → 2026-05-24)

Top 3 :
  ✅ Deck board (fini jeudi)
  🔄 Acme deal (relance lundi)
  ❌ Recruit Head of CS (shortlist pas faite — manque temps)

Patterns détectés :
  • 3 carry-over sur "prep entretiens CS" → bloc dédié manquant
  • Mood en chute jeudi → 6 meetings + lunch annulé

Learnings :
  • "Bloquer 2h récurrentes pour le recrutement, sinon ça ne se fait pas."
```

## TODO v0.2
- Comparaison multi-semaines (drift score sur ratio done/planifié)
- Push automatique de learnings stables vers SOPs Notion via `/publish-sop`
- Suggestion d'ajustement Quarter_Goals si 3 semaines de slip

## Notes
- Réf. playbook `11-operating-cadence.md`.
- Le skill alimente `/quarter-review` qui agrège les week-reviews.
