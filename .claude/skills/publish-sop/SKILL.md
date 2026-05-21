---
name: publish-sop
description: Détecte les workflows matures et propose la création d'un SOP Notion structuré dans la page racine "📚 OpowAI SOPs". Arborescence auto-créée.
status: spec
version: 0.1
---

# /publish-sop

Transforme un workflow mature en SOP Notion canonique.

## Trigger
- Manuel : `/publish-sop [path-to-workflow.md]`
- Proactif : Claude détecte les workflows utilisés >3 fois sur 30 jours, ou taggés `# Mature`
- Premier run via `/setup-opowai` : crée la page racine

## Workflow premier run (création racine)

1. Notion search root pages
2. Propose 3 emplacements possibles pour la page racine
3. Demande confirmation utilisateur
4. Crée page **"📚 OpowAI SOPs & Playbooks"** avec arborescence :
   ```
   📚 OpowAI SOPs & Playbooks
   ├─ 🎯 Strategy
   ├─ 💰 Sales
   ├─ 🛠️ Product
   ├─ 🎓 People & Team
   ├─ 💼 Operations
   ├─ 📊 Finance & Capital
   └─ 🚨 Crisis & Comms
   ```
5. Sauvegarde `notion_root_page_id` dans `System/company-profile.yaml`

## Workflow création d'un SOP

1. Lit le workflow markdown source
2. Classifie automatiquement la catégorie (Strategy/Sales/Product/People/Operations/Finance/Crisis)
3. Génère structure SOP :
   ```markdown
   # SOP — [Titre]
   
   **Owner :** [Personne responsable]
   **Updated :** [Date]
   **Frequency :** [Daily / Weekly / Monthly / Ad-hoc]
   
   ## 🎯 Purpose
   ## 🚀 Trigger
   ## 📋 Steps
   ## 👥 RACI
   ## ⚠️ Exceptions & Edge Cases
   ## 📊 Success Metrics
   ## 🔗 Related
   ```
4. Demande validation utilisateur avant publication
5. Crée la page Notion sous la bonne sous-catégorie
6. Ajoute lien bidirectionnel : vault note `🔗 Notion: [URL]` ↔ Notion page `🔗 Source: [vault path]`
7. Append à `System/sop-index.yaml`

## Detection des workflows matures

Scan hebdo (via `/drift-detection`) :
- Fichiers `05-Operations/*.md` mentionnés >3x dans meeting notes/tasks/journals des 30 derniers jours
- Fichiers taggés `# Mature` manuellement
- Sortie : liste de candidats SOP avec score de maturité

## TODO v0.1
- [ ] Notion MCP authentifié read/write
- [ ] Logique de classification (LLM call ou keyword)
- [ ] Template SOP markdown
- [ ] Création arborescence Notion racine
- [ ] Bidirectional linking
