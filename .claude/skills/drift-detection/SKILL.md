---
name: drift-detection
description: Hook hebdo qui détecte les dérives dans le vault (OKR pas à jour, projet stale, person sans interaction, conflit OKR/projets) et propose corrections.
status: spec
version: 0.1
---

# /drift-detection

Garde le vault sain et à jour. Détecte ce qui pourrit silencieusement.

## Trigger
- Programmé : hook hebdo (vendredi 17h ou intégré au `/week-review`)
- Manuel : `/drift-detection`

## Detection rules

### 1. OKR pas mis à jour
- Scan `01-Strategy/OKRs_Current_Quarter.md`
- Vérifie `last_updated` frontmatter
- Si >3 semaines → alerte

### 2. Projet "actif" sans activité
- Scan `04-Projects/Company/` et `Private/`
- Vérifie status frontmatter `active`
- Cross-check git log : aucun commit affectant ce projet depuis 30 jours ?
- → propose archivage ou réactivation

### 3. Person page stale
- Scan `03-People/External/`
- Si dernière mention en meeting/email <6 mois et pas de tag `# Long-term contact`
- → propose archivage dans `10-Archives/People/`

### 4. Conflit OKR ↔ Projets
- Liste les OKRs du trimestre
- Liste les projets actifs
- Pour chaque projet, vérifie qu'il contribue à au moins 1 OKR
- Sinon → flag "projet sans rattachement OKR"

### 5. SOP candidat
- Scan workflows fréquemment mentionnés (cross-check `04-Projects/`, `06-Meetings/`, `07-Tasks/`)
- Si >3 mentions sur 30 jours et pas encore SOP → propose `/publish-sop`

### 6. People avec action items en retard
- Scan `07-Tasks/Tasks.md`
- Tasks ouvertes assignées à une personne, mentionnées dans son 1:1 le plus récent
- Si due date <2 semaines passée → flag

### 7. Frontmatter privacy manquant ou incohérent
- Scan dossiers sensibles (`Fundraising/`, `Board/`)
- Vérifie `private: founder`
- Si absent → propose correction

## Output

À la fin du scan, génère un rapport :

```markdown
# 🔍 Drift Detection — [Date]

## 🔴 Critical (à traiter cette semaine)
- [ ] OKRs trimestre pas update depuis [5 semaines] — voir `01-Strategy/OKRs_*.md`
- [ ] 2 fichiers `01-Strategy/Fundraising/` sans `private: founder` (leak risk Cowork)

## 🟡 Warning
- [ ] Projet "Refonte Pricing" déclaré actif, dernière modif 45 jours
- [ ] Person page Jean Dupont sans interaction depuis 8 mois → archiver ?
- [ ] Workflow "process onboarding client" mentionné 5x ce mois → SOP ?

## 🟢 Info
- [ ] 12 tasks ouvertes avec due date passée
```

L'utilisateur traite les items via `/week-review` ou directement.

## TODO v0.1
- [ ] Implémentation scan rules 1-7
- [ ] Hook hebdo (cron local v0.1, Action v0.2)
- [ ] Intégration `/week-review`
