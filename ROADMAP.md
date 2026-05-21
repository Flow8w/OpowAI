# OpowAI Roadmap

## v0.1 — Cette semaine (livrable le client vendredi)

**Status :** 🟡 En construction

- [x] Repo GitHub `Flow8w/OpowAI` créé (privé)
- [x] Folder structure 11 dossiers
- [x] Playbooks Florian importés (4 markdown, 4 à convertir)
- [ ] CLAUDE.md OpowAI-branded
- [ ] Skills v0.1 (specs) :
  - [ ] `/setup-opowai` — onboarding 5 phases
  - [ ] `/sync-cowork` — sync hebdo vers Cowork (local)
  - [ ] `/publish-sop` — page racine Notion + arborescence auto
  - [ ] `/draft-support-reply` — brouillon mail support (P0 use case)
  - [ ] `/all-hands` — prep all-hands mensuel (template inclus)
- [ ] 3 améliorations validées (specs) :
  - [ ] `/context-cards` — cards modulaires pour Cowork
  - [ ] `/people-intel` — enrichissement people via Scrapling
  - [ ] `/drift-detection` — hook hebdo qui détecte les dérives
- [ ] System templates (user-profile, company-profile, pillars, privacy-rules, cowork-sync)
- [ ] Template `allhands-template.md`
- [ ] Hooks auto-sync git (post-action commit + push)
- [ ] Convertir playbooks HTML/docx → markdown (installer pandoc ou alternative)
- [ ] Top 5 use cases personnalisé le client à envoyer mercredi soir
- [ ] Setup vendredi avec le client chez [l’entreprise]

## v0.2 — Semaine 27 mai → 2 juin

**Theme :** Migration cloud + maturité playbooks

- [ ] **Migration agents vers GitHub Actions** (reporté de v0.1)
  - [ ] `/sync-cowork` programmé dimanche 22h
  - [ ] `/all-hands` programmé dernier vendredi du mois
  - [ ] `/weekly-digest` programmé vendredi 17h
  - [ ] Secrets management (Anthropic API key dans GitHub Secrets)
- [ ] Re-segmentation des 4 playbooks longs (coaching, SaaS, vente-valeur, valeur client) en SOPs atomiques
- [ ] 5 nouveaux playbooks pré-injectés (Hiring, Customer Discovery, OKR, Board, Support)
- [ ] Skill `/coach-team-member` — analyse transcripts récurrents
- [ ] Skill `/board-prep` — préparation board meeting

## v0.3 — Juin

**Theme :** Élargissement skills + landing page

- [ ] 10 playbooks pré-injectés complets
- [ ] Skill `/competitor-watch` — veille concurrentielle programmée
- [ ] Skill `/fundraising-tracker` (private:founder)
- [ ] Skill `/exec-summary` — synthèse hebdo board/investisseurs
- [ ] Landing page atelier OpowAI (avec early bird workflow)
- [ ] Documentation publique (notion-de-pricing.com ?)

## v1.0 — Juillet

**Theme :** Distribuable + funnel testé

- [ ] Onboarding visuel guidé (au-delà du Q&R Claude)
- [ ] Installer en autonomie (script `opowai-init`)
- [ ] Pricing/funnel testé sur 3 clients post-le client
- [ ] Atelier "x10 ops avec Claude" — itération 2 (post-10 juin)
- [ ] Option self-hosted GitLab pour clients régulés

## Backlog (non daté)

- Mode collaboratif temps réel sur le vault (multiple founders)
- Plugin VSCode pour édition rapide hors Claude Code
- Mobile companion (lecture seule)
- Skill `/decision-log` — journal de décisions avec rétrospective
- Skill `/hire-pipeline` — pipeline de recrutement intégré
- Connecteur DocuSign / Pennylane (clients FR)
- Multi-langue (EN default, FR localized)
