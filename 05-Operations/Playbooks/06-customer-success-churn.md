---
title: "Customer Success & Churn Playbook"
category: "Operations"
maturity: "preset"
sources_internal: []
last_updated: 2026-05-20
private: false
---

# Customer Success & Churn Playbook

## Quand utiliser ce playbook

Quand la base client dépasse 30-50 comptes et que le churn devient un sujet stratégique. Quand le NRR plafonne ou descend. Quand l'équipe CSM passe son temps à éteindre des feux au lieu de développer les comptes. Ce playbook s'adresse aux founders, CCO/COO et heads of Customer Success qui veulent transformer le post-vente d'un centre de coût réactif en moteur de croissance.

## Principes fondamentaux

1. **Le churn se joue dans les 90 premiers jours.** L'onboarding détermine 70% de la rétention à 12 mois. Tout effort de save ultérieur arrive trop tard.
2. **L'humain sur les moments critiques, le système partout ailleurs.** Le CSM doit se concentrer sur l'onboarding, les comptes à risque, et les comptes stratégiques. Le reste doit tourner sur du self-serve, du support et de l'automation.
3. **Mesurer la valeur, pas l'usage.** L'usage est un proxy faible : un compte peut beaucoup utiliser et churner quand même. La valeur réelle = atteinte d'un outcome client (revenu, économie, satisfaction).
4. **Le health score est un système d'alerte, pas un rapport.** Il sert à déclencher une action, pas à colorier un dashboard.
5. **Expansion > acquisition.** Augmenter le NRR de 95% à 115% a plus d'impact que doubler les leads.

## Étapes / Process

### Étape 1 — Mapper le cycle de vie client
Définir 6-8 étapes avec critères d'entrée/sortie, owner, KPI :
1. **Sale closed** → Bienvenue
2. **Onboarding (M0-M1)** : objectif = premier moment de valeur (TTFV)
3. **Adoption (M2-M6)** : routine installée, usage régulier
4. **Expansion (M6+)** : upsell, cross-sell, ajout de seats/modules
5. **Renewal (M11-M12)** : conversation contractuelle de renouvellement
6. **At-risk** : signaux faibles détectés → play de save activé
7. **Churn** : compte perdu, raison codifiée, apprentissage
8. **Win-back** : tentative de récupération 3-6 mois après churn

Chaque étape a un **owner** clair, des **critères de sortie explicites**, et **3-5 KPI max**.

### Étape 2 — Construire le health score
Combiner 4-6 signaux pondérés :
- **Usage** (fréquence, profondeur, derniers logins)
- **Engagement humain** (ouverture emails, réponse aux QBR, NPS)
- **Outcomes** (atteinte des objectifs client définis à l'onboarding)
- **Commercial** (paiement à date, demandes de discount, sentiment du sponsor)
- **Tickets support** (volume, sévérité, sentiment)

Output : score 0-100, code couleur (vert / jaune / rouge), trigger automatique pour le CSM si rouge ou si chute > 20 points.

### Étape 3 — Définir le modèle d'engagement
Segmenter les clients par valeur et complexité :
- **High-touch** (top 20% en revenu) : CSM dédié, QBR trimestriels, exec sponsor
- **Mid-touch** (60%) : CSM partagé, QBR semestriels, communication digitale enrichie
- **Tech-touch / Low-touch** (20% bottom) : entièrement digital, emails automatisés, communauté, KB

Règle : un CSM ne peut pas gérer > 30 comptes high-touch ou > 100 mid-touch.

### Étape 4 — Industrialiser l'onboarding
Programme structuré :
- **Kickoff** (J0-J7) : alignement objectifs client, plan de succès écrit, intro équipe
- **Setup technique** (J7-J21) : intégrations, formation initiale, première valeur visible
- **Validation premier outcome** (J21-J45) : un usage business concret atteint
- **Sortie d'onboarding** (J45-J60) : check formel, passage à la phase adoption

**Critère de sortie** : routine installée + premier outcome atteint + sponsor satisfait. Si l'un manque, le compte reste en onboarding (et alerte interne).

### Étape 5 — Animer la phase adoption
- **QBR (Quarterly Business Review)** pour les high-touch : revue d'usage, atteinte des objectifs, identification d'opportunités d'expansion.
- **Customer education** : webinars, certifications, communauté.
- **In-app guides** : nudges contextuels pour les features sous-utilisées.

### Étape 6 — Plays de save (compte at-risk)
Quand le health score passe au rouge :
- **J0** : CSM contacte le sponsor sous 48h, comprend la cause.
- **J3-J7** : plan de save écrit (action concrète, livrable, deadline).
- **J7-J30** : exécution du plan + monitoring quotidien.
- **J30** : verdict — sauvé (retour au vert), perdu (déclenchement procédure churn propre), ou conversion en compte renégocié (downgrade).

### Étape 7 — Codifier les churns
Pour chaque churn :
- Interview de sortie avec le sponsor (15-30 min).
- Codification de la cause (catégories standard : produit, prix, fit, account management, M&A...).
- Partage trimestriel des causes à Product + Sales + Marketing pour boucle d'amélioration.

### Étape 8 — Boucle d'expansion
- Identifier les comptes à signaux d'expansion (croissance usage, satisfaction haute, nouveaux use cases mentionnés).
- Trigger automatique au CSM pour proposer un upsell.
- Conversion claire : qui mène la conversation commerciale (CSM, AM, ou handoff vers Sales) ?

## Outils & Templates

- **Cycle de vie client canvas** : étapes, owners, KR, critères de sortie
- **Health score formula** : pondération par signal, seuils d'alerte
- **Plan de succès client** template (rempli au kickoff, revu trimestriellement)
- **QBR deck** template
- **Save play playbook** : checklist J0/J7/J30
- **Churn exit interview** script
- **Expansion trigger matrix** : signal → action → owner

## Anti-patterns à éviter

- **CSM = support premium** : le CSM finit par absorber tickets standards au lieu de développer le compte
- **Pas de critères de sortie d'onboarding** : les comptes restent en onboarding indéfiniment ou y sortent trop tôt
- **Health score qui ne déclenche rien** : un rapport coloré que personne n'utilise
- **Save play réactif uniquement après que le client annonce le churn** : trop tard
- **Pas de codification du churn** : on perd l'apprentissage à chaque départ
- **CSM compensé sur la rétention seule** : pas d'incitatif à l'expansion
- **Mêmes ressources pour tous les comptes** : on sur-investit sur les petits, on sous-sert les gros

## Métriques de succès

- **GRR (Gross Revenue Retention)** : > 90% (signe que la base de départ ne fuit pas)
- **NRR (Net Revenue Retention)** : > 110% (signe d'expansion réelle)
- **TTFV (Time To First Value)** : < 30 jours pour la majorité des segments
- **Churn rate** : annuel < 10% (volontaire) ; mensuel < 1% pour SaaS B2B
- **Onboarding completion rate** : > 90% des comptes sortent de l'onboarding selon le SLA
- **Expansion rate** : > 30% des comptes high-touch ont un upsell par an
- **NPS** : > 30 (industriel SaaS B2B)
- **CSM-to-account ratio** : adapté au segment (voir step 3)

## Pour aller plus loin

- Voir le playbook **Hiring & Onboarding** pour les profils CSM
- Voir le playbook **Pricing & Monetization** pour structurer expansion et upsell
- Voir le playbook **Process Documentation** pour industrialiser les SOP support et CSM
