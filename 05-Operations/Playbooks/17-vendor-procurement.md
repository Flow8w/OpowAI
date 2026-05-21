---
title: "Vendor & Procurement Playbook"
category: "Operations"
maturity: "preset"
sources_internal: []
last_updated: 2026-05-20
private: false
---

# Vendor & Procurement Playbook

## Quand utiliser ce playbook

Quand la stack SaaS dépasse 50 outils et que personne ne sait plus qui paie quoi, quand les contrats se renouvellent en silence à la hausse, quand une dépendance vendor critique fait peser un risque sur l'activité. Quand l'équipe finance commence à perdre la traçabilité des engagements. Ce playbook s'adresse aux COO, CFO et Heads of Operations qui veulent structurer le procurement et limiter le SaaS sprawl sans transformer l'achat en frein bureaucratique.

## Principes fondamentaux

1. **Tout achat récurrent est un engagement long.** Un SaaS payé annuellement = 3-5 ans de coût total à anticiper.
2. **Le bon vendor au bon stade.** Un outil enterprise sur une startup Seed = sur-spec. Un outil grand public sur une scale-up Series B = sous-spec.
3. **Centralisation contrôlée, décentralisation guidée.** Centraliser tous les achats freine l'agilité. Décentraliser sans cadre crée le sprawl. La bonne réponse : seuils + catalogue.
4. **Le coût total dépasse le prix de licence.** Implémentation, formation, intégration, exit cost. Le TCO sur 3 ans est la bonne unité.
5. **Le renouvellement automatique est une rente déguisée.** Sans process de revue avant renewal, l'entreprise paie pour de l'inutile.

## Étapes / Process

### Étape 1 — Cartographier la stack existante
- Lister tous les vendors actifs : nom, owner interne, coût annuel, date renewal, usage réel.
- Catégoriser : core (essentiel), important, optionnel, candidat à suppression.
- Identifier les redondances : 2 outils qui font la même chose = candidate à consolidation.

### Étape 2 — Définir une politique d'achat
- **Seuils d'approbation** : par exemple < 5k€/an = manager, 5-25k€ = head, > 25k€ = COMEX, > 100k€ = CEO/CFO.
- **Process simplifié** sous seuil bas : achat libre depuis un catalogue approuvé.
- **Process standard** au-dessus : business case + comparatif 2-3 options + validation.
- **Process complexe** pour les vendors critiques : RFP, due diligence sécurité, validation juridique.

### Étape 3 — Sélectionner un nouveau vendor
- **Cadrer le besoin** : problème à résoudre, users impactés, intégrations requises, must-have vs nice-to-have.
- **Sourcer 3 options** minimum : leader marché, challenger, alternative open-source/no-name.
- **Évaluer** sur grille pondérée : fit fonctionnel, prix, sécurité, scalabilité, support, intégration, exit.
- **Pilote** : tester en conditions réelles avant signature (POC 30-60 jours).
- **Négocier** : remise sur engagement multi-an, lock du prix, clause de sortie en cas de pivot.

### Étape 4 — Due diligence vendor critique
- **Sécurité** : SOC 2, ISO 27001, GDPR compliance, data residency, sub-processors.
- **Financière** : santé financière du vendor (un vendor qui dépose le bilan = catastrophe).
- **Référence client** : parler à 2-3 clients existants de taille comparable.
- **Continuité** : que se passe-t-il si le vendor disparaît ? Export des données ? Plan de migration ?

### Étape 5 — Cadrer le contrat
- **Pricing** : prix locked, conditions d'augmentation, palliers d'usage.
- **Engagement** : durée minimale, conditions de sortie, préavis.
- **SLA** : niveau de service garanti, pénalités en cas de manquement.
- **Data ownership** : les données restent propriété du client, exportables à tout moment.
- **Audit rights** : possibilité d'auditer le vendor sur la sécurité, l'usage, la facturation.

### Étape 6 — Gérer les renouvellements
- **Calendrier centralisé** : alerte 90 jours avant chaque renewal critique.
- **Revue pré-renewal** : usage réel vs licences payées, satisfaction users, alternatives marché.
- **Renégociation systématique** sur les contrats > 10k€/an. Un vendor sans pression d'attrition augmente toujours.
- **Décision documentée** : continue / renegotiate / replace / cancel.

### Étape 7 — Off-boarding vendor
- **Décision argumentée** : raison du départ, alternative choisie, plan de migration.
- **Export des données** dans un format exploitable, vérifié AVANT résiliation.
- **Notification dans les délais** : préavis contractuel respecté pour éviter renouvellement tacite.
- **Audit de fin** : confirmation suppression données chez l'ancien vendor.

### Étape 8 — Vendor risk management
- **Vendor risk register** : pour chaque vendor critique, scorer risque (financier, sécurité, dépendance).
- **Plan de continuité** : pour les vendors irremplaçables, plan B documenté.
- **Revue annuelle** : update du risk register avec les leadership concernés.

## Outils & Templates

- **Stack inventory sheet** : vendor × catégorie × coût × owner × renewal date × usage
- **Vendor evaluation matrix** : critères pondérés (fonctionnel, prix, sécurité, support…)
- **RFP template** : besoins, contexte, critères, processus de sélection
- **Contract checklist** : clauses essentielles à vérifier avant signature
- **Vendor risk register** : risques par vendor, mitigations, owner
- **Renewal calendar** : alertes 90/60/30 jours avant chaque renewal

## Anti-patterns à éviter

- **Achat impulsif** sans business case (« on a vu une démo cool »)
- **Pas de pilote** : signature direct sur 3 ans → regret 6 mois plus tard
- **Renouvellement automatique** non challengé → augmentations annuelles silencieuses
- **Vendor unique critique** sans plan B : risque opérationnel majeur
- **Pas de centralisation** : 3 équipes utilisent 3 outils similaires sans le savoir
- **Tout centraliser** : procurement devient un goulot d'étranglement, les équipes contournent
- **Pas de vérification sécurité** : un vendor compromis = porte d'entrée vers vos données
- **Contrats signés sans clause de sortie** : verrouillage long et coûteux

## Métriques de succès

- **Coût total stack / employee** : benchmark interne mois sur mois
- **% de renewals renégociés** : > 70% des contrats > 10k€/an
- **Économies obtenues** : sur renewals (objectif 10-15% en moyenne)
- **Taux d'utilisation des licences** : > 80% (en dessous = sur-équipement)
- **Vendor risk score** : nombre de vendors à risque haut (cible : décroissant)
- **Time-to-procure** : délai entre besoin exprimé et vendor opérationnel
- **% de vendors avec due diligence sécurité à jour** : 100% pour les vendors critiques

## Pour aller plus loin

- Voir le playbook **Operating Cadence** pour ritualiser les revues vendor mensuelles
- Voir le playbook **OKR Operating Model** pour aligner procurement et objectifs business
- Voir le playbook **Crisis & Comms** pour gérer une défaillance vendor critique
- Voir le playbook **M&A Readiness** pour préparer la cartographie vendor en due diligence
