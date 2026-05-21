---
title: "Product Roadmap Playbook"
category: "Product"
maturity: "preset"
sources_internal: []
last_updated: 2026-05-20
private: false
---

# Product Roadmap Playbook

## Quand utiliser ce playbook

Quand le backlog dépasse 200 items et que personne ne sait par où commencer. Quand les stakeholders pressent pour ajouter leurs features et que la roadmap devient un document politique plutôt qu'un outil de décision. Quand l'équipe produit livre mais que l'impact business ne suit pas. Ce playbook s'adresse aux CPO, Heads of Product, fondateurs et engineering leads qui veulent structurer une roadmap qui éclaire les décisions plutôt que de les contraindre.

## Principes fondamentaux

1. **Une roadmap est un pari sur l'impact, pas un planning de livraison.** Le découpage en Now/Next/Later force à raisonner par horizons d'incertitude.
2. **Prioriser, c'est dire non.** Une roadmap qui contient tout ce que tout le monde demande n'est pas une roadmap. C'est un backlog déguisé.
3. **L'outcome précède l'output.** Ne jamais inscrire « livrer la feature X » sans le résultat business attendu (rétention, conversion, ARR…).
4. **La dette technique est une ligne de roadmap, pas un sujet ingé caché.** 15-25% de la bande passante doit y être consacrée explicitement.
5. **La roadmap est un objet de communication.** Une roadmap interne peut être détaillée. La version externe (clients, board) doit être thématique, sans dates précises au-delà du trimestre courant.

## Étapes / Process

### Étape 1 — Cadrer les inputs
- **Stratégie & OKR entreprise** : la roadmap incarne la stratégie produit, pas l'inverse.
- **Voix client** : entretiens, NPS, support tickets, win/loss analysis.
- **Data produit** : funnel, rétention, feature usage, churn drivers.
- **Voix interne** : sales (deals perdus pour cause de gap), success (churn drivers), tech (dette).
- Centraliser dans un opportunity backlog : description, source, segment ICP touché, valeur estimée, effort estimé.

### Étape 2 — Choisir un framework de priorisation
- **RICE** (Reach × Impact × Confidence ÷ Effort) : équilibre les variables, bon pour la priorisation standard.
- **MoSCoW** (Must / Should / Could / Won't) : utile pour cadrer une release ou un trimestre.
- **Opportunity Solution Tree** : relie outcome → opportunity → solution. Évite de prioriser des solutions sans problème clair.
- **Kano model** : pour différencier les features must-have, performance et delighters.
- Choisir UN framework principal et s'y tenir. Mélanger les frameworks crée du bruit.

### Étape 3 — Structurer Now / Next / Later
- **Now** (trimestre courant) : engagement ferme, dates précises, ressources allouées.
- **Next** (1-2 trimestres) : priorités probables, dépendances identifiées, mais pas de date ferme.
- **Later** (au-delà) : thèmes stratégiques, pas de scope précis. Sert à communiquer la vision sans verrouiller l'exécution.
- Une bonne roadmap a 60% Now, 30% Next, 10% Later — pas l'inverse.

### Étape 4 — Allouer la bande passante
- **Bandes typiques** : 60% nouveaux produits/features, 20% optimisation/scale, 15% dette technique, 5% explorations/innovations.
- Adapter selon le stade : early-stage = plus de nouveaux features, scale-up = plus de scale et dette.
- Si la dette explose, geler 1-2 sprints pour rembourser avant que le coût devienne exponentiel.

### Étape 5 — Gérer les dépendances
- Mapper les dépendances entre équipes produit, design, ingé, GTM, juridique.
- Si une feature dépend de 3+ équipes, c'est un programme — pas un sprint. Nominer un program manager.
- Tenir un dependency log à jour : owner, statut, risque de slippage.

### Étape 6 — Communiquer la roadmap
- **En interne** : version détaillée par épopée/feature, mise à jour mensuelle, accessible à tous.
- **Aux clients / sales** : version thématique, focus sur les outcomes par segment.
- **Au board** : 1 slide, 3-5 thèmes par trimestre, alignés aux OKR business.
- Une roadmap pas communiquée n'existe pas.

### Étape 7 — Revue & réajustement
- **Mensuel** : check d'avancement, slippages, signal d'alerte sur les dépendances.
- **Trimestriel** : revue formelle, re-priorisation, ajustement Now/Next/Later.
- **Pivot signal** : si > 30% des items planifiés sont déplacés ou abandonnés, la stratégie produit doit être ré-examinée, pas juste la roadmap.

## Outils & Templates

- **RICE scoring sheet** : reach × impact × confidence / effort
- **Now/Next/Later canvas** : structure visuelle par horizon
- **Opportunity Solution Tree template** : outcome → opportunity → solution
- **Dependency log** : owner × dépendance × statut × risque
- **Roadmap external view** : version thématique sans dates précises

## Anti-patterns à éviter

- **Roadmap = liste de features promises au sales** : la dette de promesse devient ingérable
- **Pas de slot pour la dette technique** : la vélocité finit par s'effondrer
- **Roadmap figée 12 mois** : aucune capacité à intégrer le learning produit
- **Trop de Now, pas de Later** : pas de vision stratégique, exécution court-termiste
- **Pas de critère d'outcome** : on livre des features qui ne bougent aucune métrique
- **Pas de version externe** : sales improvise, clients se sentent trahis
- **Frameworks empilés** : RICE + MoSCoW + Kano + ICE → personne ne sait plus comment décider

## Métriques de succès

- **Outcome attainment rate** : % des features livrées qui ont atteint l'outcome cible
- **Roadmap accuracy** : % des items Now livrés dans le trimestre (cible 70-85% — au-delà = sandbagging)
- **Dette technique ratio** : 15-25% de la bande passante effectivement allouée
- **Time-to-decision** : délai entre identification d'une opportunité et inscription Now/Next
- **Stakeholder NPS roadmap** : satisfaction qualitative trimestrielle des stakeholders sur la roadmap

## Pour aller plus loin

- Voir le playbook **Customer Discovery & Validation** pour alimenter le backlog d'opportunités
- Voir le playbook **OKR Operating Model** pour aligner roadmap et OKR
- Voir le playbook **Operating Cadence** pour ritualiser les revues mensuelles/trimestrielles
- Voir le playbook **GTM Foundations** pour aligner roadmap et go-to-market
