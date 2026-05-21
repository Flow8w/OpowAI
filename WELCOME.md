# 👋 Bienvenue dans OpowAI

Hello, et bravo d'avoir franchi le pas. Tu viens d'installer **ton système d'exploitation personnel augmenté par l'IA**.

Avant qu'on attaque le setup, prends 3 minutes pour comprendre comment OpowAI fonctionne — ça change tout pour la suite.

---

## 🧭 Comment ça marche, simplement

OpowAI, c'est **trois choses qui se parlent** :

1. **Un dossier de fichiers Markdown sur ton ordi** — c'est ton cerveau externalisé. Stratégie, OKRs, gens, projets, meetings, playbooks. Tout est en texte simple, lisible à vie.
2. **Claude Code** — l'IA qui lit, écrit, organise ce dossier pour toi. Tu lui parles, il agit (avec ta validation).
3. **GitHub (privé) + Cowork + Notion** — pour que ça survive aux crashes, pour partager avec ton COMEX, pour publier vers ton équipe.

**Tu ne touches presque jamais aux fichiers directement.** Tu parles à Claude, il fait le boulot.

---

## 🌱 Comment OpowAI vit dans le temps

OpowAI n'est pas un outil que tu installes et que tu oublies. **C'est un système qui s'enrichit avec toi.**

Trois mécanismes le font évoluer :

### 1. Le rythme quotidien
- `/daily-plan` le matin — Claude te prépare ta journée à partir de ton calendrier, tes tâches, tes meetings.
- `/daily-review` le soir — Claude capture ce que tu as fait, les décisions, les apprentissages.

### 2. Le rythme hebdo & mensuel
- `/week-plan` / `/week-review` — Claude relit ta semaine, surface les patterns.
- `/all-hands` (mensuel) — Claude prépare ton all-hands avec les chiffres, la roadmap, le narratif.
- `/sync-cowork` (hebdo) — Claude pousse le contexte entreprise vers ton COMEX.

### 3. La maturation des process
Quand un workflow se répète assez pour être stabilisé, Claude te propose : *"Ce process est mûr, je crée un SOP Notion ?"* — et hop, il devient une page de référence pour toute la boîte.

**Plus tu utilises OpowAI, plus il devient précis sur ton entreprise, ton équipe, tes priorités.**

---

## ⚙️ Comment on l'améliore

Tu n'es pas seul à le faire évoluer. **Claude le fait pour toi** :

- **Drift detection** — chaque semaine, Claude détecte ce qui dérive (OKR pas mis à jour, projet déclaré actif mais sans activité, personne sans interaction depuis 6 mois) et te propose des corrections.
- **Proposition d'améliorations** — Claude te propose régulièrement des nouveaux skills, des nouveaux playbooks, des refactos de structure quand il voit un pattern récurrent.
- **Playbooks vivants** — les playbooks pré-injectés (10 templates éprouvés) se personnalisent au fil du temps avec tes propres apprentissages.

**Toi, tu peux :**
- Modifier les templates dans `System/templates/` (notamment `allhands-template.md` que tu vas adorer customiser)
- Ajouter tes propres playbooks dans `05-Operations/Playbooks/`
- Tagger les workflows mûrs avec `# Mature` pour déclencher leur transformation en SOP

---

## 🔒 Privacy — règle simple

Chaque fichier a un flag en haut (frontmatter) :

```yaml
---
private: founder    # Visible que par toi
private: comex      # Visible par ton COMEX via Cowork
private: false      # Visible par toute la boîte via Notion SOPs (défaut)
---
```

Les dossiers sensibles (`Fundraising/`, `Board_Investors/`, `04-Projects/Private/`) sont **automatiquement** `founder`. Tu n'as rien à faire.

---

## 🚀 Prêt ?

Lance la commande suivante :

```
/setup-opowai
```

Claude te pose 5 phases :
1. **Connecter tes outils** (Notion → Drive → Gmail → CRM → Jira/Linear → Analytics)
2. **Auto-discovery** — Claude scanne tes outils et propose un profil pré-rempli
3. **Confirmation** — tu corriges plutôt que tu écris (5x plus rapide)
4. **Playbooks** — sélection des playbooks pertinents pour ton stade
5. **Premier run** — Claude exécute `/daily-plan` pour valider que tout marche

**Durée totale : ~30 minutes.**

---

## ❤️ Une dernière chose

OpowAI est conçu pour **te faire gagner 5-15h/semaine** sur les tâches d'ops, de coordination, de prep. Mais c'est aussi un **partenaire de réflexion** : challenge tes idées avec lui, fais-le débattre, demande-lui de jouer l'avocat du diable.

Le meilleur usage d'OpowAI, ce n'est pas la productivité brute. C'est la **qualité de tes décisions**.

Bienvenue. On commence ?

→ `/setup-opowai`
