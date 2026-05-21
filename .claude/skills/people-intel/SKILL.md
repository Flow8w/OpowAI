---
name: people-intel
description: Enrichit automatiquement une person page externe (prospect, candidat, investisseur) avec LinkedIn, articles récents, connexions communes, historique d'interactions.
status: spec
version: 0.1
---

# /people-intel

Quand une personne externe est mentionnée (meeting prep, intro, nouveau contact), enrichit sa page.

## Trigger
- Manuel : `/people-intel [Firstname_Lastname]`
- Proactif : avant chaque meeting external dans le calendrier (J-1 à 18h)
- Au moment de créer une person page dans `03-People/External/` ou `Board_Investors/`

## Workflow

1. **Identifier la personne**
   - Nom, email, société (si déjà connus dans le vault)
   - Sinon, demande à l'utilisateur

2. **LinkedIn scrape** (via Scrapling MCP)
   - URL LinkedIn (auto-recherche ou demande)
   - Job history, current role, formation, posts récents

3. **Articles & mentions récentes**
   - Scrapling search : `"[Nom] [Société]" site:linkedin.com OR site:medium.com OR site:[entreprise].com`
   - Limite : 5 résultats max
   - Synthèse : 3 bullets sur ce qu'ils ont fait/dit récemment

4. **Connexions communes**
   - Cross-check Gmail signatures (qui a écrit à cette personne dans tes mails ?)
   - Cross-check signatures sur d'autres meeting notes
   - Liste : "Tu as 3 contacts communs : X, Y, Z"

5. **Historique d'interactions**
   - Recherche dans `06-Meetings/External/` mentions précédentes
   - Recherche dans Gmail threads avec cet email
   - Synthèse : "Vous avez échangé [N] fois, dernière fois le [date] sur [topic]"

6. **Update person page**
   - Ajoute section `## 🔍 Intel ([date])`
   - Format structuré, sources citées

## Output exemple

```markdown
## 🔍 Intel (2026-05-20)

**Source LinkedIn** : [url]
- Current : VP Sales chez [Société] depuis 18 mois
- Ex : Director Sales chez [Compétiteur] (2 ans)
- Formation : ESCP Europe
- Posts récents : focus sur outbound + sales enablement

**Articles & mentions** :
- [Article 1] : "[Quote]" (date)
- [Article 2] : participation panel sur [topic]

**Connexions communes** :
- Sarah Dupont (LinkedIn 2nd) — vous avez échangé en mars 2025
- Marc Leroy (ex-collègue cité dans son LinkedIn)

**Historique** :
- Vous avez échangé 3 fois entre 2024-09 et 2025-02
- Dernière interaction : meeting le 2025-02-14 sur [topic]
- Sentiment de la dernière interaction : positif, intéressé par OpowAI

**Angles d'attaque suggérés** :
- Référence ESCP (école commune si applicable)
- Lien avec son focus sales enablement → notre playbook AARRR
- Mentionner Sarah Dupont si pertinent
```

## Privacy
- Toujours `private: comex` ou `private: false` selon le contexte
- Si la personne est dans `Board_Investors/` → `private: founder`

## TODO v0.1
- [ ] Intégration Scrapling MCP
- [ ] Recherche connexions communes via Gmail
- [ ] Template intel section
- [ ] Auto-trigger calendar J-1
