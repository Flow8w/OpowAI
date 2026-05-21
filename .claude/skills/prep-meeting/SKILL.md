---
name: prep-meeting
description: Prep meeting externe enrichi CRM — historique deal, dernière interaction, signaux récents, 3 questions à creuser, objectif probable. Plus profond que /meeting-prep générique.
status: implemented-v0.1
version: 0.1
category: Sales & pipeline
required: [calendar, crm]
optional: [email]
---

# /prep-meeting

Brief sales-focused pour un meeting externe. Conçu pour les founders et commerciaux qui veulent entrer en RDV armés.

## Pré-requis
- **Required** : calendar + CRM. Sans CRM, bascule sur `/meeting-prep` (générique).
- **Optional** : email (récupère thread d'échanges précédent), people-intel data.

## Trigger
- Manuel : `/prep-meeting "Acme review"` ou `/prep-meeting --tomorrow`
- Programmé : appelé en mode batch par `/friday-close` pour la semaine N+1
- Proactif : si meeting external dans < 24h sans prep faite, suggère

## Workflow

### 1. Identification deal/compte
- Match nom du meeting + attendees au compte CRM (fuzzy + email domain)
- Si match multiple, demande confirmation

### 2. Synthèse compte
- Stage CRM courant + montant
- Date entrée dans le pipeline + jours en stage courant
- Dernière activité loggée (date + type)
- Owner du deal

### 3. Synthèse interactions
- Dernière interaction email (si email connecté) — résumé 2 lignes
- Dernières notes de meeting (lookup `06-Meetings/External/`)
- Notes CRM récentes (3 dernières)

### 4. Signaux & contexte
- Si people-intel disponible : intel sur les attendees (rôle, récents changements, contexte boîte)
- Concurrents évoqués dans l'historique
- Objections récurrentes mentionnées

### 5. Output brief
3 sections :
- **Contexte** (5 lignes max)
- **Objectif probable de ce meeting** (1 ligne)
- **3 questions à creuser** (focus sur ce qui débloque le deal)
- **Anti-patterns** (ce qu'il ne faut PAS faire — ex : "ne pas ressortir le pricing avant d'avoir validé use case")

Écriture : `06-Meetings/External/YYYY-MM-DD-CompanyName-prep.md`.

## Outputs

- `06-Meetings/External/YYYY-MM-DD-CompanyName-prep.md`
- Notification chat avec lien
- Aucune action externe

## Anti-patterns à éviter
- Brief de 3 pages : 1 page max. Si on lit pas avant le meeting, c'est inutile.
- Questions trop "framework" : 3 questions précises au contexte du compte, pas génériques BANT.
- Oublier l'historique humain : si le contact a déjà dit non sur le prix, ne pas reposer la question frontalement.

## Exemples concrets

```
🤝 Prep — Acme Corp review (Mardi 14h)

Contexte :
  Stage : Negotiation (depuis 18 jours, avg = 12)
  Montant : 180k€ ARR
  Dernier contact : email vendredi (pricing détaillé envoyé)
  Owner : Founder

Objectif probable :
  → Décision sur option pricing A vs B + signature target end of month.

3 questions à creuser :
  1. "Qui d'autre doit valider côté Acme ?" (single-threaded risque)
  2. "Sur quoi vous comparez encore ?" (concurrent évoqué : Competitor X)
  3. "Quelle est la décision si on n'avance pas ce trimestre ?" (urgence)

Anti-patterns :
  ❌ Ne pas reproposer une remise (déjà discounté 12%)
  ❌ Ne pas évoquer la roadmap produit (a freezé Beta call précédent)
```

## TODO v0.2
- Suggested writes CRM (logger l'activité automatiquement après le meeting)
- Brief audio (Loom 2 min) pour les meetings critiques
- Détection des deals "single-threaded" et alerte

## Notes
- Privacy : `private: comex` (info commerciale sensible).
- Réf. playbooks `07-sales-pipeline.md`, `13-gtm-foundations.md`.
- Alimenté par `/people-intel` pour l'intel attendees.
