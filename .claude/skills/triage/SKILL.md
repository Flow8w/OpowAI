---
name: triage
description: Tri rapide de l'inbox email + chat — classifie en Do / Defer / Delegate / Drop, extrait les tâches éparses et propose des drafts pour les Do rapides.
status: implemented-v0.1
version: 0.1
category: Rituels quotidiens
required: [email]
optional: [chat]
---

# /triage

Vide l'inbox sans la lire entièrement. Cible : 15 min pour passer de 80+ emails à 0 tâche perdue.

## Pré-requis
- **Required** : email connecté.
- **Optional** : chat (Slack/Teams) — étend le triage aux mentions et DMs.

## Trigger
- Manuel : `/triage` ou `/triage --since "2 days"`
- Programmé : aucun en v0.1 (rituel choisi, pas imposé)
- Proactif : si > 50 unread emails et l'utilisateur évoque "noyé", suggérer le rituel

## Workflow

### 1. Fetch
Liste les threads unread depuis la dernière exécution (ou X jours en mode manuel).

### 2. Classification (4D)
Pour chaque thread :
- **Do** : <2 min de réponse → draft proposé inline
- **Defer** : tâche réelle, à mettre en backlog avec due date
- **Delegate** : à transférer (suggestion d'owner si team mappé)
- **Drop** : archive sans action (newsletters, FYI, notifications)

### 3. Extraction tâches
Pour les Defer + Delegate, crée des tasks dans `07-Tasks/Inbox.md` avec lien deeplink vers l'email.

### 4. Drafts pour les Do
Génère un draft Gmail (jamais envoyé) pour les Do, validation humaine obligatoire avant envoi.

### 5. Output
- Notification : "65 emails triés : 8 Do (drafts prêts), 12 Defer, 3 Delegate, 42 Drop"
- Log dans `System/triage-log.md` pour rétro analyse

## Outputs

- Drafts Gmail (jamais envoyés)
- Tasks dans `07-Tasks/Inbox.md`
- Archive auto pour les Drop (avec label `opowai-triaged`)
- Aucun envoi externe sans validation explicite

## Anti-patterns à éviter
- Auto-archive sans confirmation : un thread "Drop" reste accessible, JAMAIS supprimé.
- Drafter pour les threads complexes : si > 2 min de réponse, c'est un Defer, pas un Do.
- Drop par défaut les threads d'investisseurs/board : escalader systématiquement.

## Exemples concrets

```
📥 Triage du 2026-05-21 (65 unread) :

  Do (8 — drafts prêts dans Gmail) :
    • "Re: facture Stripe Q1" (réponse comptable factuelle)
    • "Re: dispo lundi 14h ?" (refus poli)
  Defer (12 — dans Inbox tasks) :
    • Préparer réponse RFP Acme (due 2026-05-26)
  Delegate (3 — suggestion d'owner) :
    • Refund customer X → @[membre équipe] (CS lead)
  Drop (42 — archivés avec label) :
    • LinkedIn notifs, newsletters, FYI internes
```

## TODO v0.2
- Apprentissage : si un sender est toujours Drop, suggérer une règle de filtrage permanente
- Sentiment + urgence sur les threads externes
- Intégration des DMs Slack avec même schéma 4D

## Notes
- Privacy : un thread investisseur classé Defer génère une tâche `private: founder`.
- Réf. playbook `12-ai-augmented-ops.md`.
