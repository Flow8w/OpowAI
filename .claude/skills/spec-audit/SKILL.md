---
name: spec-audit
description: Audit d'une spec produit — détecte ambiguïtés, edge cases manquants, dépendances implicites, et génère un brief devs prêt à attaquer.
status: implemented-v0.1
version: 0.1
category: Produit
required: [docs]
optional: [project]
---

# /spec-audit

Réduit la friction "spec floue → questions devs → re-spec → retard". Audit en 5 min ce qui sinon prend 3 allers-retours.

## Pré-requis
- **Required** : docs (Notion ou équivalent où vit la spec).
- **Optional** : project (pour cross-référencer avec tickets existants).

## Trigger
- Manuel : `/spec-audit "Refonte tunnel paiement"` (titre ou URL Notion)
- Proactif : si une page Notion taggée `spec` n'a pas été modifiée depuis 7 jours et a un statut "draft", suggère l'audit

## Workflow

### 1. Fetch spec
Charge la spec depuis Notion (par titre ou URL). Fallback : lire un fichier local si spec dans le vault.

### 2. Audit structuré
Claude analyse 7 dimensions :
- **Problème** : est-ce clair POURQUOI on fait ça ?
- **Success criteria** : mesurables ?
- **User flows** : couverts (happy path + edge cases) ?
- **Dépendances** : autres équipes/services explicités ?
- **Out of scope** : explicitement listé ?
- **Risques** : techniques + produit identifiés ?
- **Decision points** : qui décide quoi ?

### 3. Détection ambiguïtés
Liste les phrases vagues : "etc.", "à voir", "à confirmer", "comme avant", "user-friendly". Demande clarification.

### 4. Brief devs
Génère section "Pour les devs" avec :
- Acceptance criteria précis (Given/When/Then)
- Edge cases identifiés
- Questions ouvertes à trancher

### 5. Output
Écrit `04-Projects/Specs/Audits/YYYY-MM-DD-[slug].md` avec :
- Liste des gaps
- Brief devs
- Recommandation : "prête à shipper" / "à compléter (X points)" / "à reprendre"

## Outputs

- `04-Projects/Specs/Audits/YYYY-MM-DD-[slug].md`
- Suggestion de commentaires Notion (drafted, validation humaine avant push)
- Aucun write Notion automatique

## Anti-patterns à éviter
- Audit qui réécrit la spec : audit = signaler les gaps, pas combler à la place du PM.
- Verbal "to confirm" sans owner : si quelque chose est à confirmer, désigner QUI.
- Tolérance 0 sur "etc." : forcer l'explicit.

## Exemples concrets

```
🔎 Spec Audit — "Refonte tunnel paiement v2"

Gaps (4) :
  ⚠️ Success criteria flou ("améliorer conversion") → préciser cible chiffrée
  ⚠️ Edge case manquant : que se passe-t-il si paiement timeout ?
  ⚠️ Dépendance non explicitée : équipe billing à aligner ?
  ⚠️ "Etc." x 3 dans la section flow → expliciter

Brief devs (généré) :
  Given un user en tunnel checkout
  When il finalise son paiement
  Then [criteria précis manquant — à compléter avec PM]

Recommandation : à compléter (4 points), 1-2h de travail PM.
```

## TODO v0.2
- Détection des conflicts avec specs antérieures (overlap, contradictions)
- Mode review collaborative (commentaires structurés sur Notion)

## Notes
- Réf. playbooks `14-product-roadmap.md`, `02-customer-discovery.md`.
- Complémentaire à `/roadmap-sync` (vue d'ensemble vs deep audit d'une spec).
