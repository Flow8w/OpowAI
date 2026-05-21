---
name: sync-cowork
description: Synchronise le contexte entreprise du vault vers Claude Cowork (filtré privacy). Programmable hebdo. En v0.1 local, v0.2 GitHub Actions.
status: spec
version: 0.1
---

# /sync-cowork

Pousse le contexte non-privé du vault vers le projet Claude Cowork "Company Context".

## Trigger
- Manuel : `/sync-cowork`
- Programmé v0.1 : hook cron local (dimanche 22h)
- Programmé v0.2 : GitHub Action `.github/workflows/sync-cowork.yml`

## Workflow

1. **Scan vault** — parcours tous les `.md` avec frontmatter
2. **Filtre privacy** :
   - Exclut `private: founder`
   - Inclut `private: comex` et `private: false` (ou absent)
3. **Génère Context Cards modulaires** (cf. `/context-cards`) :
   - `Card_Vision_Mission.md`
   - `Card_OKRs_Current_Quarter.md`
   - `Card_Org_Chart.md`
   - `Card_ICP_Personas.md`
   - `Card_Glossary.md`
   - `Card_Active_Projects.md` (depuis `04-Projects/Company/`)
   - `Card_Team_Status.md` (depuis `03-People/Internal/`)
4. **Upload Cowork** :
   - v0.1 : copy/paste assisté (génère le bundle, l'utilisateur upload)
   - v0.2 : via API Anthropic projects (si dispo) ou playwright sur Cowork
5. **Log** : append à `System/sync-cowork.log` (date, fichiers, diff size)

## Filter rules (privacy)

```yaml
exclude_patterns:
  - "04-Projects/Private/**"
  - "01-Strategy/Fundraising/**"
  - "03-People/Board_Investors/**"
  - "06-Meetings/Board/**"
  - "*private:founder*"  # frontmatter check

include_patterns:
  - "01-Strategy/Vision_Mission.md"
  - "01-Strategy/OKRs_*.md"
  - "02-Company/**"
  - "03-People/Internal/**"
  - "04-Projects/Company/**"
  - "05-Operations/SOPs/**"
  - "05-Operations/Playbooks/**"
```

Configurable via `System/cowork-sync.yaml`.

## Conflict resolution

Si fichier modifié côté Cowork (par un membre du COMEX) :
- Détecter via `/reverse-sync` (v0.2)
- Proposer merge dans le vault
- L'utilisateur valide

## TODO v0.1
- [ ] Implémentation scan + filtre
- [ ] Génération Context Cards
- [ ] Bundle upload assisté
- [ ] Doc de l'opération manuelle Cowork (capture/paste)
