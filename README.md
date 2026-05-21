# OpowAI

**Le système d'exploitation personnel pour fondateurs et COMEX de startups SaaS.**

OpowAI est un vault Claude Code spécialisé founder/COMEX, fork de [Dex](https://github.com/Dave-Killeen/dex), repensé pour :
- Le quotidien d'un dirigeant (stratégie, COMEX, board, équipe, capital)
- La distribution multi-utilisateurs (Founder → COMEX → Équipe)
- L'opérationnalisation automatique via playbooks et SOPs

---

## Architecture en 3 couches

```
GITHUB (source de vérité, privé)
    ▲
    │ auto-sync
    ▼
CLAUDE CODE (founder + power users)   →   CLAUDE COWORK (COMEX)   →   NOTION SOPs (équipe)
```

1. **Claude Code** — vault complet, source de vérité, tous les skills/agents/MCPs.
2. **Claude Cowork** — projet partagé "Company Context", filtré par règles privacy.
3. **Notion** — page racine "📚 OpowAI SOPs" générée automatiquement, base canon pour toute l'équipe.

---

## Principes

1. **GitHub-first, local working copy** — zéro perte, multi-device gratuit, audit via git history.
2. **Human-in-the-loop systématique** — aucune action externe sans validation.
3. **Privacy par frontmatter** — `private: founder | comex | false`. Opt-in publication, pas opt-out censure.
4. **Markdown pérenne** — vault lisible à vie, même sans OpowAI.
5. **Playbooks > prompts** — playbooks éprouvés injectés, reproductibles, auditables.
6. **Évolution par SOPs** — chaque process mature devient un SOP Notion (page racine "📚 OpowAI SOPs").

---

## Structure

```
opowai/
├── 00-Inbox/                  # Capture brute
├── 01-Strategy/               # Vision, OKRs, Industry Truths, Pricing, Fundraising
├── 02-Company/                # ICP, Glossaire, Products, Competitors
├── 03-People/                 # Internal / External / Board & Investors
├── 04-Projects/               # Company (partagé) / Private (founder)
├── 05-Operations/             # SOPs / Playbooks / Rituals
├── 06-Meetings/               # Board / COMEX / 1-1 / External / All-Hands
├── 07-Tasks/
├── 08-Coaching/               # Team development, transcripts analysis
├── 09-Resources/
├── 10-Archives/
└── System/                    # Configs, templates, privacy rules
```

---

## Démarrer

1. Clone : `git clone git@github.com:Flow8w/OpowAI.git`
2. Lance Claude Code dans le dossier
3. Exécute `/setup-opowai` — Claude te guide en 5 phases (~30 min)
4. Lis `WELCOME.md` pour comprendre comment OpowAI vit et s'améliore dans le temps

---

## Roadmap

Voir [ROADMAP.md](./ROADMAP.md) — v0.1 (cette semaine), v0.2 (Actions cloud), v1.0 (juillet).

---

**Maintenu par** [Florian Guerrier](https://github.com/Flow8w) — Fractional COO / Consultant / Coach
