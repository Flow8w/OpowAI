---
name: exec-summary
description: Synthèse exec hebdo investisseurs — format 3 wins / 3 challenges / 3 asks. Le rituel qui maintient les investisseurs warm entre deux boards.
status: implemented-v0.1
version: 0.1
category: Stratégie & capital
required: [crm]
optional: [analytics]
schedule: "Fri 17:00"
---

# /exec-summary

Génère le draft de l'update hebdo investisseurs. Format court (1 page), lisible en 2 min.

## Pré-requis
- **Required** : CRM (KPIs deal/ARR).
- **Optional** : analytics (data précise MRR/churn).

## Trigger
- Manuel : `/exec-summary`
- Programmé : vendredi 17h (juste après `/friday-close`)
- Proactif : si vendredi 17h+ et exec summary hebdo pratiqué (frontmatter `executive_update_cadence: weekly`)

## Workflow

### 1. Recharge update précédent
Lit le dernier exec-summary pour consistency narrative (KPIs mêmes définitions, suivi des asks).

### 2. Fetch data semaine
- Deals signed cette semaine (CRM)
- Deals lost cette semaine (raisons synthétisées)
- Pipeline movement (net new + closed)
- MRR / NRR si analytics dispo
- Hires/departures

### 3. Structure 3-3-3
**Wins (3)** :
- 1-2 lignes par win avec data
- Pas plus de 3 même si semaine exceptionnelle

**Challenges (3)** :
- Honnêteté > spin (un investisseur a vu pire)
- Action en cours pour chaque

**Asks (3)** :
- Précis, actionnable
- Intros, intros, intros (le plus haut levier)

### 4. Draft
Écrit `06-Meetings/Investors/Weekly/YYYY-WW.md` (privacy: founder).
Format markdown court (max 30 lignes).

### 5. Validation + envoi
Notification founder : "Exec summary prêt. Relire avant envoi via Gmail/[outil habituel]."
**Aucun envoi automatique.** Le founder relit, ajuste, copie-colle dans son canal habituel.

## Outputs

- `06-Meetings/Investors/Weekly/YYYY-WW.md` (privacy: founder)
- Notification founder
- Aucun envoi externe

## Anti-patterns à éviter
- Sucre : si la semaine a été merdique, le dire. La crédibilité se construit sur 50 semaines.
- 6 asks : 3 max. Au-delà, dilution = aucun ask retenu.
- Changer la métrique principale chaque semaine : si tu tracks ARR, garde ARR. Pas de cherry-picking.

## Exemples concrets

```
📊 Exec Summary — S21

**Wins**
1. Acme deal signé : 180k€ ARR (biggest to date)
2. NRR 118% confirmé sur cohorte Q1 2026
3. Head of CS : 3 candidats finalistes, décision la semaine prochaine

**Challenges**
1. Churn $ semaine +35k€ (2 départs : Beta, Gamma — raison : roadmap)
2. Pipeline Discovery -30% (lead gen à investiguer)
3. Slip roadmap : feature X décalée de 4 semaines (impact sur 2 deals)

**Asks**
1. Intros 5 prospects ICP Series B (cible : sourcing pipeline)
2. Connexion 2 candidats Head of CS si réseau (profil ex-Salesforce)
3. Avis stratégique sur churn drivers (call 30 min cette semaine ?)
```

## TODO v0.2
- Envoi automatique optionnel (après validation humaine en 1 clic)
- Suivi des asks : "ask de la semaine X a-t-elle été honorée ?"
- Mode mensuel pour les investisseurs cadence longue

## Notes
- Privacy : `private: founder` strict.
- Réf. playbook `04-board-investor-comms.md` (cadence update mensuel/hebdo, structure).
- Alimente `/board-prep` (les exec summaries hebdo sont la matière brute du board trimestriel).
