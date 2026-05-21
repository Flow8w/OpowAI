---
name: coach-team-member
description: Coaching d'un membre de l'équipe sales basé sur ses transcripts récurrents — feedback structuré pour 1:1, plan de développement, suivi multi-semaines.
status: implemented-v0.1
version: 0.1
category: Sales & pipeline
required: [crm, transcript]
optional: [chat]
---

# /coach-team-member

Outil de coaching pour un manager qui supervise des commerciaux. Génère un debrief utilisable en 1:1.

## Pré-requis
- **Required** : CRM (outcomes deals) + transcript (matière analysée).
- **Optional** : chat (push du brief en DM au coaché si convenu).

## Trigger
- Manuel : `/coach-team-member "Marie"` (nom du commercial)
- Programmé : aucun par défaut (rituel manager, lié au 1:1)
- Proactif : avant un 1:1 commercial planifié, propose le run

## Workflow

### 1. Sélection coaché
Lookup du commercial dans `03-People/Internal/`. Vérifie qu'il est tagué `role: sales` ou équivalent.

### 2. Collecte transcripts
Filtre les transcripts où le coaché est host/owner depuis la dernière exécution (ou window paramétrable).

### 3. Analyse par dimension (mêmes critères que /coach-sales-self)
- Talk-listen ratio
- Questions ouvertes/fermées
- Traitement des objections
- Next steps
- Discovery framework

### 4. Construction debrief 1:1
Structure SBI (Situation - Behavior - Impact) :
- 2 wins concrets avec citation
- 2 axes concrets avec citation + impact business
- 1 play à expérimenter sur les 2 prochaines semaines

### 5. Output
Écrit `08-Coaching/Team/[Firstname]/YYYY-WW.md` (privacy: comex) + suggestion de push vers le coaché si chat connecté + accord préalable.

## Outputs

- `08-Coaching/Team/[Firstname]/YYYY-WW.md`
- Suggestion DM Slack/Teams (drafted, jamais envoyé sans validation)
- Aucune action externe automatique

## Anti-patterns à éviter
- Coaching dans le dos : le commercial DOIT savoir que ses calls sont analysés (consent layer).
- Critique sans citation : SBI = exemple précis, pas généralité.
- Sauter le play : un debrief sans expérimentation à mener est cosmétique.

## Exemples concrets

```
🎓 Coaching Marie — S21

Wins :
  • Excellent discovery sur Acme call (12 questions ouvertes, talk 35%)
  • Push objection "trop cher" → reframing valeur sur Beta call (timestamp 22:15)

Axes :
  • 3/5 calls sans next step daté → impact : 2 deals stagnés
  • Pas de qualif budget sur Gamma → impact : effort sur deal non bankable

Play S22-S23 :
  → Imposer "date next step" dans les 5 dernières minutes de chaque call.
```

## TODO v0.2
- Vue manager : agrégation multi-coachés, comparaison patterns
- Suivi longitudinal du play (a-t-il marché ?)
- Mode "review collaborative" : Claude propose, manager + coaché commentent

## Notes
- Privacy : `private: comex`. Le coaché a accès à son propre dossier.
- Consent : la première analyse d'un nouveau coaché demande validation explicite manager + commercial.
- Réf. playbooks `07-sales-pipeline.md`, `08-team-rituals.md`.
