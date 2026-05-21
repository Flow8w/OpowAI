---
name: meeting-prep
description: Préparation J-1 des meetings du lendemain — contexte attendees, historique récent, objectifs probables, questions à poser. Générique (interne + externe).
status: implemented-v0.1
version: 0.1
category: Rituels quotidiens
required: [calendar]
optional: [crm, email]
---

# /meeting-prep

Génère un brief de prep pour chaque meeting de demain. Pour le sales-focused, voir `/prep-meeting` qui est plus riche en CRM.

## Pré-requis
- **Required** : calendar — sinon impossible de scanner les meetings.
- **Optional** : CRM (enrichit pour meetings externes), email (historique de threads).

## Trigger
- Manuel : `/meeting-prep` (tous les meetings demain) ou `/meeting-prep "Acme review"` (ciblé)
- Programmé : en v0.2 (J-1 18h). En v0.1, le rituel est lancé en fin de daily-review si proposé.

## Workflow

### 1. Scan calendar J+1
Liste les meetings du lendemain, filtre les blocages personnels (lunch, focus blocks).

### 2. Pour chaque meeting, classer
- **Interne** (attendees du domaine company) → contexte 1:1, projets en cours, dernière conversation
- **Externe** (autres domaines) → bascule sur `/prep-meeting` si CRM connecté, sinon contexte minimal
- **Récurrent** (>3 occurrences passées) → résumé de la dernière itération

### 3. Construction du brief
Pour chaque meeting :
- Attendees + rôle (lookup `03-People/`)
- Objectif probable (inféré titre + historique)
- 3 questions à poser
- Décisions attendues
- Lien vers les notes de la dernière édition (si récurrent)

### 4. Output
Écrit `06-Meetings/Prep/YYYY-MM-DD-prep.md` consolidé (toutes les preps du jour).

### 5. Notification
Synthèse en chat : "5 meetings demain, 2 critiques (board, demo Acme). Prep complète disponible."

## Outputs

- `06-Meetings/Prep/YYYY-MM-DD-prep.md`
- Aucune action externe en v0.1

## Anti-patterns à éviter
- Brief verbeux : 5 min max de lecture par meeting, sinon l'utilisateur ne lira pas.
- Inventer du contexte : si l'historique est vide, le dire explicitement plutôt que d'extrapoler.

## Exemples concrets

```
🤝 Prep meeting demain — 1:1 [un membre du COMEX] (10h)

Contexte :
- Dernière 1:1 il y a 7 jours : a évoqué blocage sur l'API checkout
- Projet en cours : refonte tunnel paiement (en retard 2 semaines)
- Mood last meeting : tendu

Questions à poser :
1. Où en est le blocage API checkout depuis ?
2. As-tu besoin d'arbitrage côté priorisation ?
3. Comment je peux te débloquer ?
```

## TODO v0.2
- Synthèse vidéo/audio (Loom 2 min) pour les preps importantes
- Push automatique vers Notion pour les meetings COMEX

## Notes
- Privacy : si meeting board ou fundraising → brief en `private: founder`, jamais sync ailleurs.
- Réf. playbooks `08-team-rituals.md` (1:1), `04-board-investor-comms.md` (board).
