---
name: competitor-watch
description: Veille concurrentielle hebdo — scrape news, releases produit, pricing changes, hires sales/exec, et synthétise les signaux qui méritent attention.
status: implemented-v0.1
version: 0.1
category: Intelligence
required: []
optional: []
schedule: "Mon 08:00"
---

# /competitor-watch

Évite de découvrir les mouvements concurrents par les prospects en RDV.

## Pré-requis
- Aucun outil bloquant. Le skill utilise du scraping web stealth (`scrapling` MCP) + sources publiques.
- Pré-requis vault : `01-Strategy/Competitors.yaml` avec liste des concurrents à tracker.

## Trigger
- Manuel : `/competitor-watch` ou `/competitor-watch "Competitor X"`
- Programmé : lundi 8h
- Proactif : si un prospect mentionne un concurrent non tracké en RDV (via `/process-meetings`), suggère de l'ajouter

## Workflow

### 1. Charge la liste
Lit `01-Strategy/Competitors.yaml`. Format :
```yaml
competitors:
  - name: "Competitor X"
    domain: "competitorx.com"
    sources:
      - blog: "https://competitorx.com/blog"
      - changelog: "https://competitorx.com/changelog"
      - linkedin: "..."
    last_scraped: 2026-05-14
```

### 2. Scrape par concurrent
Pour chaque concurrent :
- Blog : derniers articles depuis last_scraped
- Pricing page : detect changes (diff vs snapshot précédent)
- Changelog : nouvelles features publiées
- LinkedIn (public) : nouveaux hires sales/exec
- ProductHunt / G2 : nouveaux reviews ou launches

### 3. Synthèse par concurrent
1 paragraphe (5 lignes max) par concurrent avec :
- Mouvement notable (si applicable, sinon "RAS")
- Signal d'analyse (positionnement, segment ciblé, etc.)
- Implication pour nous

### 4. Top signaux semaine
Agrégation : 3-5 signaux qui méritent action (recadrage messaging, alerte CS, prep deal en cours).

### 5. Output
Écrit `01-Strategy/Intel/Competitors/YYYY-WW.md` (privacy: comex).
Notification chat avec top signaux.

## Outputs

- `01-Strategy/Intel/Competitors/YYYY-WW.md`
- Snapshot pricing pages dans `01-Strategy/Intel/Competitors/snapshots/`
- Notification chat
- Aucune action externe

## Anti-patterns à éviter
- Veille pour la veille : sans implication actionable, le rapport est lu en diagonale et oublié.
- Surveiller 15 concurrents : 5 max. Au-delà = bruit.
- Ignorer les signaux faibles : un hire VP Sales chez un concurrent = mouvement go-to-market.

## Exemples concrets

```
👀 Competitor Watch — S21

Competitor X :
  • Nouvelle feature "Advanced reporting" (changelog 2026-05-19)
  • Hire : nouveau Head of Sales (ex-Salesforce Enterprise)
  → Signal : push vers enterprise. À surveiller sur deals > 100k€.

Competitor Y :
  • Pricing : ajout d'un plan "Starter" à 49€/mois (avant : 99€)
  → Signal : agressivité bas du marché. Anti-pattern pour nous ou opportunité ?

Top 3 signaux semaine :
  1. Competitor X enterprise push → briefer commerciaux (battle card update)
  2. Competitor Y starter plan → analyse cannibalisation ICP ?
  3. Competitor Z silence radio (3 sem sans publication) → ralentissement ?
```

## TODO v0.2
- Battle cards auto-générées par concurrent (intégration ICP + différentiateurs)
- Alerte temps réel sur mouvements critiques (hire C-level, M&A, levée)
- Sentiment analysis sur reviews G2/Capterra

## Notes
- Privacy : `private: comex`.
- Réf. playbook `13-gtm-foundations.md`.
- Utilise `scrapling` MCP pour les scrapes anti-bot.
