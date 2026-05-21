# Runbook — Premier setup OpowAI avec un client

> Document tactique pour Florian. À suivre minute par minute lors d'une session de premier setup. Premier usage : vendredi jour J avec [le client] ([l’entreprise]).

**Durée cible :** 3h30 (3h confortable, 4h max).
**Format :** sur place, en présentiel ou en visio écran partagé.

---

## ✅ Pré-vol — la veille (jeudi soir)

Vérifier sur **ta** machine avant de partir :

- [ ] `cd ~/opowai && git pull origin main` — tu es bien à jour
- [ ] `bin/opowai status` — moteur répond OK
- [ ] `python3 -m pytest .scripts/opowai/tests/ -v` — 6/6 passent
- [ ] Token GitHub Flow8w en main (au cas où tu dois ré-auth pendant la session)
- [ ] Compte Anthropic prêt si le client n'a pas Max 5x

Vérifier côté **le client** (par texto ou mail) avant 18h :

- [ ] Il a bien **upgrade Claude vers Max 5x** (100 €/mois)
- [ ] Il a **Python 3.11+** sur son Mac : `python3 --version`
- [ ] Il a **Git** installé : `git --version`
- [ ] Il a **Claude Code CLI** : `which claude`
- [ ] Il a accès admin à ses outils : **Notion, Pipedrive, Gmail, Calendar, Slack, Jira, Granola, Posthog (si dispo)**
- [ ] Tu l'as ajouté comme **collaborateur sur `Flow8w/OpowAI`** (Settings → Collaborators)
- [ ] Il a généré son **PAT GitHub** (Personal Access Token) pour cloner le repo privé
- [ ] La spec **scoring Lovable** qu'il voulait démontrer est récupérée (use case 5 de son mail)

Préparer le **livrable post-session** côté toi :

- [ ] Page Notion ou doc partagé "OpowAI — Setup [l’entreprise] — 2026-05-23" prête à recevoir le récap
- [ ] Plan de retex à 7 jours (lundi prochain) déjà calé dans ton calendrier

---

## ⏱️ Timeline de la session

| Bloc | Durée | Quoi |
|------|-------|------|
| 0. Accueil & contexte | 15 min | Cadrage, vérif prérequis live |
| 1. Install (terminal) | 15 min | `git clone` + `bash install.sh` |
| 2. Premier lancement | 10 min | `claude` puis `/setup-opowai` |
| 3. Phase -1 env prep | 10 min | Diagnostic, fixes automatiques |
| 4. Phase 0 priorisation | 15 min | 3 cas d'usage prioritaires |
| 5. Phase 1 connexion outils | 75 min | Boucle 10 thématiques |
| 6. Phase 2 auto-discovery | (parallèle phase 1) | Background |
| 7. Phase 3 confirmation | 15 min | Valider profil pré-rempli |
| 8. Phase 4 activation | 10 min | Skills + agents programmés |
| 9. Phase 5 premier run | 15 min | `/daily-plan` démo |
| 10. Wrap-up + Q&A | 20 min | Plan post-session |

**Total : 3h25**, avec 10-15 min de marge pour les imprévus.

---

## 🎬 BLOC 0 — Accueil & contexte (15 min)

**Objectif :** poser le cadre, créer la confiance, lever les ambiguïtés.

### Script

> "On va passer 3h30 ensemble. À la fin, ton OpowAI tourne. La règle d'or : tu ne touches pas au clavier pour les commandes — c'est moi qui guide. Mais tu décides toujours."

### À dire explicitement

1. **Tu es mon client zéro.** OpowAI évolue avec ton feedback. C'est normal qu'il y ait des accrocs.
2. **Aucun envoi externe sans validation.** Les drafts mail, les writes Notion, les updates Pipedrive — tu valides toujours avant.
3. **Tes données ne sortent pas de ton repo.** Le code OpowAI vient d'upstream. Tes meeting notes, OKRs, person pages restent dans ton repo privé.
4. **On peut quitter et reprendre.** Si on est interrompus, le système retient où on en était.

### Vérifications live

- Le client ouvre son terminal → `python3 --version` → `git --version` → `which claude`
- Si un de ces 3 manque : **STOP**, on installe avant. Le runbook s'arrête ici.
- Le client confirme son plan Claude Max 5x sur claude.ai/billing

### Trigger pour la suite

Quand les 3 prérequis sont validés et que vous êtes face au terminal du client, écran partagé : **on attaque le bloc 1**.

---

## 🎬 BLOC 1 — Install (15 min)

**Objectif :** OpowAI installé sur sa machine, environnement prêt.

### Commande 1 — Cloner le repo

Le client tape (ou tu lui dictes) :

```bash
git clone https://github.com/Flow8w/OpowAI.git ~/opowai
```

**Watchpoint** : si erreur `403` ou `authentication failed` → c'est le PAT GitHub. Le client le configure ainsi :

```bash
git config --global credential.helper osxkeychain
# Re-essaie le clone, il va demander username + password
# Username = son GitHub username
# Password = son PAT (pas son mot de passe GitHub)
```

### Commande 2 — Lancer l'installer

```bash
cd ~/opowai && bash install.sh
```

**Ce qui s'affiche** (à narrer) :

```
━━ Vérification des prérequis ━━
✓ Python 3.11.x
✓ Git 2.x
✓ claude (vX.X.X)

━━ Création de l'environnement Python ━━
▸ Création du virtualenv .venv ...
✓ Virtualenv créé
▸ Installation des dépendances Python (pyyaml, click)...
✓ Dépendances installées

━━ Permissions & configuration ━━
✓ bin/opowai exécutable
✓ Remote upstream configuré (= origin pour l'instant)

━━ Test du moteur OpowAI ━━
✓ Le moteur OpowAI répond correctement

━━ Installation terminée 🎉 ━━

Prochaines étapes :
  1.  cd /Users/[username]/opowai
  2.  claude
  3.  /setup-opowai
```

**Watchpoint** : si le test moteur échoue ("Le moteur OpowAI a renvoyé une erreur") → lance `bin/opowai status` manuellement, regarde l'erreur. Probable cause : Python trop ancien ou venv corrompu. Re-tente après `rm -rf .venv && bash install.sh`.

---

## 🎬 BLOC 2 — Premier lancement (10 min)

**Objectif :** Claude Code lit OpowAI, `/setup-opowai` se lance proprement.

### Commandes

```bash
claude
```

Une fois dans Claude Code, Le client tape :

```
/setup-opowai
```

### Ce qui doit se passer

Claude :
1. Lit `CLAUDE.md` (visible dans son contexte de démarrage)
2. Détecte que le vault est neuf (pas de `02-Company/Glossary.md`)
3. Lance `/setup-opowai` qui démarre par afficher `WELCOME.md` ou un résumé

**Watchpoint** : si Claude ne reconnaît pas `/setup-opowai` → vérifier que le SKILL.md existe : `ls ~/opowai/.claude/skills/setup-opowai/`. Si manquant, c'est que `git clone` a échoué partiellement. Re-cloner.

### Hand-off

À ce moment, **tu laisses Claude conduire**. Tu interviens juste pour :
- Reformuler les questions de Claude si le client bloque
- Confirmer les choix
- Décider en cas de doute le client

---

## 🎬 BLOC 3 — Phase -1 Environment prep (10 min)

**Objectif :** Claude diagnostique l'env du client et applique les fixes.

### Ce que Claude va faire (script attendu)

```
🔍 Diagnostic OpowAI
  ✅ Python 3.11.x
  ✅ Git 2.x
  ✅ Virtualenv .venv présent
  ✅ Dépendances (pyyaml, click)
  ✅ Remote origin configuré (Flow8w/OpowAI)
  ⏳ Remote upstream non configuré
  ⏳ Cron OpowAI non installé

📦 MCPs déjà configurés dans Claude Code : [peut être vide ou contenir Notion/Gmail si le client les a déjà]

Veux-tu que je corrige les ⏳ ?
```

### Ce que tu dis au client

> "Confirme `yes`. Claude va auto-configurer ce qui manque. C'est sa job."

### Watchpoint

Si Claude ne fait pas la phase -1 (anciennenne version du SKILL.md), lance manuellement :
```bash
bin/opowai status
git remote -v
```
Et configure manuellement le remote upstream si absent.

---

## 🎬 BLOC 4 — Phase 0 Priorisation (15 min)

**Objectif :** le client sélectionne ses 3 cas d'usage prioritaires.

### Ce que Claude présente

```
🎯 Parmi ces cas d'usage, lesquels te font le plus envie ?
(Sélectionne au moins 3.)

  □ 1. Pilotage du pipeline & prep RDV (rituel vendredi 16h)
  □ 2. Coaching sales (toi + équipe)
  □ 3. Drafts support client automatisés
  □ 4. Prep all-hands mensuel
  □ 5. Roadmap produit, specs & maquettes
  □ 6. Pilotage perso (daily, weekly, quarterly)
  □ 7. Board, exec summary, fundraising
  □ 8. Prep contacts externes
  □ 9. SOPs partagés, contexte COMEX
  □ 10. Diagnostic ops (advisory)
```

### Sa réponse attendue (depuis son mail)

D'après son mail, ses **priorités explicites** sont **1, 2, 3, 4, 5**. C'est 5, soit 2 de trop pour rentrer dans une démo claire. **Ton job : l'aider à choisir les 3 plus impactants.**

### Recommandation à pousser

Suggère : **1 (pipeline + vendredi 16h) + 3 (support) + 4 (all-hands)**. Justification :
- Le **1** est le rituel structurant qu'il a explicitement voulu
- Le **3** active la valeur immédiate (5h/mois économisées)
- Le **4** lui donne un livrable de visibilité interne fin de mois

Le **2** (coaching) on l'ajoute en option, le **5** (roadmap) sera traité en juin via `/spec-audit`.

### Trigger pour la suite

Phase 0 terminée. Claude écrit `selected_use_cases` dans `System/.setup-state.json`. **Bloc 5 commence.**

---

## 🎬 BLOC 5 — Phase 1 Connexion thématique (75 min — le plus long)

**Objectif :** connecter le maximum d'outils le client aux 10 thématiques.

### Ordre fixe attendu (à suivre)

| # | Thématique | Outil le client | Temps | Bloquant ? |
|---|-----------|----------------|-------|------------|
| 1 | CRM & Sales | **Pipedrive** | 15 min | 🔥 OUI — bloque friday-close, pipeline-monitor, board-prep |
| 2 | Email | **Gmail** | 10 min | 🔥 OUI — bloque draft-support-reply (P0 use case) |
| 3 | Calendar | **Google Calendar** | 5 min | 🔥 OUI — bloque friday-close, daily-plan, prep-meeting |
| 4 | Knowledge & docs | **Notion** | 10 min | 🔥 OUI — bloque all-hands, publish-sop |
| 5 | Communication chat | **Slack** | 10 min | 🟡 Améliore mais non bloquant |
| 6 | Project & Roadmap | **Jira** | 10 min | 🟡 Améliore all-hands roadmap section |
| 7 | Data & Analytics | **Posthog + Stripe ?** | 10 min | 🟡 Améliore all-hands KPIs |
| 8 | Transcript & recording | **Granola** | 5 min | 🟡 Améliore coach-sales-self |
| 9 | Code & Dev | **GitHub** | (skip ou rapide) | 🔵 Optionnel |
| 10 | Autre | (rien attendu) | skip | 🔵 |

### Le pattern pour chaque thématique (à répéter 8-10 fois)

1. **Claude présente** : description + name-dropping
2. **Tu confirmes** : "le client, ton outil pour ça c'est X"
3. **Le client choisit** dans Claude Code (ex: "pipedrive")
4. **Claude lance le flow de connexion** : ouvre une URL d'auth dans le navigateur
5. **le client autorise** dans son navigateur
6. **Claude confirme la connexion** + affiche ce qui se débloque
7. **Tu commentes** : "Tu vois — connexion Pipedrive débloque ton `friday-close` quand on aura Calendar"
8. On passe à la thématique suivante

### Watchpoints critiques

- **MCP Pipedrive n'existe peut-être pas** — vérifier en amont. Si pas dispo, prendre la voie "Autre / API" et configurer un connecteur custom plus tard.
- **Auth flow Notion** — Notion demande de sélectionner un workspace ET des pages. le client doit autoriser un workspace large ou un parent de la page racine qu'il veut.
- **Gmail OAuth** — peut demander Google Workspace admin si [l’entreprise] est sur Workspace. À anticiper.
- **Posthog/Stripe** — si pas dispo, **skip sans forcer**. Tu peux configurer ces APIs en juin.
- **Granola** — il y a un MCP officiel ? Si non, on saute en v0.1 et on configure manuellement après.

### Trigger pour la suite

À la fin du bloc 5, **au minimum** Pipedrive + Gmail + Calendar + Notion doivent être connectés. C'est le socle. Tout le reste est bonus.

---

## 🎬 BLOC 6 — Phase 2 Auto-discovery (en parallèle du bloc 5)

**Objectif :** Claude scanne les outils déjà connectés pendant que vous continuez la connexion.

### Pendant le bloc 5

Pendant la connexion de la **3ᵉ thématique**, Claude lance discreètement l'auto-discovery sur les 2 premières. Tu verras apparaître :

```
🔵 Auto-discovery en cours...
  ✅ Profil détecté ([le client], CEO [l’entreprise])
  ✅ COMEX détecté (3 personnes — [un membre du COMEX], [un autre membre du COMEX])
  🔵 Glossaire en cours (depuis Notion)
  🔵 ICP en cours (depuis Pipedrive)
```

**Tu n'arrêtes pas le bloc 5 pour ça.** L'auto-discovery se déroule en parallèle.

### Watchpoint

Si l'auto-discovery prend > 10 min, c'est qu'un MCP rame. Laisse tourner et continue les connexions. Si vraiment bloqué : `Ctrl+C` côté discovery, on passe en mode manuel à la phase 3.

---

## 🎬 BLOC 7 — Phase 3 Confirmation guidée (15 min)

**Objectif :** le client valide ou corrige le profil pré-rempli.

### Ce que Claude présente

```
✨ J'ai pré-rempli ton profil. Confirme ou corrige.

Toi
  Nom :     [le client]
  Rôle :    CEO
  Email :   [founder]@[entreprise].com

Ta boîte
  Nom :     [l’entreprise]
  Domaine : [entreprise].com
  Secteur : [inféré]
  Stade :   [inféré — Seed ?]
  Taille :  ~12 personnes

COMEX
  ✓ [membre 1]
  ✓ [membre 2]
  ✓ [membre 3]

Pillars stratégiques (défaut)
  • Growth · Product · Team · Operations · Capital

Privacy rules (défaut)
  • Fundraising/, Board/, Projets Privés → private:founder
  • COMEX meetings, OKRs → private:comex
  • Tout le reste → public
```

### Ton rôle ici

- **Pousse le client à confirmer rapidement** — ne pas perdre 30 min à débattre du libellé "secteur". Le YAML reste éditable plus tard.
- **Valide les Pillars par défaut** sauf s'il en a d'autres en tête (Growth/Product/Team/Ops/Capital marche très bien pour son stade).
- **Confirme les privacy rules par défaut**. Ne touche surtout pas en v0.1 — c'est sensible et il pourra affiner plus tard.

### Trigger pour la suite

Claude écrit dans `System/user-profile.yaml`, `System/company-profile.yaml`, et crée les person pages dans `03-People/Internal/`. **Bloc 8.**

---

## 🎬 BLOC 8 — Phase 4 Activation skills & agents (10 min)

**Objectif :** Claude active automatiquement les skills + propose les playbooks.

### Ce que Claude affiche

```
✅ Activation terminée.

  ✅ Skills activés : [liste, ~14-18 selon connexions]
  ⏳ Skills en attente : [liste, ~6-10]
  🔒 Skills dormants : [liste, ~4]
  ✅ Playbooks proposés (5/18) :
     • 05-okr-operating-model
     • 06-customer-success-churn
     • 07-sales-stage-gates
     • 11-operating-cadence
     • 13-gtm-foundations
  ✅ Agents récurrents programmés (~5) :
     • /daily-plan        Mon-Fri 08:00
     • /friday-close      Fri 16:00
     • /drift-detection   Fri 17:00
     • /sync-cowork       Sun 22:00
     • /all-hands         Last Fri 14:00
```

### Ton rôle

- **Confirme les 5 playbooks** suggérés. le client peut en activer plus plus tard.
- **Confirme l'installation du cron**. Claude demande peut-être ton permission pour `crontab` — accepte.
- Vérifie avec le client que les horaires des agents lui conviennent. Particulièrement `/friday-close` 16h : c'est SON rituel.

### Watchpoint

Si Claude n'a pas activé `/friday-close` alors que Pipedrive + Calendar sont connectés → **bug**. Vérifier `bin/opowai status` et forcer activation via `bin/opowai activate`.

---

## 🎬 BLOC 9 — Phase 5 Premier run (15 min)

**Objectif :** prouver que ça tourne en live, sur ses vraies données.

### Étape 9.1 — Page Notion racine

Claude crée `📚 OpowAI SOPs & Playbooks` sur Notion. Il demande l'emplacement parent. **Tu suggères** : page "Team & Operations" ou racine du workspace [l’entreprise].

Le client vérifie sur Notion → la page existe avec l'arborescence (Strategy / Sales / Product / People / Operations / Finance / Crisis / Marketing).

### Étape 9.2 — Routing modèle

Claude écrit dans `.claude/settings.json` :
```json
{
  "model_routing": {
    "default": "claude-haiku-4-5",
    "analyses": "claude-sonnet-4-6",
    "strategy": "claude-opus-4-7"
  }
}
```
**Tu lui dis** : "Ça t'évite de saturer en tokens. Haiku pour les drafts, Sonnet pour les analyses, Opus pour la strat."

### Étape 9.3 — Premier `/daily-plan` en démo

Claude lance `/daily-plan` sur les vraies données du client (calendrier d'aujourd'hui, tâches en cours). C'est sa **première rencontre** avec ce que produit le système.

**Si on est vendredi (et on l'est) :** lancer aussi `/friday-close --preview` pour démontrer le rituel sur la semaine en cours.

### Étape 9.4 — Récap final

Claude affiche le bilan complet :

```
🎉 OpowAI v0.1.0 configuré.

📊 Bilan : X / 10 thématiques · Y skills activés · Z agents programmés

📅 Tes prochains rendez-vous OpowAI :
  • Demain 08:00     /daily-plan
  • Lundi prochain   /week-plan
  • Vendredi 16:00   /friday-close
```

---

## 🎬 BLOC 10 — Wrap-up + Q&A (20 min)

**Objectif :** cadrer la suite, capturer le feedback, fixer le retex.

### Script de wrap-up

> "Tu as un système opérationnel. Voici ce qui va se passer cette semaine."

#### Cette semaine (semaine du 26 mai)

1. **Lundi matin** : le client lance `/daily-plan`. Premier vrai usage solo.
2. **Vendredi 16h** : son premier vrai `/friday-close` automatique sur les RDV de la semaine.
3. **Dimanche 22h** : `/sync-cowork` tourne (même si Cowork pas encore configuré — il préparera le bundle).

#### Mois suivant (juin)

- Connexion des outils Phase 1 manquants si applicable
- Démarrage du **cas 2 — coaching sales** (avec transcripts Granola)
- Démarrage du **cas 5 — roadmap produit** via `/spec-audit` sur ses specs Lovable
- Construction du **MCP custom Pipedrive** si besoin (selon ses retours)

### Capturer son feedback (5 min)

3 questions ouvertes :
1. **Ce qui t'a impressionné** — pour pitcher OpowAI à d'autres
2. **Ce qui t'a frustré** — pour le backlog v0.2
3. **Ce que tu vas vraiment utiliser** — pour comprendre l'usage réel vs supposé

**Note ses réponses dans une note vault `00-Inbox/Feedback/YYYY-MM-DD-client-setup.md`** côté toi.

### Calage du retex

- **Dans 7 jours (vendredi 30 mai 17h)** — appel 30 min pour debrief premier usage solo
- **Dans 30 jours (vers le 23 juin)** — bilan mensuel + roadmap des features à pousser pour lui

### Ce qui doit être clair pour le client en partant

- [ ] **Il sait ouvrir Claude Code** dans `~/opowai` et taper une commande slash
- [ ] **Il sait où voir l'état du système** : `/opowai-status`
- [ ] **Il sait qu'il peut quitter et reprendre** sans rien casser
- [ ] **Il a le manuel** (`docs/setup-guide-v0.1.html`) en favori navigateur
- [ ] **Il sait à qui écrire** en cas de problème (toi, par mail)
- [ ] **Il a noté son retex à 7 jours** dans son calendrier

---

## 🚨 Plan B — Si ça part en sucette

### Si l'install plante (bloc 1)
→ Pas grave. Passez en **mode démo** sur ton vault à toi. Tu montres `bin/opowai status` et un exemple de `/daily-plan` depuis ton OpowAI. On installera chez lui plus tard.

### Si une connexion MCP rame (bloc 5)
→ Skip la thématique. Note dans `00-Inbox/Setup-followups.md` "configurer X". Le skill dépendant reste ⏳ pending — pas grave.

### Si l'auto-discovery hallucine ou délire (bloc 6/7)
→ **Manuel**. Tu remplis les YAML directement avec lui :
```bash
vi System/user-profile.yaml
vi System/company-profile.yaml
```

### Si Claude Code crashe ou perd le contexte
→ `Ctrl+C`, relance `claude` puis `/setup-opowai`. Le state est dans `System/.setup-state.json` — il reprendra.

### Si tu vois que tu déborderas largement
→ **Arrête au bloc 5 incomplet** (au moins Pipedrive + Calendar + Notion connectés). Pousse les blocs 7-10 à un appel suivant la semaine prochaine. Mieux vaut un setup partiel bien posé qu'un setup complet bâclé.

---

## 📝 Checklist post-session (à faire avant de partir)

- [ ] le client a OpowAI qui tourne sur sa machine
- [ ] Au minimum 4 thématiques connectées (CRM, Gmail, Calendar, Notion)
- [ ] Page Notion "📚 OpowAI SOPs" créée et visible
- [ ] Crontab installé (vérifier avec `crontab -l | grep opowai`)
- [ ] Feedback capturé dans `00-Inbox/Feedback/YYYY-MM-DD-client-setup.md`
- [ ] Retex 7 jours calé dans le calendrier
- [ ] Repo le client pushé sur son GitHub privé (vérifier `git log` chez lui)
- [ ] Tu as noté les bugs / friction points pour la v0.2

---

## 📞 Ressources de secours pendant la session

- **Repo OpowAI** : https://github.com/Flow8w/OpowAI
- **Doc moteur Python** : `.scripts/opowai/README.md`
- **Spec setup-opowai** : `.claude/skills/setup-opowai/SKILL.md`
- **Mapping skills/prereqs** : `System/skill-prerequisites.yaml`
- **Token GitHub Flow8w** : `~/.config/opowai/token` (sur ta machine, au cas où)

---

## 💭 Trois rappels pour toi, Florian

1. **Tu n'es pas en démo, tu es en setup.** le client n'a pas besoin d'être ébloui — il a besoin d'être autonome dans 30 jours.
2. **Refuse les sur-customisations.** S'il propose "et si on faisait aussi X spécifique pour [l’entreprise]" → "On le note pour la v0.2 — restons sur le setup standard aujourd'hui."
3. **Vendredi 16h, c'est SON rituel.** Si l'horaire de la session déborde sur 16h, **arrête tout, et lance `/friday-close --preview` en live**. Symbolique forte.

Bonne route 🚀
