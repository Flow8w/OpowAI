---
name: pipeline-monitor
description: Monitoring hebdo du pipeline CRM — alertes drift (deals stagnés, stages sautés, valeurs aberrantes), forecast par taux historiques, top movers / freezers.
status: implemented-v0.1
version: 0.1
category: Sales & pipeline
required: [crm]
optional: []
schedule: "Mon 09:00"
---

# /pipeline-monitor

Surveillance automatisée du pipeline. Détecte ce que l'humain ne voit plus à force de regarder.

## Pré-requis
- **Required** : CRM connecté avec stages configurés.

## Trigger
- Manuel : `/pipeline-monitor` ou `/pipeline-monitor --since "2 weeks"`
- Programmé : lundi 9h
- Proactif : si un deal critique (>10% du pipeline) ne bouge pas depuis 3 semaines, alerte

## Workflow

### 1. Fetch pipeline
Charge tous les deals open du CRM + 90 jours d'historique de transitions.

### 2. Calcul des indicateurs
- **Stage age** : temps moyen par stage vs benchmark interne
- **Stage skip detection** : deals qui sautent des stages (signal positif ou négatif selon contexte)
- **Drift score** : deals stagnés > 2x stage average duration
- **Top movers** : deals qui ont progressé cette semaine
- **Freezers** : deals dormants > 21 jours sans activité

### 3. Forecast
Calcule expected ARR par stage en utilisant les taux de conversion historiques (rolling 6 mois). Cible : 3 scénarios (commit / likely / upside).

### 4. Alertes drift
Génère liste priorisée :
- 🔴 Critique : deal > 50k€ ARR + freezer > 21j
- 🟠 Warning : skip de stage suspect (Discovery → Closed Won en 3 jours sur deal > 100k€)
- 🟡 Info : volume stage Discovery en baisse de 30%

### 5. Output
Écrit `01-Strategy/Pipeline/YYYY-WW-monitor.md` (privacy: comex) + notification chat avec top 5 alertes.

## Outputs

- `01-Strategy/Pipeline/YYYY-WW-monitor.md`
- Notification chat synthétique
- Aucun write CRM

## Anti-patterns à éviter
- Alerter sur tout : top 5 max en chat. Le reste dans le fichier.
- Forecast trop précis : 3 scénarios (commit/likely/upside), pas une valeur unique.
- Ignorer le contexte saisonnier : un Q4 a une dynamique différente d'un Q1.

## Exemples concrets

```
📈 Pipeline Monitor — S21

Forecast Q3 :
  Commit  : 850k€
  Likely  : 1.2M€  ← cible 1M€ ✅
  Upside  : 1.7M€

Top alertes :
  🔴 Acme (180k€) stagné 28 jours en Negotiation
  🔴 Beta (120k€) skip Discovery → Proposal (vérifier qualif)
  🟠 Volume Discovery -35% vs S20 (signal lead-gen ?)

Top movers :
  ✅ Gamma : Discovery → Proposal (12 jours, sain)
  ✅ Delta : Proposal → Closed Won (45k€)
```

## TODO v0.2
- Pattern detection cross-deals (ex : 80% des deals lost ont stagnés au stage X)
- Recommandation play par deal en alerte (réf. playbook `07-sales-pipeline.md`)
- Vue COMEX hebdo agrégée

## Notes
- Privacy : `private: comex`.
- Réf. playbook `07-sales-pipeline.md` (stages, forecast par taux historiques).
- Alimente `/friday-close` et `/board-prep`.
