---
name: setup-opowai
description: Onboarding guidé d'OpowAI en 6 phases avec checklist visible, connexion thématique des outils, et activation just-in-time des skills/agents au fur et à mesure que les prérequis sont remplis.
status: implemented-v0.1
version: 0.2
implementation: .scripts/opowai/
cli: bin/opowai
---

## Usage rapide

Ce skill est implémenté en Python dans `.scripts/opowai/`. Pour l'invoquer directement :

```bash
./bin/opowai init              # Phase 0
./bin/opowai connect crm       # Phase 1 (boucle)
./bin/opowai discover          # Phase 2
./bin/opowai confirm           # Phase 3
./bin/opowai activate          # Phase 4
./bin/opowai first-run         # Phase 5
./bin/opowai status            # Vue d'ensemble à tout moment
./bin/opowai resume            # Reprend où on en était
```

Voir `.scripts/opowai/README.md` pour la documentation complète du moteur.

---


# /setup-opowai

Skill d'orchestration de l'onboarding OpowAI. Conçu pour être **hyper didactique** : chaque étape est visible, l'avancement est constamment montré, l'utilisateur sait exactement où il en est et ce qui se débloque.

## Philosophie

- **Tout visible** : checklist persistante dans `System/setup-checklist.md`, mise à jour en temps réel
- **Just-in-time** : les skills s'activent dès que leurs prérequis sont remplis, pas en fin de setup
- **Résumable** : l'utilisateur peut quitter et reprendre à tout moment
- **Transparent** : à chaque connexion d'outil, l'utilisateur voit ce qui se débloque
- **Pas de rail forcé** : porte de sortie "Autre" dans chaque thématique, thématique "Autre" en fin

---

## Architecture

```
PHASE -1 — Environment prep (Claude vérifie tout)  [≈ 2 min, automatique]
PHASE 0  — Bienvenue & priorisation                [≈ 5 min]
PHASE 1  — Connexion thématique des outils         [≈ 15-20 min]
PHASE 2  — Auto-discovery (background)             [parallèle à phase 1]
PHASE 3  — Confirmation guidée                     [≈ 5 min]
PHASE 4  — Activation des skills/agents            [progressif]
PHASE 5  — Premier run                             [≈ 5 min]
```

Total ≈ 30-40 min, dont **2 min de manuel** (juste le `git clone` + `bash install.sh` AVANT de lancer Claude Code).

---

## PHASE -1 — Environment prep (NOUVEAU — tout en chat)

**Principe : zero manual step pour l'utilisateur une fois Claude Code lancé.** Tout ce qui peut être exécuté en Bash depuis le chat l'est. Claude diagnostique et corrige.

### Étape -1.1 — Diagnostic environnement

Claude lance via Bash :
```bash
# Vérifications
python3 --version            # 3.11+ ?
git --version                # présent ?
ls .venv 2>/dev/null         # venv existe ?
.venv/bin/python3 -c "import yaml, click" 2>&1  # deps installées ?
git remote -v                # remote configuré ?
which claude                 # claude code dispo ?
crontab -l 2>&1 | grep opowai  # cron déjà installé ?
# Vérif des symlinks globaux des skills
ls -la ~/.claude/skills/setup-opowai 2>/dev/null  # skill global installé ?
```

Affiche un récap clair :
```
🔍 Diagnostic OpowAI
  ✅ Python 3.11.15
  ✅ Git 2.44
  ✅ Virtualenv .venv présent
  ✅ Dépendances (pyyaml, click)
  ✅ Remote origin configuré (Flow8w/OpowAI)
  ✅ Skills installés globalement (~/.claude/skills/)
  ⏳ Remote upstream non configuré
  ⏳ Cron OpowAI non installé
```

### Étape -1.2 — Réparation automatique

Pour chaque ⏳ détecté, Claude **propose** la correction et l'exécute après accord utilisateur (jamais en silence) :

- **Venv manquant** → `python3 -m venv .venv && .venv/bin/pip install -r .scripts/opowai/requirements.txt`
- **Deps manquantes** → `.venv/bin/pip install -r .scripts/opowai/requirements.txt`
- **Remote upstream absent** → `git remote add upstream https://github.com/Flow8w/OpowAI.git`
- **Skills non installés globalement** → `bash .scripts/opowai/install_global_skills.sh ~/opowai` (rend les slash commands disponibles depuis n'importe quel dossier, dans toutes les futures sessions). Si Claude exécute ça en cours de session, prévenir : "Tu devras relancer Claude une fois pour que les skills apparaissent dans cette session."
- **Cron pas installé** → propose `crontab -l > /tmp/current; cat .scripts/cron/opowai.cron >> /tmp/current; crontab /tmp/current` (fera attendre phase 4 pour que le fichier cron existe)

### Étape -1.3 — Détection des MCPs déjà configurés dans Claude Code

Claude lance :
```bash
cat ~/.claude.json 2>/dev/null | python3 -c "import json, sys; d=json.load(sys.stdin); print('\n'.join(d.get('mcpServers', {}).keys()))" 2>/dev/null
```

Et compare avec les outils des 10 thématiques. Si Pipedrive est déjà configuré comme MCP par exemple, on saute la connexion en phase 1 pour cette thématique → l'utilisateur gagne du temps.

### Étape -1.4 — Validation

Une fois tout vert :
```
✅ Environnement OpowAI prêt.

📦 Détecté préalablement :
  • MCPs déjà configurés : Notion, Gmail (on les utilisera en phase 1)
  • Skills déjà activés (rituels sans pré-req) : daily-review, week-review,
    quarter-plan, drift-detection

▶ Prêt à démarrer la phase 0 ?
```

---

## Fichiers gérés par ce skill

| Fichier | Rôle |
|---------|------|
| `System/setup-checklist.md` | État persistant visible — mis à jour à chaque action |
| `System/skill-prerequisites.yaml` | Cerveau : mapping skills → thématiques requises/optionnelles |
| `System/user-profile.yaml` | Rempli en phase 2-3 |
| `System/company-profile.yaml` | Rempli en phase 2-3 |
| `System/.setup-state.json` | État interne (phase courante, thématiques connectées) — gitignored |
| `02-Company/Glossary.md` | Pré-rempli en phase 2 depuis Notion/Slack |
| `03-People/Internal/*` | COMEX créés en phase 2 |

---

## PHASE 0 — Bienvenue & priorisation

### Étape 0.1 — Lecture du WELCOME.md
Affiche `WELCOME.md` dans le chat (ou résumé si l'utilisateur dit "je l'ai lu").

### Étape 0.2 — Priorisation des cas d'usage

Présente les 10 cas d'usage d'OpowAI (lus depuis `skill-prerequisites.yaml`, section `use_cases`) :

```
🎯 Parmi ces cas d'usage, lesquels te font le plus envie ?
(Sélectionne 3 au minimum — on adaptera le setup pour les rendre opérationnels en premier.)

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

Sauvegarde sélection dans `System/.setup-state.json` → `selected_use_cases: [...]`.

Calcule la liste des **skills "sélectionnés"** (union des skills des use cases choisis). Tous les autres skills passent en statut `🔒 dormant` jusqu'à activation manuelle.

### Étape 0.3 — Update checklist

Génère `System/setup-checklist.md` depuis le template et coche Phase 0 ✅.

---

## PHASE 1 — Connexion thématique

### Boucle principale

Pour chaque thématique dans l'ordre fixe (1 → 10), Claude présente :

```
─────────────────────────────────────────────────────
THÉMATIQUE 1/10 — CRM & Sales 💼
─────────────────────────────────────────────────────

Le cœur commercial : pipeline, deals, contacts.

Sans CRM connecté, pas de prep RDV, pas de récap pipeline, pas de board prep.

Les outils dans cette catégorie :
  • Pipedrive (populaire)
  • HubSpot (populaire)
  • Salesforce
  • Close
  • Attio
  • Folk
  • Autre / Mon outil n'est pas listé
  • Je n'ai pas de CRM (skip)

Quel est ton outil principal ?
```

### Si l'utilisateur choisit un outil connu

Claude :
1. Vérifie si un MCP existe pour cet outil dans le registry
2. Lance le flow de connexion guidé (auth, scopes, test ping)
3. Affiche un **wait state** explicite : « ⏳ Je t'attends — autorise OpowAI sur Pipedrive dans la fenêtre qui s'ouvre »
4. Une fois connecté, scan rapide (read-only) pour confirmer ping OK
5. **Notification de débloquage** (voir ci-dessous)

### Si l'utilisateur choisit "Autre"

```
Quel est cet outil ?

Et est-ce qu'il a :
  • Un MCP officiel (URL ?)
  • Une API publique
  • Aucune intégration (note manuelle)
```

Si MCP → tentative de connexion via registry custom.
Si API → propose de créer un MCP custom (skill `/integrate-mcp` ou doc).
Si rien → enregistre l'outil dans `System/manual-tools.yaml` pour référence (skills ne s'activent pas pour cette thématique).

### Si l'utilisateur choisit "Skip"

Thématique marquée 🔘 todo, on passe à la suivante. Les skills dépendants restent ⏳ pending.

### Notification de débloquage (CRITIQUE)

À chaque connexion d'outil réussie, Claude affiche :

```
✅ Pipedrive connecté.

🎉 Ce que ça débloque immédiatement :

  ✅ Skills activés (3)
     • /pipeline-monitor — monitoring pipeline + alertes drift
     • /board-prep — prep board meeting
     • /exec-summary — synthèse exec hebdo

  ⏳ Skills en attente d'autres outils (2)
     • /friday-close — attend Calendar
     • /prep-meeting — attend Calendar

  💡 Prochaine étape recommandée : connecter Calendar pour débloquer
     ton rituel vendredi 16h (cas d'usage prioritaire).

Tape `continue` pour la thématique suivante (Email).
```

### Update checklist en temps réel

Après chaque connexion, ré-écriture de `System/setup-checklist.md` :
- Coche la ligne thématique dans le tableau
- Met à jour la section "Skills activés" / "En attente"
- Recalcule le % d'avancement global

---

## PHASE 2 — Auto-discovery (background)

**Lance en parallèle dès qu'au moins 2 thématiques sont connectées.**

Agents parallèles selon outils connectés :

| Source | Extrait |
|--------|---------|
| Notion | Pages root, glossaire, OKRs si trouvés, org chart |
| Drive | Structure dossiers, docs récents |
| Gmail | Domaines emails (équipe vs externe), signatures (rôles), historique récent |
| Calendar | Rituels (1:1, COMEX, board, all-hands), fréquences |
| CRM | Pipeline, customers (révèle ICP), MRR/clients si dispo |
| Slack | Canaux principaux, équipes, glossaire récurrent |
| GitHub | Repos, langages, projets actifs |
| Transcripts | Patterns de calls, vocabulaire client |

Output dans `System/.discovery-draft.yaml` (gitignored, sensible).

Notifications discrètes :

```
🔵 Auto-discovery en cours...
  ✅ Profil détecté ([le client], CEO [l’entreprise])
  ✅ COMEX détecté (3 personnes)
  🔵 Glossaire en cours (depuis Notion)
  🔵 ICP en cours (depuis Pipedrive)
```

---

## PHASE 3 — Confirmation guidée

Quand auto-discovery est terminée, présente à l'utilisateur :

```
✨ J'ai pré-rempli ton profil. Confirme ou corrige.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Toi
  Nom :     [le client]
  Rôle :    CEO
  Email :   [founder]@[entreprise].com
  → [Confirmer] [Modifier]

Ta boîte
  Nom :     [l’entreprise]
  Domaine : [entreprise].com
  Secteur : SaaS B2B (PostHog product analytics adjacent ?)
  Stade :   Seed
  Taille :  ~12 personnes (détecté via emails)
  → [Confirmer] [Modifier]

COMEX (3 personnes détectées)
  ✓ [membre COMEX] [...]
  ✓ [un membre du COMEX] [...]
  ✓ [un autre membre du COMEX] [...]
  → [Confirmer] [Ajouter / Retirer]

Pillars stratégiques (défaut)
  • Growth · Product · Team · Operations · Capital
  → [Garder par défaut] [Personnaliser]

Privacy rules (défaut)
  • Fundraising/, Board/, Projets Privés → private:founder
  • COMEX meetings, OKRs → private:comex
  • Tout le reste → public
  → [Garder par défaut] [Modifier]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

À chaque confirmation, écriture dans `System/user-profile.yaml` / `company-profile.yaml` / `03-People/Internal/*`.

---

## PHASE 4 — Activation des skills/agents

**Cette phase tourne en parallèle des phases 1-3.** Au moment où Phase 1 + Phase 3 sont complètes, tous les skills sélectionnés en phase 0 dont les prérequis sont remplis passent à ✅ activated.

### Pour chaque skill ✅ activated

1. Création de la commande dans `.claude/skills/[name]/SKILL.md` (instanciée depuis la spec)
2. Si `schedule` défini dans `skill-prerequisites.yaml` → ajout au cron local (`.scripts/cron/opowai.cron`)
3. Notification utilisateur :
   ```
   ✅ /friday-close activé
      Première exécution : vendredi 2026-05-22 à 16h
      Pour tester maintenant : tape /friday-close --preview
   ```

### Sélection des playbooks

À ce stade, propose les 5 playbooks les plus pertinents pour le stade + use cases sélectionnés :

```
🎯 Voici les 5 playbooks à activer en priorité pour toi
   (sur les 18 disponibles dans 05-Operations/Playbooks/) :

  ✓ 05-okr-operating-model  (cadence trimestrielle)
  ✓ 06-customer-success-churn  (P0 vu support client)
  ✓ 07-sales-stage-gates  (P0 vu pipeline)
  ✓ 11-operating-cadence  (vendredi 16h)
  ✓ 13-gtm-foundations  (motion sales en pose)

→ [Activer tous] [Modifier la sélection]
```

Les autres restent dispos mais marqués comme non-actifs.

---

## PHASE 5 — Premier run

### Étape 5.1 — Création page Notion racine

Via skill `/publish-sop --init` :
- Crée la page **"📚 OpowAI SOPs & Playbooks"** sous le parent confirmé par l'utilisateur
- Arborescence : Strategy · Sales · Product · People & Team · Operations · Finance · Crisis · Marketing
- Sauvegarde `notion_root_page_id` dans `company-profile.yaml`

### Étape 5.2 — Routing modèle

Écrit dans `.claude/settings.json` :
```json
{
  "model_routing": {
    "default": "claude-haiku-4-5",
    "analyses": "claude-sonnet-4-6",
    "strategy": "claude-opus-4-7"
  }
}
```

### Étape 5.3 — Premier daily-plan en démo

Lance `/daily-plan --demo` pour l'utilisateur voir le rendu.

### Étape 5.4 — Si vendredi : premier /friday-close

Si jour de setup = vendredi → propose lancer `/friday-close --preview` immédiatement avec données de la semaine en cours.

### Étape 5.5 — Récap final

```
🎉 OpowAI v0.1.0 configuré.

📊 Bilan
  ✅ 7 / 10 thématiques connectées
  ✅ 14 skills activés (sur 24)
  ⏳ 6 skills en attente (Data, Code, Transcripts)
  🔒 4 skills dormants (non sélectionnés)
  ✅ 5 playbooks actifs (sur 18)
  ✅ 5 agents récurrents programmés

📅 Tes prochains rendez-vous OpowAI
  • Demain 08:00 → /daily-plan
  • Vendredi 16:00 → /friday-close (premier vrai run)
  • Dimanche 22:00 → /sync-cowork
  • Dernier vendredi du mois → /all-hands

📚 Documentation
  • README.md  — vue d'ensemble
  • WELCOME.md — comment ça vit dans le temps
  • ROADMAP.md — v0.2, v0.3
  • System/setup-checklist.md — tu peux y revenir à tout moment

Tape `/opowai-status` pour avoir la vue d'ensemble.
Tape `/help` pour voir tous les skills disponibles.

Bienvenue dans OpowAI 🚀
```

---

## États & reprise

### Si l'utilisateur quitte en cours de setup
`System/.setup-state.json` garde la trace :
```json
{
  "current_phase": "1",
  "current_thematic": "calendar",
  "completed_thematics": ["crm", "email"],
  "selected_use_cases": ["pipeline-prep", "coaching-sales", "support-client"],
  "auto_discovery_status": "running",
  "started_at": "2026-05-21T10:00:00Z",
  "last_update": "2026-05-21T10:23:00Z"
}
```

### Reprise
À la prochaine session, message d'accueil :
```
👋 Bon retour ! Tu avais commencé ton setup hier.

  ✅ Phase 0 : terminée
  🔵 Phase 1 : 2/10 thématiques connectées (CRM + Email)
  🔘 Phases suivantes : en attente

Tape `continue` pour reprendre où tu en étais.
Tape `restart` pour repartir de zéro.
Tape `/opowai-status` pour voir le détail.
```

### Modification ad-hoc
- `/setup-opowai --redo thematic-crm` → reconfigure une thématique
- `/setup-opowai --add-tool` → ajouter un outil "Autre" plus tard
- `/setup-opowai --change-use-cases` → re-prioriser

---

## TODO d'implémentation v0.1

- [ ] Parser `System/skill-prerequisites.yaml`
- [ ] Logique de calcul des skills débloqués vs en attente (à chaque connexion)
- [ ] Mise à jour temps réel de `System/setup-checklist.md`
- [ ] Wrappers de connexion par MCP (Notion, Pipedrive, Gmail, Calendar, Slack, GitHub, Stripe, Posthog…)
- [ ] Auto-discovery agent (background)
- [ ] Création des SKILL.md des autres skills à partir de leurs specs au moment de l'activation
- [ ] Hook cron local pour les schedules
- [ ] Persistance et reprise via `.setup-state.json`
- [ ] Commande `/opowai-status`
- [ ] Commande `/setup-opowai --redo|--add-tool|--change-use-cases`

## Notes design

- **Symboles cohérents** partout : `✅ ⏳ 🔘 🔒 🔵` (cf. `skill-prerequisites.yaml > symbols`)
- **Pas de surprise** : à chaque action, l'utilisateur sait ce qui se passe et pourquoi
- **Confirmation > saisie** : on n'écrit que ce qu'on ne peut pas inférer
- **Privacy par défaut** : tous les dossiers sensibles auto-configurés en `private: founder`
