---
name: draft-support-reply
description: Génère des brouillons de réponses au support client à partir d'un SOP de réponse, avec validation humaine systématique avant envoi. Use case P0 le client [l’entreprise].
status: spec
version: 0.1
---

# /draft-support-reply

Aide le founder/COMEX à traiter les emails support client : drafts générés, validés humainement, jamais envoyés sans approbation.

**ROI le client [l’entreprise]** : ~5h/mois économisées.

## Pré-requis
- Gmail MCP connecté
- SOP source : `05-Operations/SOPs/SOP_Support_Triage.md` (à créer lors du setup)

## Trigger
- Manuel : `/draft-support-reply` — Claude liste les tickets non répondus
- Manuel ciblé : `/draft-support-reply [thread_id]`
- Programmé v0.2 : 2x/jour via Action

## Workflow

1. **Fetch** — liste les threads Gmail dans `label:support` ou avec mots-clés "support", "help", "bug" non répondus depuis >24h
2. **Classifie** chaque ticket :
   - Bug technique
   - Question produit
   - Demande commerciale
   - Plainte / churn risk
   - Documentation/onboarding
3. **Génère draft** selon le SOP de réponse :
   - Ton aligné voix de marque
   - Réponse structurée (acknowledgment / réponse / next step)
   - Liens docs/articles pertinents auto-injectés
   - Signature founder
4. **Crée un Gmail draft** (jamais envoyé)
5. **Notifie** : "8 drafts prêts à relire, [lien Gmail drafts]"
6. **Track** : log dans `System/support-replies.log` (thread_id, classified, drafted_at)

## SOP de référence (à créer)

`05-Operations/SOPs/SOP_Support_Triage.md` :

```markdown
---
private: false
mature: true
---

# SOP — Support Customer Triage

## Classification
[5 catégories ci-dessus]

## Ton
- Empathique mais factuel
- Pas de blabla, on va à la solution
- Première personne (je) — pas "nous"

## Templates par catégorie
[Templates de réponse pour chaque cas]

## Escalade
- Si churn risk → ping founder direct
- Si bug critique → créer issue Linear/Jira auto
```

## Validation humaine

**Aucun envoi automatique en v0.1**. L'utilisateur :
1. Reçoit notification "drafts prêts"
2. Ouvre Gmail drafts
3. Relit, ajuste, envoie manuellement

En v0.2, option `--auto-send` pour les catégories à faible risque (documentation, FAQ), après score de confiance >0.9.

## TODO v0.1
- [ ] Gmail MCP : list draft threads, create_draft
- [ ] Création SOP_Support_Triage.md template
- [ ] Logique de classification (LLM)
- [ ] Auto-fetch docs/articles depuis Notion/Drive pour enrichir
- [ ] Logging
