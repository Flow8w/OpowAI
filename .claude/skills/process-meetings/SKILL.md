---
name: process-meetings
description: Traite les transcripts de meetings (Granola, Gong, Fireflies…) ou notes brutes — extrait tasks, met à jour pages personnes, route vers projets, alimente CRM.
status: implemented-v0.1
version: 0.1
category: Rituels quotidiens
required: []
optional: [transcript]
---

# /process-meetings

Boucle de post-meeting : transforme la matière brute en actions structurées dans le vault.

## Pré-requis
- Aucun outil bloquant. Sans transcripts connectés, le skill marche sur les notes manuelles déposées dans `00-Inbox/Meetings/`.
- **Optional** : transcript MCP (Granola le plus mainstream) — débloque le traitement automatique.

## Trigger
- Manuel : `/process-meetings` (traite tout l'inbox) ou `/process-meetings [filename]`
- Programmé : v0.2 (poll toutes les 30 min des sources transcripts)
- Proactif : si > 3 fichiers non traités dans `00-Inbox/Meetings/`, Claude suggère le run

## Workflow

### 1. Collecte
- Scan `00-Inbox/Meetings/` (notes manuelles)
- Si transcript MCP connecté : fetch les nouveaux transcripts depuis la dernière exécution

### 2. Pour chaque meeting
- Identifie titre, date, attendees
- Détecte le type (1:1 interne, sales call externe, COMEX, board…)
- Applique privacy rule appropriée (board → founder, COMEX → comex, sinon false)

### 3. Extraction structurée
Sépare en :
- **Tasks** (action items avec owner + due date si mentionné)
- **Decisions** (avec rationale)
- **Open questions** (à reprendre next meeting)
- **People context** (intel sur des attendees externes)

### 4. Routing
- Tasks → `07-Tasks/Inbox.md` avec lien vers le meeting
- Decisions → `09-Resources/Decisions.md` (decision log)
- People intel → update `03-People/Internal/` ou `External/`
- Meeting note finale → `06-Meetings/[Internal|External|Board|COMEX]/YYYY-MM-DD-titre.md`

### 5. Notification + validation
Synthèse : "Meeting Acme review traité : 4 tasks extraites, 1 decision, 2 personnes mises à jour. Confirmer ?" Validation humaine avant écriture définitive si > 5 modifications.

## Outputs

- Meeting note structurée dans `06-Meetings/`
- Tasks dans `07-Tasks/Inbox.md`
- People pages mises à jour
- Decisions dans le log
- Aucun push CRM automatique en v0.1 (suggestion uniquement)

## Anti-patterns à éviter
- Hallucination de tasks : si l'attendee a dit "on devrait regarder X", c'est une open question, pas un commitment.
- Mélanger les privacy tiers : un meeting board ne doit JAMAIS générer des tasks publiques avec son nom.
- Réécraser une meeting note existante : append si update, pas overwrite.

## Exemples concrets

Input : transcript Granola "1:1 [un membre du COMEX] 2026-05-21" de 30 min.

Output :
- `06-Meetings/Internal/2026-05-21-1-1-[un membre du COMEX].md` (privacy: false)
- 2 tasks dans Inbox : "Décider archi cache checkout ([un membre du COMEX], 2026-05-28)", "Arbitrer entre Redis et Postgres pour sessions"
- 1 decision : "On part sur Redis pour la session checkout"
- [un membre du COMEX].md mis à jour : ajout du meeting + contexte projet checkout

## TODO v0.2
- Push automatique des tasks vers project mgmt (Linear/Jira) avec validation par batch
- Détection de blockers récurrents (même topic 3 fois → escalade)
- Sentiment analysis sur 1:1 (signaux de désengagement)

## Notes
- Réf. playbooks `08-team-rituals.md` (1:1), `07-sales-pipeline.md` (sales calls).
- Le skill alimente `/coach-sales-self` et `/coach-team-member` qui consomment les transcripts traités.
