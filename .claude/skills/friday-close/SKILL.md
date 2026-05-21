---
name: friday-close
description: Rituel vendredi 16h — récap des RDV passés de la semaine (synthèse + relance no-shows) et prep des RDV de la semaine suivante. Le skill phare du pilotage pipeline.
status: implemented-v0.1
version: 0.1
category: Sales & pipeline
required: [crm, calendar]
optional: [chat, email]
schedule: "Fri 16:00"
---

# /friday-close

**Le rituel qui clôture la semaine commerciale et arme la suivante.** Vendredi 16h, OpowAI compile en une page : ce qui s'est passé en RDV cette semaine + ce qu'il faut préparer pour la semaine d'après.

Ce skill est conçu autour d'un usage concret : un founder/CEO qui veut, en 15 minutes le vendredi soir, savoir où il en est sur ses RDV et démarrer le lundi sans charge mentale.

## Pré-requis
- **Required** : CRM (Pipedrive, HubSpot, Salesforce, Attio…) + Calendar. Sans ces deux, le rituel ne peut pas tourner.
- **Optional** : transcript (Granola/Gong/Fireflies) pour des synthèses RDV plus riches, chat (Slack) pour pousser les relances aux bons owners, email pour récupérer les threads associés.

## Trigger
- Manuel : `/friday-close` ou `/friday-close --preview` (affiche sans écrire dans Notion)
- Programmé : vendredi 16h (cron local v0.1, GitHub Action v0.2)
- Proactif : si vendredi 16h+ et pas de run aujourd'hui, Claude propose

## Workflow

### 1. Scan calendar — semaine écoulée
Liste tous les meetings catégorisés "external" entre lundi 00h et vendredi 16h :
- Marqués `attended` si transcripts/notes existent OU si Claude a une trace dans `06-Meetings/External/`
- Marqués `no-show` sinon (à valider humainement — peut être un meeting interne mal classé)

### 2. Pour chaque RDV passé — mini-synthèse
Pour chaque RDV `attended`, Claude génère une synthèse 4 sections :
- **Positif** : signaux d'achat, validation use case, momentum
- **No-go / objections** : blocages, concurrence, freins budget
- **Next steps faites** : ce qui a déjà été envoyé/produit depuis le RDV
- **Next steps à faire** : ce qui reste à faire côté commercial (avec owner suggéré)

Source de la synthèse, par priorité :
1. Transcript Granola/Gong/Fireflies si dispo
2. Notes dans `06-Meetings/External/YYYY-MM-DD-*.md`
3. Stage CRM + activités CRM (calls, mails loggés) en fallback

### 3. Pour chaque no-show — liste de rappel
Pour les meetings sans trace :
- Vérifier statut CRM (reschedule prévu ?)
- Construire une liste "à relancer" avec template de relance préfilled
- Si chat connecté + owner identifié (ex : un membre équipe), push une notification Slack DM : "3 no-shows cette semaine à relancer — liste dans la page Vendredi 16h."
- **JAMAIS d'envoi d'email automatique.** La liste est un draft.

### 4. Scan calendar — semaine suivante
Liste les meetings external entre lundi 00h et vendredi 16h de la semaine N+1. Pour chaque, déclenche `/prep-meeting` en mode batch (light prep : context CRM + dernière interaction). Les preps individuelles plus profondes restent dispos à la demande.

### 5. Output — page "Vendredi 16h — Semaine [N]"
Deux sections claires :

```markdown
# Vendredi 16h — Semaine 21 (2026-05-18 → 2026-05-22)

## Section A — Récap RDV de la semaine

### Acme Corp — Mardi 14h (attended)
- Positif : validation use case, demande pricing détaillé
- No-go : concurrent évoqué (Competitor X), prix question
- Next steps faites : pricing envoyé jeudi
- Next steps à faire : appel CFO Acme la semaine prochaine [owner: Founder]

### Beta Co — Mercredi 11h (no-show)
- Relance à envoyer : draft prêt, à valider
- Owner : [membre équipe] (CS Lead)

[... autres RDV ...]

## Section B — Prep semaine 22

### Gamma Ltd — Lundi 10h
- Stage CRM : Discovery
- Dernière interaction : il y a 12 jours (relance demo)
- 3 questions à creuser : [...]

[... autres meetings ...]
```

Écriture :
- Page Notion sous "📚 OpowAI SOPs > Sales > Vendredi 16h" (timestamped)
- Copie markdown dans `06-Meetings/Sales/Friday-Close/YYYY-WW.md` (privacy: comex)

## Outputs

- Page Notion "Vendredi 16h — Semaine [N]" (validation humaine avant publication)
- Copie locale `06-Meetings/Sales/Friday-Close/YYYY-WW.md`
- Draft de relances no-shows (Gmail drafts si email connecté, JAMAIS envoyés)
- Slack DM owner si chat connecté
- Aucun write CRM en v0.1 (read-only)

## Anti-patterns à éviter
- Synthétiser un RDV sans source : si pas de transcript ni notes, dire "pas de trace, à compléter par le founder" plutôt que d'inventer.
- Confondre no-show et meeting non-trackable : un meeting board mal taggé `external` peut générer un faux no-show.
- Envoyer les relances en automatique : validation humaine systématique en v0.1.

## Exemples concrets

**Use case typique** : Founder SaaS B2B avec 8-12 RDV externes par semaine. Vendredi 16h, OpowAI compile la page. En 15 min, le founder valide les synthèses, ajuste 1-2 next steps, et confirme les relances no-shows. La page est publiée sur Notion accessible au COMEX. Le lundi matin, la section B sert de base de `/daily-plan`.

**ROI mesuré** : suppression de 30-45 min de saisie/synthèse manuelle, zéro RDV perdu de vue, démarrage de lundi clarifié.

## Réponses aux 2 questions le client

**Q1 : "Comment retrouver facilement le résultat des RDV préparés ?"**
→ Toutes les preps individuelles vivent dans `06-Meetings/External/YYYY-MM-DD-Compagnie.md`. La page Vendredi 16h consolide la lecture hebdo (récap section A). La recherche par compagnie/contact passe par `lookup_person` ou grep sur le dossier External.

**Q2 : "Dans quelle mesure les preps alimentent Pipedrive ?"**
→ En v0.1, **read-only** : OpowAI lit Pipedrive pour enrichir les preps, mais ne pousse rien. Aucun risque de polluer le CRM.
→ En v0.2 : **suggested writes** (Claude propose un update CRM, l'utilisateur valide en 1 clic — création note, mise à jour stage, push next steps).
→ En v0.3 : **auto-writes** sur les patterns à faible risque (logging d'activité, ajout de notes), avec audit trail complet.

## TODO v0.2
- Suggested writes Pipedrive (notes, stage update, next steps)
- Mode "team friday-close" pour COMEX commercial (chaque commercial sa page, agrégation Founder)
- Pattern detection multi-semaines (deal qui stagne 3 vendredis → escalade)
- Intégration native chat (DM aux owners avec card Slack)

## Notes
- Privacy : page Notion `private: comex`. Copie locale `private: comex` aussi.
- Réf. playbooks `07-sales-pipeline.md` (stages, mutual action plan), `11-operating-cadence.md` (rituel hebdo), `13-gtm-foundations.md` (motion sales).
- Le skill consomme la sortie de `/prep-meeting` pour la section B, et alimente `/coach-sales-self` en données pour l'auto-coaching.
