---
name: roadmap-sync
description: Sync hebdo Jira/Linear → Notion — extrait l'état roadmap (shipped/in-progress/late), aide priorisation, prépare la section roadmap du all-hands.
status: implemented-v0.1
version: 0.1
category: Produit
required: [project]
optional: [docs]
schedule: "Mon 09:00"
---

# /roadmap-sync

Pont entre le project management (où vivent les tickets) et la knowledge layer (où vit la roadmap visible).

## Pré-requis
- **Required** : project mgmt (Linear, Jira, Notion projects, Asana, ClickUp, Shortcut).
- **Optional** : docs (Notion) — pour publier la roadmap visible.

## Trigger
- Manuel : `/roadmap-sync`
- Programmé : lundi 9h
- Proactif : avant `/all-hands`, lance automatiquement

## Workflow

### 1. Fetch tickets
Récupère tous les tickets actifs (in-progress, ready, blocked) + tickets terminés la semaine passée.

### 2. Catégorisation
Classifie par :
- **🟢 Shipped** (status Done dans les 7 derniers jours)
- **🟡 In progress** (status active)
- **🔴 Late** (in progress avec due date dépassée)
- **⏸️ Blocked** (status blocked ou tag spécifique)

### 3. Priorisation insight
Claude lit la liste et signale :
- 2-3 tickets "in progress" depuis > 21 jours (signal de breakdown)
- Tickets late récurrents (même owner) → coaching opportunity
- Volume late vs target sprint

### 4. Génération vue roadmap
- Format Now / Next / Later (réf. playbook `14-product-roadmap.md`)
- Now = in progress + late
- Next = planifiés Q en cours
- Later = backlog Q+1

### 5. Output
- Markdown : `04-Projects/Roadmap/YYYY-WW-snapshot.md`
- Push Notion (si docs connecté) : update page "🗺️ Roadmap publique" sous "📚 OpowAI SOPs > Product"
- Validation humaine avant publication Notion

## Outputs

- `04-Projects/Roadmap/YYYY-WW-snapshot.md`
- Page Notion roadmap (drafted, validation humaine)
- Notification chat

## Anti-patterns à éviter
- Publier sur Notion sans validation : la roadmap publique a un impact perception interne fort.
- Mélanger Now et Next : Now doit être "réellement en cours cette semaine", pas une wishlist.
- Ignorer les blockers : un ticket blocked depuis 14 jours est un problème de priorisation, pas un état stable.

## Exemples concrets

```
🛠️ Roadmap Sync — S21

Shipped cette semaine (3) :
  ✅ Feature export CSV (12 jours)
  ✅ Refonte tunnel paiement v1 (45 jours)
  ✅ Bugfix critique webhook (3 jours)

In progress (8) — 2 alertes :
  🟡 API v2 (24j en cours → breakdown ?)
  🟡 Refonte dashboard (18j)
  ⚠️ Onboarding wizard (35j — owner: [un membre du COMEX], en retard 2 sem)

Late (2) :
  🔴 SSO entreprise (due 2026-05-15, 6j retard)
  🔴 Reporting custom (due 2026-05-18, 3j retard)
```

## TODO v0.2
- Détection auto des dépendances inter-tickets
- Connexion à `/all-hands` pour pré-remplir section roadmap
- Suggestion de breakdown sur tickets de > 3 sprints

## Notes
- Privacy : `private: false` pour la roadmap publique, `private: comex` pour les analyses internes.
- Réf. playbook `14-product-roadmap.md` (Now/Next/Later, frameworks priorisation).
- Alimente `/all-hands`.
