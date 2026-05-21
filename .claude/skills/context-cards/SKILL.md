---
name: context-cards
description: Génère des Context Cards modulaires (1 card = 1 sujet) à uploader dans Claude Cowork. Mise à jour granulaire, lisible context-aware par Cowork.
status: spec
version: 0.1
---

# /context-cards

Utilisé par `/sync-cowork` (ou manuel). Génère des cards modulaires plutôt qu'un seul gros bundle.

## Cards générées (v0.1)

| Card | Source vault | Update freq |
|------|--------------|-------------|
| `Card_Vision_Mission.md` | `01-Strategy/Vision_Mission.md` | Trimestriel |
| `Card_OKRs_Current_Quarter.md` | `01-Strategy/OKRs_*.md` | Hebdo |
| `Card_Industry_Truths.md` | `01-Strategy/Industry_Truths.md` | Mensuel |
| `Card_Org_Chart.md` | Génération depuis `03-People/Internal/` | Hebdo |
| `Card_ICP_Personas.md` | `02-Company/ICP_Personas.md` | Mensuel |
| `Card_Glossary.md` | `02-Company/Glossary.md` | Hebdo |
| `Card_Active_Projects.md` | `04-Projects/Company/` (status: active) | Hebdo |
| `Card_Team_Status.md` | `03-People/Internal/` + 1:1 récents | Hebdo |
| `Card_Product_Roadmap.md` | `04-Projects/Company/` + roadmap externe | Hebdo |

## Avantages

- **Mise à jour granulaire** : changer l'org chart sans toucher au glossaire
- **Cowork context-aware** : active la bonne card selon la conversation (RAG-like)
- **Pinning** : l'équipe peut épingler des cards en référence permanente
- **Versioning** : chaque card a un `last_updated` et un diff vs version précédente

## Format Card standard

```markdown
---
card: [name]
last_updated: YYYY-MM-DD
source: [vault path]
diff_since_last: [summary]
---

# 📇 [Card Title]

[Contenu de la card — concis, format adapté lecture par Claude]
```

## TODO v0.1
- [ ] Génération chaque card depuis sources
- [ ] Diff detection (vs dernière version sync)
- [ ] Bundle pour upload Cowork (ZIP ou folder)
