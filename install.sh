#!/usr/bin/env bash
# OpowAI installer — exécuté UNE seule fois après git clone
# Tout le reste du setup se fait dans Claude Code via /setup-opowai

set -e

# ─── Couleurs / formatting ────────────────────────────────────
BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

say() { echo -e "${CYAN}▸${NC} $1"; }
ok() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
err() { echo -e "${RED}✗${NC} $1"; exit 1; }
section() { echo ""; echo -e "${BOLD}━━ $1 ━━${NC}"; }

# ─── Verify we're in the OpowAI repo ──────────────────────────
if [[ ! -f "CLAUDE.md" ]] || [[ ! -d ".claude/skills/setup-opowai" ]]; then
  err "install.sh doit être lancé depuis la racine du repo OpowAI cloné."
fi

REPO_DIR="$(pwd)"

section "Vérification des prérequis"

# ─── Check Python ─────────────────────────────────────────────
if ! command -v python3 >/dev/null 2>&1; then
  err "Python 3 non détecté. Installe Python 3.11+ depuis https://www.python.org/downloads/"
fi
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 11 ]]; }; then
  err "Python $PY_VER détecté — requis 3.11+. Mets à jour Python."
fi
ok "Python $PY_VER"

# ─── Check git ────────────────────────────────────────────────
if ! command -v git >/dev/null 2>&1; then
  err "git non détecté. Installe-le via Xcode Command Line Tools (xcode-select --install)."
fi
ok "$(git --version)"

# ─── Check Claude Code ────────────────────────────────────────
if ! command -v claude >/dev/null 2>&1; then
  warn "Claude Code (CLI 'claude') non détecté."
  warn "Tu pourras l'installer ensuite depuis https://claude.com/code"
else
  ok "$(claude --version 2>&1 | head -1 || echo 'claude (version inconnue)')"
fi

section "Création de l'environnement Python"

# ─── Create venv ──────────────────────────────────────────────
VENV_DIR="$REPO_DIR/.venv"
if [[ -d "$VENV_DIR" ]]; then
  say "Virtualenv déjà présent dans .venv, on saute la création."
else
  say "Création du virtualenv .venv ..."
  python3 -m venv "$VENV_DIR"
  ok "Virtualenv créé"
fi

# ─── Install deps ─────────────────────────────────────────────
say "Installation des dépendances Python (pyyaml, click)..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r .scripts/opowai/requirements.txt
ok "Dépendances installées"

section "Permissions & configuration"

# ─── Make CLI executable ──────────────────────────────────────
chmod +x bin/opowai 2>/dev/null || true
ok "bin/opowai exécutable"

# ─── Add upstream remote for future updates ──────────────────
if git remote | grep -q "^upstream$"; then
  ok "Remote upstream déjà configuré"
else
  UPSTREAM_URL=$(git remote get-url origin 2>/dev/null || echo "")
  if [[ -n "$UPSTREAM_URL" ]]; then
    git remote add upstream "$UPSTREAM_URL"
    ok "Remote upstream configuré (= origin pour l'instant)"
    say "Pour basculer vers le repo officiel OpowAI plus tard :"
    echo "    git remote set-url upstream https://github.com/Flow8w/OpowAI.git"
  fi
fi

# ─── Smoke test the CLI ───────────────────────────────────────
section "Test du moteur OpowAI"
if "$VENV_DIR/bin/python3" .scripts/opowai/cli.py status >/dev/null 2>&1; then
  ok "Le moteur OpowAI répond correctement"
else
  warn "Le moteur OpowAI a renvoyé une erreur (non bloquant — Claude diagnostiquera au setup)"
fi

# ─── Install skills globally in ~/.claude/skills/ ─────────────
section "Installation des skills Opow.AI au niveau global"
say "Création de symlinks dans ~/.claude/skills/ pour que les slash commands"
say "soient disponibles depuis n'importe quel dossier dans Claude Code."
bash "$REPO_DIR/.scripts/opowai/install_global_skills.sh" "$REPO_DIR"

# ─── Final message ────────────────────────────────────────────
section "Installation terminée 🎉"
cat <<EOF

Opow.AI est installé et ses skills sont disponibles globalement.

${BOLD}Prochaines étapes :${NC}

  1.  Quitte cette session Claude Code (${CYAN}/quit${NC}) puis relance-la une fois
      depuis n'importe quel dossier — par exemple ton home (${CYAN}cd ~ && claude${NC}).
      Cette relance unique permet à Claude de charger les skills Opow.AI.
  2.  Une fois Claude relancé, tape ${CYAN}/setup-opowai${NC} pour démarrer
      l'onboarding guidé.

Le setup ${BOLD}/setup-opowai${NC} s'occupe du reste :
  • Détection automatique de ton environnement
  • Configuration des MCPs (Pipedrive, Gmail, Notion, etc.)
  • Auto-discovery de ton contexte (équipe, ICP, glossaire)
  • Activation des skills et agents récurrents
  • Premier run de validation

${BOLD}Durée totale :${NC} ~30 min de bout en bout.

Bonne route 🚀

EOF
