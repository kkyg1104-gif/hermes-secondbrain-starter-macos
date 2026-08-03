# Hermes Personal SecondBrain Starter

Current release: **v1.1.0**

A standalone Hermes skill for setting up a fresh personal Obsidian SecondBrain / LLM Wiki for one person and one agent.

This starter creates **structure, ontology, templates, Agent Rules, Tag Registry, and qmd setup guidance** only. It does **not** import another person's projects, people, decisions, memories, chats, configs, or private notes.

The generated instructions use first-person ownership language: **my SecondBrain**, **my vault**, **my LLM Wiki**.

## What this gives you

- Empty Obsidian vault skeleton
- First-person Agent Rules
- Project / agenda / decision / person / source / log / concept ontology
- Tag Registry and tag-deduplication rules
- Templates for core note types
- qmd first-time setup instructions
- Optional qmd collection/update/embed bootstrap
- “remember this / 기록해 / 저장해” recording workflow

## What it deliberately does not do

- It does not seed real projects.
- It does not seed real agendas.
- It does not seed real people.
- It does not seed real decisions.
- It does not copy another user's SecondBrain.
- It does not store secrets, passwords, tokens, auth codes, or private configs.

## Quick start

```bash
git clone https://github.com/kkyg1104-gif/hermes-secondbrain-starter-macos.git
cd hermes-secondbrain-starter-macos

# Choose a vault path.
export OBSIDIAN_VAULT_PATH="$HOME/Documents/SecondBrain"

# Validate first without writing anything.
bash install.sh --vault "$OBSIDIAN_VAULT_PATH" --check

# Create the empty vault skeleton.
bash install.sh --vault "$OBSIDIAN_VAULT_PATH"
```

The installer rejects a non-empty directory that does not contain its starter marker. After reviewing the target, use `--allow-nonempty` only when you intentionally want to add the structure to an existing directory. `--overwrite` automatically backs up existing managed files before replacing them.

To migrate a v1.0-generated vault, review the target and run with both `--allow-nonempty --overwrite`. The obsolete duplicate `10_Dashboard/People Hub.md` is backed up and removed; the canonical hub remains at `30_Knowledge/People/People Hub.md`.

If qmd is already installed and you want this installer to configure the qmd collection:

```bash
bash install.sh --vault "$OBSIDIAN_VAULT_PATH" --setup-qmd --qmd-collection my-secondbrain
```

If qmd is not installed yet:

```bash
npm install -g @tobilu/qmd
bash install.sh --vault "$OBSIDIAN_VAULT_PATH" --setup-qmd --qmd-collection my-secondbrain
```

## Install the skill into Hermes

For a multi-file install that works with Hermes versions whose bare-URL adapter only fetches one file, use the GitHub skill-directory identifier:

```bash
SKILL_ID="kkyg1104-gif/hermes-secondbrain-starter-macos/skills/personal-secondbrain-llm-wiki"
hermes skills inspect "$SKILL_ID"
hermes skills install "$SKILL_ID"
```

This directory bundle includes and security-scans both `SKILL.md` and `scripts/bootstrap_personal_secondbrain.py`. Newer Hermes releases may also follow explicit support-file links from a raw `SKILL.md` URL, but the GitHub directory identifier is the compatibility-first route.

Manual installation remains available:

Recommended local install pattern:

```bash
mkdir -p "$HOME/.hermes/skills/note-taking/personal-secondbrain-llm-wiki"
cp SKILL.md "$HOME/.hermes/skills/note-taking/personal-secondbrain-llm-wiki/SKILL.md"
mkdir -p "$HOME/.hermes/skills/note-taking/personal-secondbrain-llm-wiki/scripts"
cp scripts/bootstrap_personal_secondbrain.py "$HOME/.hermes/skills/note-taking/personal-secondbrain-llm-wiki/scripts/"
```

Then restart Hermes or start a new session so the skill list refreshes.

The shell `export OBSIDIAN_VAULT_PATH=...` is temporary. If Hermes runs through a gateway or another long-lived process, configure the vault path in that process's environment and start a new Hermes session after installing the skill.

## Agent instruction after install

Tell the target agent:

```text
Use the personal-secondbrain-llm-wiki skill to set up my personal SecondBrain.

My vault path is:
<absolute Obsidian vault path>

Requirements:
- Start with zero real projects, agendas, people, decisions, concepts, and sources.
- Do not import another person's SecondBrain or private context.
- Create only the structure, ontology, templates, Agent Rules, and Tag Registry.
- Configure qmd for this vault only if qmd is available.
- If qmd is missing, tell me how to install it and still finish the vault skeleton.
- When I say “remember this,” “record this,” “기억해,” “기록해,” or “저장해,” record it structurally into project, agenda, decision, person, source, log, or concept notes.
- Search existing notes and tags before creating new ones.
- After meaningful note changes, run qmd update && qmd embed and verify search when possible.
```

## qmd setup notes

qmd itself is **not bundled**. Install it separately, then let the bootstrap configure and verify a collection. The v1.1.0 bootstrap fails closed if an existing collection name points to a different path, and it verifies both `Agent Rules` and `Tag Registry` through collection-scoped searches before reporting success.

The bootstrap requires a qmd release that supports `qmd collection show <name>` (verified with qmd 2.1.0). If collection inspection is unavailable or fails for an ambiguous reason, setup stops instead of assuming the collection is missing.

Check qmd first:

```bash
command -v qmd || true
qmd --version 2>&1 || true
qmd collection list 2>&1 || true
qmd status 2>&1 || true
```

Add only this vault:

```bash
qmd collection add "$OBSIDIAN_VAULT_PATH" --name my-secondbrain
qmd context add qmd://my-secondbrain "My personal Obsidian SecondBrain / LLM Wiki."
qmd update
qmd embed
qmd status
qmd collection list
```

Verify search:

```bash
qmd search "My SecondBrain Agent Rules" --collection my-secondbrain
qmd search "Tag Registry" --collection my-secondbrain
```

## Files

```text
.
├─ CHANGELOG.md
├─ README.md
├─ SKILL.md
├─ install.sh
├─ scripts/
│  └─ bootstrap_personal_secondbrain.py
├─ skills/
│  └─ personal-secondbrain-llm-wiki/
│     ├─ SKILL.md
│     └─ scripts/
│        └─ bootstrap_personal_secondbrain.py
└─ tests/
   └─ test_bootstrap.py
```

## Privacy boundary

This repository is public and contains only generic setup logic. Do not commit generated vault content, personal notes, Hermes config, qmd index files, auth state, tokens, passwords, cookies, or API keys.
