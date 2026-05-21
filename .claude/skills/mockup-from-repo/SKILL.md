---
name: mockup-from-repo
description: Génération de maquettes alignées au design system existant — lit le repo (composants, tokens, patterns) et produit une maquette cohérente sans repartir de zéro.
status: implemented-v0.1
version: 0.1
category: Produit
required: [code]
optional: []
---

# /mockup-from-repo

Pour les founders techniques. Évite de repartir d'un Figma vierge — utilise ce qui existe déjà dans le code.

## Pré-requis
- **Required** : code (GitHub, GitLab, Bitbucket). Sans repo accessible, le skill se met en pending.

## Trigger
- Manuel : `/mockup-from-repo "Nouvelle page settings utilisateur"`
- Proactif : si une spec contient "mockup à faire" et un design system est détecté dans le repo, propose

## Workflow

### 1. Discovery design system
Lit le repo cible :
- Détecte le framework (React, Vue, Svelte, autre)
- Identifie les fichiers tokens (colors, spacing, typography) — patterns courants : `tokens/`, `theme/`, `tailwind.config`, `design-system/`
- Liste les composants UI réutilisables (`components/ui/`, `lib/components/`, etc.)
- Détecte les patterns récurrents (layout principal, container, header)

### 2. Brief utilisateur
Présente ce qui a été détecté + demande :
- Que doit faire la nouvelle UI ?
- Quels composants existants utiliser ?
- Quelles contraintes (mobile-first, accessibilité, etc.) ?

### 3. Génération maquette
Produit :
- Un fichier HTML/JSX selon le framework détecté
- Réutilise les composants identifiés (imports cohérents)
- Respecte les tokens (couleurs, spacing) du design system
- Output : code prêt à dropper dans une nouvelle PR

### 4. Documentation
Écrit `04-Projects/Mockups/YYYY-MM-DD-[slug]/` avec :
- Maquette (fichier code)
- README avec composants réutilisés + tokens utilisés
- Diff conceptuel (qu'est-ce qui est nouveau vs réutilisé)

### 5. Notification
"Maquette prête. 4 composants existants réutilisés, 1 nouveau composant 'UserSettingsCard' suggéré."

## Outputs

- `04-Projects/Mockups/YYYY-MM-DD-[slug]/` (code + README)
- Aucun push GitHub automatique. PR à créer manuellement par le dev.

## Anti-patterns à éviter
- Inventer des composants : si le design system n'a pas de "Select" custom, ne pas en inventer un — utiliser le HTML natif ou demander.
- Ignorer les tokens : ne JAMAIS coder en couleurs hex en dur si des tokens existent.
- Présupposer un framework : confirmer ce qui est détecté avant de générer.

## Exemples concrets

```
🎨 Mockup — "Page settings utilisateur"

Design system détecté :
  Framework : React + Tailwind
  Tokens : tailwind.config.js (colors.brand, spacing custom)
  Composants réutilisables : Button, Card, Input, Toggle, Avatar (9 dispos)

Brief :
  Page settings avec sections Profile / Notifications / Billing / Security.

Maquette générée :
  - Réutilise : Card, Input, Toggle, Button
  - Nouveau composant suggéré : SettingsSection (wrapper avec titre + content)
  - Tokens utilisés : colors.brand.500, spacing.6, spacing.8

→ Code dispo dans 04-Projects/Mockups/2026-05-21-user-settings/
```

## TODO v0.2
- Génération multi-frameworks parallèles (HTML statique + React + Figma export)
- Détection accessibility issues dans la maquette
- Mode "design review" : analyse une PR avec mockup et signale les écarts au design system

## Notes
- Privacy : `private: false` par défaut. Si le projet est sensible, hériter du tag du projet parent.
- Skill réservé aux founders techniques (ou COMEX avec repo accès).
- Réf. playbook `14-product-roadmap.md`.
