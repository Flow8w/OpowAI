---
name: health-score-builder
description: Workshop guidé pour construire un health score client custom — choix des signaux, pondération, seuils d'alerte, intégration tooling. Produit advisory ou interne CS.
status: implemented-v0.1
version: 0.1
category: Advisory
required: []
optional: [crm, analytics]
---

# /health-score-builder

Construit un health score actionnable, pas un score cosmétique. Approche : moins de signaux mais bien choisis.

## Pré-requis
- Aucun outil bloquant. Le skill marche en mode workshop déclaratif.
- **Optional** : CRM (signaux usage/activité), analytics (signaux produit) — pour intégration tooling au build.

## Trigger
- Manuel : `/health-score-builder` (interne) ou `/health-score-builder --client "Company X"` (advisory)
- Proactif : si `/operating-rhythm-audit` a flagué "pas de health score" en gap prioritaire, propose le workshop

## Workflow

### 1. Cadrage
Interview structuré :
- Quel est ton ICP ?
- Quels segments différenciés ? (Enterprise vs SMB peuvent avoir des scores différents)
- Combien de clients actifs ?
- Qu'est-ce qui DÉJÀ prédit le churn historiquement ?

### 2. Signaux candidats (3 catégories)
Propose une longue liste, l'utilisateur sélectionne 6-10 max :
- **Usage** : login fréquence, features adoption, volume données
- **Business** : MRR, expansion, croissance compte
- **Relationship** : NPS, tickets support, sentiment 1:1 CSM

### 3. Pondération
Pour chaque signal retenu : poids 1-5. Total = 100%. Force la priorisation.

### 4. Seuils d'alerte
3 zones :
- 🟢 Healthy (score > X)
- 🟡 Watch (X-Y)
- 🔴 At risk (< Y)

Pour chaque zone : action standard (no-op / check-in / save play).

### 5. Plan d'intégration
- Où le score vit (CRM custom field ? Spreadsheet ? Dashboard custom ?)
- Cadence recalcul (live / hebdo / mensuel)
- Qui le voit (CSM, Sales, Founder)
- Plays automatisés (alerte Slack si bascule de zone)

### 6. Output
- `01-Strategy/Customer_Success/Health_Score_v1.md` (mode self)
- `04-Projects/Advisory/[Client]/Health_Score_v1.md` (mode advisory)
- Template d'implementation pour le tooling cible

## Outputs

- Documentation health score complète
- Template d'implémentation (CRM custom fields, formules)
- Aucune action externe automatique

## Anti-patterns à éviter
- 20 signaux : impossible à maintenir, score qui ne bouge plus.
- Score sans action attachée : un score qui ne déclenche rien est inutile.
- Score "agrégé" sans transparence : le CSM doit voir POURQUOI un compte est rouge, pas juste le score final.

## Exemples concrets

```
❤️ Health Score Builder — Output

Signaux retenus (7) :
  Usage (50%) :
    • Login 30j (15%)
    • Adoption features clés 3/5 (20%)
    • Volume données vs t-30 (15%)
  Business (30%) :
    • Expansion 6 derniers mois (15%)
    • MRR vs cohorte (15%)
  Relationship (20%) :
    • NPS dernier (10%)
    • Sentiment last 1:1 CSM (10%)

Zones :
  🟢 Healthy : > 70 → no-op, simple check-in trimestriel
  🟡 Watch   : 40-70 → CSM action (call dans 14j), focus features non-adoptées
  🔴 At risk : < 40 → save play (escalade Founder, retention offer)

Implementation :
  Tooling : CRM custom field calculated weekly
  Visibilité : Slack #cs-alerts si bascule zone
```

## TODO v0.2
- Templates par industrie (SaaS B2B Enterprise, SMB, PLG)
- Calibration automatique (rétrofit sur historique churn pour pondérer)
- A/B sur seuils (mesurer prédictivité)

## Notes
- Réf. playbook `06-customer-success-churn.md`.
- Complémentaire à `/operating-rhythm-audit` (qui détecte que CS manque d'outils) et `/pipeline-monitor` (pour la partie pre-sales).
- Si advisory : livrable packageable en 1 atelier de 3-4h avec le client.
