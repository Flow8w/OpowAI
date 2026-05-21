---
name: daily-plan
description: Plan structuré du matin en 3 niveaux (Must / Should / Could) basé sur calendrier, tâches en cours, priorités hebdo et capacité réaliste. Réduit la friction de démarrage à zéro.
status: implemented-v0.1
version: 0.1
category: Rituels quotidiens
required: [calendar]
optional: [email, project, chat]
schedule: "Mon-Fri 08:00"
---

# /daily-plan

Génère le plan de la journée en moins de 60 secondes. Sortie par défaut : page markdown dans le vault + notification chat.

## Pré-requis
- **Required** : Calendar connecté — sans calendar, pas de plan fiable, le skill se met en `⏳ pending`.
- **Optional** : email (inbox stress), project (tickets en cours), chat (mentions et asks).

## Trigger
- Manuel : `/daily-plan` ou `/daily-plan --preview` (affiche sans écrire)
- Programmé : Mon-Fri 08:00 (cron local, cf. `.scripts/cron/opowai.cron`)
- Proactif : si premier message de la journée après 08:30 et pas de plan écrit, Claude suggère `/daily-plan`

## Workflow

### 1. Scan contextuel (parallèle)
- Calendar : meetings du jour avec attendees, durées, gaps disponibles
- Week_Priorities : top 3 priorités de la semaine en cours
- Tasks : tâches due aujourd'hui ou en retard
- Inbox (si email connecté) : asks reçues hier soir / ce matin
- Project (si connecté) : tickets assignés in-progress

### 2. Évaluation capacité
Calcule le temps de focus réel disponible : 24h - meetings - lunch - context-switch tax (15 min/transition).

### 3. Construction Must / Should / Could
- **Must** (1-3 items max) : ce qui ne peut pas glisser, lié à Week_Priorities ou un meeting critique
- **Should** (3-5 items) : ce qui avancerait la semaine si Must est rapide
- **Could** (libre) : opportunités si focus mode débloque du temps

### 4. Output
Écrit `07-Tasks/Daily/YYYY-MM-DD.md` avec frontmatter `private: false` (sauf si meeting board/COMEX → propage le privacy).

### 5. Notification
Push synthèse en chat : "📅 3 Must, 4 Should, 2h focus dispo entre 10h et 12h. Voir plan complet."

## Outputs

- `07-Tasks/Daily/YYYY-MM-DD.md` (créé ou écrasé si même jour)
- Notification chat avec lien vers le fichier
- Aucun envoi externe

## Anti-patterns à éviter
- Lister 15 tâches : si tout est prioritaire, rien ne l'est. Hard cap à 3 Must.
- Ignorer la capacité réelle : ne JAMAIS planifier > 75% du temps non-meeting.
- Réécrire le plan si l'utilisateur l'a édité à la main (vérifier `last_edited_by` dans le frontmatter).

## Exemples concrets

**Input** : Mardi, 4 meetings (board prep 9h, 1:1 Lead Sales 11h, demo client 14h, COMEX 16h), 2h libres entre 12h-14h.

**Output Must** :
1. Finir slides board (block 12h-13h)
2. Brief 1:1 Lead Sales sur churn Acme (15 min avant)
3. Debrief demo client → push next steps Pipedrive (block 13h-13h45)

## TODO v0.2
- Détection des conflits agenda (meetings overlapping)
- Suggestion de décalage pour libérer du focus mid-week
- Intégration énergie/chronotype (matins focus, après-midis meetings)

## Notes
- Le skill respecte les privacy rules : si une tâche provient d'un meeting `private: comex`, elle hérite du tag.
- Réf. playbook `11-operating-cadence.md` pour le contexte rituels.
