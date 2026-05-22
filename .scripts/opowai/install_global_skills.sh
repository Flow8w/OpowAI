#!/usr/bin/env bash
# Install Opow.AI skills as symlinks in ~/.claude/skills/
# This makes the slash commands available from ANY directory in Claude Code,
# eliminating the need to relaunch Claude from within ~/opowai.
#
# Why symlinks (vs copy) :
#   - Updates via `git pull` in the repo automatically reflect everywhere.
#   - Single source of truth — no drift between repo state and global state.
#   - Clean uninstall: just remove the symlinks.

set -e

REPO_DIR="${1:-$HOME/opowai}"
GLOBAL_SKILLS_DIR="$HOME/.claude/skills"
REPO_SKILLS_DIR="$REPO_DIR/.claude/skills"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

say() { echo -e "${CYAN}▸${NC} $1"; }
ok()  { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
err()  { echo -e "${RED}✗${NC} $1"; }

if [[ ! -d "$REPO_SKILLS_DIR" ]]; then
  err "Skills source directory not found: $REPO_SKILLS_DIR"
  exit 1
fi

mkdir -p "$GLOBAL_SKILLS_DIR"

CREATED=0
ALREADY=0
CONFLICTS=()

for skill_dir in "$REPO_SKILLS_DIR"/*/; do
  [[ -d "$skill_dir" ]] || continue
  skill_name=$(basename "$skill_dir")
  target="$GLOBAL_SKILLS_DIR/$skill_name"

  # Case 1: existing symlink pointing to our repo → skip silently
  if [[ -L "$target" ]]; then
    actual=$(readlink "$target")
    if [[ "$actual" == "$skill_dir" || "$actual" == "${skill_dir%/}" ]]; then
      ALREADY=$((ALREADY + 1))
      continue
    fi
    # Symlink exists but points elsewhere → conflict
    CONFLICTS+=("$skill_name (symlink → $actual)")
    continue
  fi

  # Case 2: existing real file/dir → conflict
  if [[ -e "$target" ]]; then
    CONFLICTS+=("$skill_name (existing file)")
    continue
  fi

  # Case 3: free slot → create the symlink
  # Strip trailing slash for cleaner symlink target
  ln -s "${skill_dir%/}" "$target"
  CREATED=$((CREATED + 1))
done

# Summary
echo ""
ok "${BOLD}$CREATED${NC} skill(s) symlink(s) créé(s) dans $GLOBAL_SKILLS_DIR"
if [[ $ALREADY -gt 0 ]]; then
  ok "${BOLD}$ALREADY${NC} skill(s) déjà installé(s) (sautés)"
fi

if [[ ${#CONFLICTS[@]} -gt 0 ]]; then
  echo ""
  warn "${BOLD}${#CONFLICTS[@]} conflit(s)${NC} — les skills suivants existent déjà dans ~/.claude/skills/ et n'ont pas été remplacés :"
  for c in "${CONFLICTS[@]}"; do
    echo "    • $c"
  done
  echo ""
  echo "   Pour les résoudre, supprime manuellement le fichier en conflit puis relance :"
  echo "   bash $REPO_DIR/.scripts/opowai/install_global_skills.sh"
fi

echo ""
say "Les slash commands Opow.AI seront actives dans toute nouvelle session Claude Code, depuis n'importe quel dossier."
echo "    (Une seule relance de Claude Code est nécessaire après cette installation initiale.)"
