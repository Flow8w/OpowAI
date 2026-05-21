---
name: all-hands
description: Prépare le all-hands mensuel sur Notion avec template structuré (KPIs, marketing, sales, success, roadmap). Auto-fetch des chiffres et roadmap, validation humaine.
status: spec
version: 0.1
---

# /all-hands

Génère le draft du all-hands mensuel sur Notion.

## Trigger
- Manuel : `/all-hands` ou `/all-hands [YYYY-MM]`
- Programmé v0.2 : dernier vendredi du mois 14h via GitHub Action

## Workflow

### 1. Audit Notion + emplacement
- Liste les pages Notion racines candidates (workspace root, équipe, méta)
- Propose 3 emplacements pour la page : "All-Hands [Mois Année]"
- Demande confirmation

### 2. Crée la page avec le template

Source : `System/templates/allhands-template.md` (modifiable par l'utilisateur)

```markdown
# 🏢 All-Hands — [Mois Année]

**Date :** [Date du all-hands]
**Présentateur :** [Founder]
**Status :** 📝 Draft - à valider

---

## 📊 Chiffres clés du mois

| KPI | Valeur | vs M-1 | vs Target |
|-----|--------|--------|-----------|
| New MRR | [auto] | [auto] | [auto] |
| Newbies (nouveaux clients) | [auto] | [auto] | — |
| Total clients actifs | [auto] | [auto] | — |
| Churn $ | [auto] | [auto] | [auto] |
| Net Revenue Retention | [auto] | [auto] | — |
| Unit economics (LTV/CAC) | [auto/manuel] | [auto] | — |
| Cash runway | [manuel] | — | — |

## 📣 Marketing

- Campagnes du mois : [auto-fetch Notion/Drive marketing]
- Métriques acquisition : [auto-fetch Posthog/Amplitude]
- Top performer : [à compléter]
- Flop : [à compléter — ce qui n'a pas marché et pourquoi]

## 💼 Sales review

- Pipeline status : [auto-fetch CRM]
- Deals closed ce mois : [auto-fetch] (TCV : [montant])
- Deals lost ce mois : [auto-fetch] (Raisons : [synthèse])
- Top wins (narrative) : [Claude propose, founder valide]

## 🎓 Onboarding & Customer Success

- Nouveaux clients onboardés : [auto-fetch]
- Time-to-value moyen : [auto-fetch ou manuel]
- Churn count + $ : [auto-fetch]
- Health scores (si dispo) : [auto-fetch]
- Top tickets support : [synthèse semaine via /draft-support-reply data]

## 🛠️ Product roadmap

- **🟢 Shipped ce mois** : [auto-fetch Jira/Linear/Notion — status Done dans la période]
- **🟡 En cours** : [auto-fetch — status In Progress]
- **🔴 En retard** : [auto-fetch — status In Progress avec due date < aujourd'hui]
- Highlights produit (impact client) : [Claude propose]

## 🎯 Focus mois prochain

- Objectifs majeurs (depuis OKRs trimestre) : [Claude propose, founder valide]
- Risques identifiés : [Claude depuis /drift-detection]
- Décisions à acter : [manuel founder]

## 🙏 Shout-outs & remerciements

[À compléter manuellement par le founder]

---

## Q&A (live)

[Skill compagnon /all-hands-live ajoute les Q&A en temps réel ici]
```

### 3. Auto-fetch des chiffres
- Stripe / CRM : MRR, clients, churn $
- Posthog / Amplitude : acquisition, retention
- Jira / Linear / Notion : status roadmap projets
- Demande confirmation sur chaque catégorie auto-fetched avant publication

### 4. Notification
- Crée la page sur Notion en status "📝 Draft - à valider"
- Notifie founder (Slack DM ou email)
- Founder relit, ajuste, change status → "✅ Ready to present"

### 5. Archive
- Sauvegarde une copie markdown dans `06-Meetings/All-Hands/YYYY-MM.md`
- Permet rétro analyse multi-mois (évolution MRR sur 12 mois, etc.)

## Compagnon : `/all-hands-live`

Pendant le all-hands en direct, prend les Q&A en temps réel et les append à la section Q&A de la page Notion.

## TODO v0.1
- [ ] Template `System/templates/allhands-template.md`
- [ ] Auto-fetch Stripe MCP
- [ ] Auto-fetch Linear/Jira MCP
- [ ] Auto-fetch Notion roadmap (si présente)
- [ ] Création page Notion avec arborescence
- [ ] Archive markdown vault
