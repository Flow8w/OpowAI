---
name: save-insight
description: Capture rapide d'un learning post-travail significatif — ad-hoc, ne demande pas d'attendre la review du soir. Route vers la bonne thématique automatiquement.
status: implemented-v0.1
version: 0.1
category: Rituels quotidiens
required: []
optional: []
---

# /save-insight

Permet de capturer un insight au moment où il survient, sans casser le flux. Plus rapide qu'écrire un fichier à la main.

## Pré-requis
- Aucun.

## Trigger
- Manuel : `/save-insight "Le faux 'oui' du prospect cache souvent un blocage organisationnel."`
- Proactif : Claude peut suggérer le skill après un travail significatif (résolution d'un blocage, finalisation d'un projet)

## Workflow

### 1. Capture brute
Si argument fourni, l'utiliser. Sinon, demander : "Quel est ton insight ?" (1-3 phrases max).

### 2. Tagging thématique
Claude classe l'insight dans une catégorie :
- sales / produit / team / ops / capital / personnel / strategy
Si ambigu, demande à l'utilisateur de choisir.

### 3. Enrichissement contextuel
- Ajoute date + contexte (meeting/projet en cours si détectable)
- Lie à un projet existant si pertinent (`04-Projects/`)

### 4. Écriture
Écrit dans `09-Resources/Insights/YYYY-MM-DD-slug.md` avec frontmatter (tag, source, project_link).

### 5. Suggestion SOP
Si l'insight ressemble à un pattern observé > 2 fois (lookup grep dans Insights), suggère : "Cet insight ressemble à [autre]. Construire un SOP ?"

## Outputs

- `09-Resources/Insights/YYYY-MM-DD-slug.md`
- Notification chat : "Insight capturé. Tag: sales. Reliable au projet 'Pipeline Q3'."

## Anti-patterns à éviter
- Capturer du bruit : un insight n'est pas une observation banale, c'est un apprentissage qu'on veut garder.
- Tag par défaut "personnel" pour tout : forcer une décision de routing.

## Exemples concrets

```
/save-insight "Quand un prospect demande à parler à un client référence avant la demo, c'est un signal positif fort — taux de close historique 78%."

→ Tag : sales
→ Linked project : "Sales playbook v2"
→ Fichier : 09-Resources/Insights/2026-05-21-prospect-reference-signal.md
```

## TODO v0.2
- Vector search sur les insights (déduplication, recherche sémantique)
- Push automatique vers SOP Notion via `/publish-sop` quand un insight devient mature

## Notes
- Réf. `/save-insight` est complémentaire à `/daily-review` (capture libre dans la journée vs capture structurée le soir).
- Privacy : par défaut `false`. Si insight stratégique → `comex`.
