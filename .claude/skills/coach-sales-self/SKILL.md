---
name: coach-sales-self
description: Auto-coaching basé sur les transcripts de tes propres calls — détecte tes patterns (objections mal traitées, questions oubliées, talk-listen ratio) et propose des plays correctifs.
status: implemented-v0.1
version: 0.1
category: Sales & pipeline
required: [crm]
optional: [transcript]
schedule: "Fri 15:30"
---

# /coach-sales-self

Coach personnel sur ta pratique sales. Lit tes calls (à toi, le founder) et te donne du feedback honnête.

## Pré-requis
- **Required** : CRM (pour identifier QUELS deals sont liés aux calls et leur outcome).
- **Optional** : transcript MCP. Sans transcripts, le skill bascule en mode "auto-coaching déclaratif" (5 questions guidées hebdo).

## Trigger
- Manuel : `/coach-sales-self` ou `/coach-sales-self --deal "Acme"`
- Programmé : vendredi 15h30 (juste avant `/friday-close`)
- Proactif : après un deal lost, propose une session post-mortem

## Workflow

### 1. Collecte
Récupère les transcripts de tes calls de la semaine (filter `host` ou `owner` = founder). Joint à chaque transcript le deal CRM associé (matching par compagnie + date proche).

### 2. Analyse par dimension
Pour chaque call :
- **Talk-listen ratio** (cible founder en discovery : 30/70)
- **Questions ouvertes vs fermées**
- **Objections** : identifiées, traitées, esquivées ?
- **Next steps** : explicites avec date ?
- **Discovery framework** appliqué (BANT / MEDDIC / SPICED selon préférence) ?

### 3. Pattern detection
Sur l'ensemble de la semaine :
- 3 forces (à renforcer)
- 3 axes (à corriger)
- 1 play prioritaire pour la semaine prochaine

### 4. Output
Écrit `08-Coaching/Self/YYYY-WW.md` (privacy: founder) avec :
- Synthèse hebdo
- Citations exactes des calls (anonymisées si partagé)
- Play prioritaire

### 5. Notification
"Auto-coaching semaine 21 prêt. Play prioritaire : poser 'pourquoi maintenant ?' plus tôt en discovery."

## Outputs

- `08-Coaching/Self/YYYY-WW.md` (privacy: founder)
- Aucune action externe

## Anti-patterns à éviter
- Coaching gratuit/positif : si tu as raté 4 next steps, le dire clairement, pas de sucre.
- Citations longues : 1-2 phrases max par exemple, sinon illisible.
- Comparer aux "best practices" abstraites : référencer le playbook `07-sales-pipeline.md` quand pertinent.

## Exemples concrets

```
🎓 Auto-coaching S21

Forces :
  • Excellent framing budget sur 3/4 calls
  • Discovery rigoureuse sur Acme (12 questions ouvertes)

Axes :
  • Talk ratio 55% sur Beta call (trop) — couper le pitch
  • 2/4 calls sans next step daté
  • Objection "trop cher" esquivée sur Gamma call (timestamp 18:32)

Play prioritaire S22 :
  → Poser "pourquoi maintenant ?" dans les 5 premières minutes de chaque discovery.
```

## TODO v0.2
- Tracking longitudinal des patterns (drift sur 12 semaines)
- A/B sur différentes formulations (suggérer alternatives)
- Mode "shadow" : Claude écoute en live et donne feedback post-call

## Notes
- Privacy : `private: founder` (matière sensible, jamais en COMEX sans choix explicite).
- Réf. playbooks `07-sales-pipeline.md`, `13-gtm-foundations.md`.
