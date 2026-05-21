---
name: daily-review
description: Revue de fin de journée — bilan du Must/Should/Could, capture des learnings du jour, et préparation du carry-over pour demain.
status: implemented-v0.1
version: 0.1
category: Rituels quotidiens
required: []
optional: []
---

# /daily-review

Rituel de clôture de journée (5 min). Compare ce qui était prévu vs ce qui a vraiment été fait, capture les apprentissages, et prépare un démarrage propre pour demain.

## Pré-requis
- Aucun outil externe requis.
- Recommandé : avoir lancé `/daily-plan` le matin pour que la review soit comparative. Sans plan du matin, le skill bascule en mode "journal libre".

## Trigger
- Manuel : `/daily-review`
- Programmé : aucun trigger automatique en v0.1 (rituel volontaire, pas mécanique)
- Proactif : si dernier message après 18h et plan du matin existe, Claude propose le rituel

## Workflow

### 1. Re-lecture du daily-plan
Charge `07-Tasks/Daily/YYYY-MM-DD.md` et présente les Must/Should/Could.

### 2. Bilan par item
Pour chaque item, demande à l'utilisateur (3 options rapides) :
- ✅ done
- 🔄 carry-over (déplacé à demain ou cette semaine)
- ❌ dropped (et pourquoi en 1 ligne)

### 3. Capture des learnings
Question ouverte : "Un truc appris aujourd'hui qui mérite d'être gardé ?" Si oui → écrit dans `09-Resources/Learnings/YYYY-MM-DD.md` avec un tag thématique (sales / produit / team / soi).

### 4. Carry-over
Items marqués 🔄 sont automatiquement injectés dans `07-Tasks/Inbox.md` pour réinjection par le prochain `/daily-plan`.

### 5. Mood / énergie (optionnel)
1 ligne facultative pour tracker l'énergie. Alimente l'identité longue durée (`System/identity-model.md`).

## Outputs

- `07-Tasks/Daily/YYYY-MM-DD.md` mis à jour avec section "## Review" en bas
- `09-Resources/Learnings/YYYY-MM-DD.md` créé si learnings capturés
- `07-Tasks/Inbox.md` enrichi des carry-over
- Aucune action externe

## Anti-patterns à éviter
- Faire la review à la place de l'utilisateur : Claude pose les questions, c'est l'utilisateur qui répond.
- Lourdeur : 5 min max. Si la review dépasse, c'est trop fréquent ou trop riche.

## Exemples concrets

```
📋 Bilan du 2026-05-21 :
  ✅ Board slides finies
  🔄 Brief Lead Sales (carry-over → demain)
  ❌ Demo Acme (cancelled, à reprogrammer)

Learning : "Préparer les slides board la veille au soir réduit le stress du matin."
→ Capturé dans 09-Resources/Learnings/2026-05-21.md
```

## TODO v0.2
- Détection des patterns multi-jours (ex : "même tâche carry-over 3 fois → suggère breakdown")
- Intégration mood/énergie dans recommandations `/week-plan`

## Notes
- Le skill alimente `/week-review` (qui agrège les daily-reviews de la semaine).
- Réf. playbook `11-operating-cadence.md`.
