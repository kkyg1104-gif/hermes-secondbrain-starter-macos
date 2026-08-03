---
name: personal-secondbrain-llm-wiki
description: Use when setting up a fresh personal Obsidian SecondBrain / LLM Wiki for one person's own agent, starting from zero content with ontology, templates, tag registry, qmd indexing, and structured “remember/record this” workflows.
version: 1.1.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [secondbrain, obsidian, qmd, llm-wiki, personal-knowledge, note-taking, ontology]
    related_skills: [obsidian, hermes-agent]
---

# Personal SecondBrain LLM Wiki

## Overview

Use this skill to set up a **fresh, empty personal SecondBrain** for the current agent/user pair. The goal is not to copy another person's vault or seed projects. The goal is to create a clean Obsidian + qmd-backed LLM Wiki that can grow from the person's own future requests such as “remember this,” “record this,” “save this for later,” or equivalent phrases.

The installed vault should begin with **zero personal projects, zero agendas, zero people, and zero decisions**. Only the structure, ontology, templates, tag registry, qmd rules, and agent recording instructions are created.

Use first-person ownership in generated instructions. For the target agent, this is **my SecondBrain**, **my vault**, and **my LLM Wiki**. Avoid third-person owner labels or another person's name inside reusable/public files unless the user explicitly asks for a named private deployment.

## When to Use

Load this skill when the user asks to:

- set up Obsidian as a personal SecondBrain for a new/family/personal agent;
- create an LLM Wiki from scratch with project/agenda/decision/person/source/log/concept structure;
- make “기억해 / 기록해 / 저장해 / remember this / record this” requests write structured notes;
- prevent importing another user's SecondBrain contents while reusing only the operating model;
- configure qmd indexing so every meaningful note write/update is searchable;
- define tag hygiene, ontology, duplicate-prevention, and correction/update rules.

Do not use this to migrate or merge existing vault contents. If migration is requested, first make an explicit import plan, privacy review, and deduplication strategy.

## Non-Negotiable Principles

1. **Start empty.** Do not copy another person's projects, agendas, people, decisions, source notes, tags, private contexts, paths, or chat history.
2. **Structure is allowed; content is not.** Folder layout, templates, ontology, qmd refresh rules, and agent instructions may be reused.
3. **The vault belongs to the active person.** Use first-person wording in agent-facing instructions: “my SecondBrain,” “my vault,” “my records.”
4. **Search before writing.** Existing project/agenda/person/concept/decision notes must be checked before creating new ones.
5. **Project/agenda first.** Do not bury long-lived knowledge only in daily logs or message sources.
6. **Sources preserve provenance.** Source notes record where a fact came from; project/agenda/person/concept notes hold the current usable state.
7. **Tags are controlled vocabulary.** Reuse existing tags from the registry; create a new tag only when it adds reusable classification value.
8. **qmd follows writes.** Meaningful note create/update/delete operations must be followed by qmd update/embed and a search check when available.
9. **Secrets are never stored.** Passwords, auth codes, card security values, API keys, tokens, cookies, and OAuth/device codes do not belong in the vault.

## Recommended Tooling

| Need | Tool |
|---|---|
| Human-facing notes | Obsidian |
| Agent file writes/patches | Hermes file tools or equivalent safe file operations |
| Semantic/keyword retrieval | qmd index for this vault only |
| Optional OCR/image/document capture | Add later; do not make it part of the initial MVP |
| Sync | Optional later; do not require complex sync for first setup |

Recommended environment variables:

```bash
OBSIDIAN_VAULT_PATH="/absolute/path/to/SecondBrain"
QMD_COLLECTION="my-secondbrain"
```

qmd must index only this vault. Do not point the new agent's qmd collection at another user's SecondBrain.

## qmd First-Time Setup

Do not assume qmd is already installed or configured on a fresh personal-agent machine. Check first:

```bash
command -v qmd || true
qmd --version 2>&1 || true
qmd collection list 2>&1 || true
qmd status 2>&1 || true
```

If qmd is missing, install it with the package manager available on the machine. The standard npm route is:

```bash
npm install -g @tobilu/qmd
```

Then add only this vault as a collection:

```bash
export OBSIDIAN_VAULT_PATH="/absolute/path/to/SecondBrain"
export QMD_COLLECTION="my-secondbrain"

qmd collection add "$OBSIDIAN_VAULT_PATH" --name "$QMD_COLLECTION"
qmd context add "qmd://$QMD_COLLECTION" "My personal Obsidian SecondBrain / LLM Wiki. It starts empty and grows from my own explicit records, sources, and decisions."
qmd update
qmd embed
qmd status
qmd collection list
```

Verify with system-file searches before relying on qmd for real records:

```bash
qmd search "My SecondBrain Agent Rules" --collection "$QMD_COLLECTION"
qmd search "Tag Registry" --collection "$QMD_COLLECTION"
qmd query "how should my agent record memories in my SecondBrain" --collection "$QMD_COLLECTION" --no-rerank
```

If qmd installation/configuration fails, the vault setup is still useful. Report separately: “vault created, qmd not configured yet.” Do not pretend that the notes are searchable through qmd until verification succeeds.

## Initial Vault Structure

Create these folders and hub/system files only. Do not create real personal projects, agendas, people, decisions, or concepts during bootstrap.

```text
SecondBrain/
├─ 00_Inbox/
│  └─ Inbox.md
├─ 10_Dashboard/
│  ├─ Home.md
│  ├─ Projects Hub.md
│  ├─ Agendas Hub.md
│  ├─ Decisions Hub.md
│  └─ Tags & Ontology Hub.md
├─ 20_Life/
│  ├─ 10_Projects/
│  ├─ 20_Agendas/
│  ├─ 20_Logs/
│  │  └─ YYYY/
│  │     └─ Life Log Index.md
│  └─ 30_Decisions/
│     └─ YYYY/
├─ 30_Knowledge/
│  ├─ People/
│  │  └─ People Hub.md
│  ├─ Concepts/
│  ├─ Sources/
│  │  ├─ Message/
│  │  ├─ Image/
│  │  ├─ Document/
│  │  └─ Web/
│  └─ Assets/
├─ 40_Events/
│  └─ Calendar/
└─ 90_System/
   ├─ Agent Rules.md
   ├─ Ontology/
   │  ├─ Ontology Guide.md
   │  └─ Tag Registry.md
   └─ Templates/
      ├─ Project.md
      ├─ Agenda.md
      ├─ Decision.md
      ├─ Person.md
      ├─ Source_Message.md
      ├─ Source_Image.md
      ├─ Source_Document.md
      ├─ Source_Web.md
      ├─ Log.md
      └─ Concept.md
```

Use the current year for `YYYY`.

## Core Ontology

| type | Meaning | Create when |
|---|---|---|
| `project` | A continuing effort with state, goals, constraints, or next actions | The topic will continue over time |
| `agenda` | A recurring issue/question to monitor or revisit | It is not yet a project but should stay visible |
| `decision` | A choice, rejection, deferral, priority change, or rationale | The person decided or changed direction |
| `person` | A person, relationship, contact, or recurring human context | The person is likely to recur |
| `source` | A message, image, document, web page, or other evidence | Provenance matters |
| `log` | A date-specific event or episode | The time/date is the main organizing key |
| `concept` | Reusable knowledge, criteria, preference, rule, or explanation | It should be searchable outside one project |

## Recording Triggers

Treat the following as SecondBrain write requests:

- Korean: `기억해`, `기록해`, `저장해`, `나중에 참고하게 해줘`, `세컨브레인에 넣어줘`, `이거 기억해둬`
- English: `remember this`, `record this`, `save this`, `put this in my SecondBrain`, `keep this for later`

When uncertain whether the user wants durable storage, ask briefly before writing.

## Record/Remember Workflow

When a write request is triggered:

1. Extract core facts: who, what, when, where, why, amount, preference, condition, decision, risk, and next action.
2. Search the vault first for related project, agenda, person, concept, decision, and source notes.
3. Search the tag registry and existing frontmatter tags before adding tags.
4. If a relevant note exists, update it rather than creating a duplicate.
5. If no relevant note exists, create the smallest appropriate note type.
6. If the message itself is provenance, create a concise source note under `30_Knowledge/Sources/Message/`.
7. If the fact changes the current state of a project/agenda/person/concept, update that main note too.
8. If a choice, rejection, deferral, or priority change occurred, create or update a decision note under `20_Life/30_Decisions/YYYY/`.
9. If the event is date-specific, record it under `20_Life/20_Logs/YYYY/` and also update project/agenda/person/concept if useful.
10. Update hub files when a new project, agenda, person, or decision is created.
11. Run qmd refresh for the vault.
12. Verify by searching for one or two core keywords when qmd/search tooling is available.
13. Report only: what was recorded, where it was recorded, and any unclear fields.

## qmd Operating Rules

Use qmd as the retrieval layer for this vault only.

After meaningful note creation, modification, deletion, renaming, or tag-registry changes:

```bash
qmd update && qmd embed
```

If local qmd uses a different command or collection argument, use the configured equivalent. The invariant is:

1. The current vault path is the only indexed target.
2. qmd is refreshed after meaningful writes.
3. A keyword search verifies the new/changed content when possible.
4. Failures are reported separately: “recording succeeded, qmd refresh failed.”

Do not silently claim searchability when qmd failed or was unavailable.

## Tag Hygiene

Create `90_System/Ontology/Tag Registry.md` before the first real write.

Rules:

1. Before adding a tag, search the registry and existing frontmatter tags.
2. Reuse the existing tag if a synonym already exists.
3. Prefer English lowercase kebab-case for reusable tags.
4. Do not use people, project names, locations, or one-off phrases as tags; use wikilinks/frontmatter instead.
5. If a genuinely new reusable tag is needed, add it to the registry immediately.
6. Avoid Korean/English/plural/spacing variants for the same meaning.

Starter registry:

| tag | Meaning |
|---|---|
| `life` | General personal life domain |
| `project` | Project type helper |
| `agenda` | Agenda type helper |
| `decision` | Decision type helper |
| `person` | Person type helper |
| `source` | Source/provenance helper |
| `log` | Date-based log helper |
| `concept` | Reusable knowledge helper |
| `family` | Family context |
| `health` | Health, hospital, medicine |
| `home` | Home, appliances, living space |
| `shopping` | Purchase/comparison context |
| `travel` | Travel context |
| `finance` | Costs, settlement, money context |
| `document` | Document source/context |
| `image` | Image/photo source/context |
| `web` | Web source/context |
| `message` | Message source/context |

Alias table examples:

| Do not create | Use instead |
|---|---|
| `생활` | `life` |
| `가족` | `family` |
| `건강`, `병원` | `health` |
| `구매`, `쇼핑` | `shopping` |
| `여행` | `travel` |
| `돈`, `비용` | `finance` |
| `메모` | Use `type` and note content |

## Correction and Update Rules

When the user corrects a prior record:

1. Search for the existing note first.
2. Patch the current-state note rather than creating a contradictory duplicate.
3. Keep provenance in source/log if useful, but make the project/agenda/person/concept note reflect the latest truth.
4. If a decision was superseded, mark the old decision `status: superseded` and link the new one.
5. Run qmd refresh and search for stale wrong phrasing if the correction is important.
6. Report the correction and qmd status.

## Duplicate Prevention

Before creating a project, agenda, person, concept, or decision:

1. Search by the intended title.
2. Search by key nouns, aliases, and likely synonyms.
3. Check hub files.
4. Reuse or update an existing note if it serves the same purpose.
5. If a new note is truly needed, add a short “why separate” line when the distinction is not obvious.

Source notes may be numerous; project/agenda/person/concept notes should be deduplicated aggressively.

## Bootstrap Content Requirements

Create these files with generic content only:

- `10_Dashboard/Home.md`
- `10_Dashboard/Projects Hub.md` with “No active projects yet.”
- `10_Dashboard/Agendas Hub.md` with “No open agendas yet.”
- `10_Dashboard/Decisions Hub.md` with “No decisions recorded yet.”
- `10_Dashboard/Tags & Ontology Hub.md`
- `00_Inbox/Inbox.md`
- `20_Life/20_Logs/YYYY/Life Log Index.md`
- `30_Knowledge/People/People Hub.md`
- `90_System/Agent Rules.md`
- `90_System/Ontology/Ontology Guide.md`
- `90_System/Ontology/Tag Registry.md`
- templates under `90_System/Templates/`

Do **not** create sample projects, sample people, sample family records, or sample decisions using real or invented names.

## Agent Rules File

The generated `90_System/Agent Rules.md` should be written in first-person ownership language, for example:

```markdown
# My SecondBrain Agent Rules

This is my personal SecondBrain and LLM Wiki. It starts empty and grows only from my own explicit records, sources, and decisions.

When I say “remember this,” “record this,” “save this,” “기억해,” “기록해,” or similar phrases, treat it as a SecondBrain write request.

Do not dump entire chats. Extract durable facts and organize them into projects, agendas, decisions, people, sources, logs, or concepts.

Search before writing. Reuse existing notes and tags when possible. Create new notes or tags only when needed.

After meaningful changes, refresh qmd and verify search when available.

Do not store passwords, authentication codes, tokens, cookies, API keys, or card security values.
```

## Template Frontmatter

All templates should include at least:

```yaml
---
schema: personal-secondbrain-v1
type:
domain: life
status:
area:
project:
people: []
source_doc: []
tags: []
created:
updated:
---
```

Recommended status values:

| type | status values |
|---|---|
| project | `active`, `waiting`, `paused`, `completed` |
| agenda | `open`, `waiting`, `resolved` |
| decision | `decided`, `deferred`, `rejected`, `superseded` |
| person | `active`, `inactive` |
| source | `captured`, `processed` |
| log | `recorded` |
| concept | `active`, `draft` |

## One-Shot Setup Recipe

Use the bundled [bootstrap script](scripts/bootstrap_personal_secondbrain.py) when available. The explicit link ensures Hermes URL installs fetch and security-scan the script together with this skill.

```bash
python3 scripts/bootstrap_personal_secondbrain.py "$OBSIDIAN_VAULT_PATH" --check
python3 scripts/bootstrap_personal_secondbrain.py "$OBSIDIAN_VAULT_PATH"
```

If the skill was installed without linked files, create the same folder/files manually from the sections above.

1. Install Obsidian if it is not installed.
2. Create an empty vault at the chosen path, e.g. `~/Documents/SecondBrain`.
3. Run the bootstrap script with `--check`, review the plan, then run it against the vault. A non-empty unmarked target is rejected unless the user explicitly approves `--allow-nonempty`.
4. Set the agent environment/config with the vault path, e.g. `OBSIDIAN_VAULT_PATH`.
5. Configure qmd to index only that vault.
6. Run qmd update/embed.
7. Search for `Agent Rules`, `Tag Registry`, and `Projects Hub` to verify indexing.
8. Test with 3 safe fake statements that do not contain real private data.
9. Verify each test creates/updates the correct note type and qmd can find the content.
10. Remove fake test notes if the vault must remain pristine after validation.

## Verification Tests

Use neutral test statements:

```text
Remember this: when choosing a refrigerator, width must be under 900 mm.
Record this: Teacher A is the homeroom teacher.
This is decided: for the next trip, prefer lodging within a 10-minute walk from the station.
```

Expected behavior:

- Purchase condition becomes agenda/project/concept plus source.
- Teacher context becomes person plus source.
- Lodging preference becomes agenda/project and decision/source as appropriate.
- Tags reuse the registry (`shopping`, `home`, `travel`, `person`, `source`) rather than inventing synonyms.
- qmd refresh runs after writes.
- Search can retrieve each record by a key phrase.

## Common Pitfalls

1. **Using third-person owner labels in reusable instructions.** The target agent should say “my SecondBrain,” not describe the vault from an outside perspective.
2. **Seeding another person's projects.** Never copy private projects, people, or decisions into a new personal vault.
3. **Date logs swallowing durable knowledge.** If a fact will matter later, update project/agenda/person/concept as the primary surface.
4. **Source notes treated as the main wiki.** Source notes preserve provenance; current usable knowledge belongs in the relevant main note.
5. **Tag sprawl.** Do not create `health`, `hospital`, `병원`, and `medical` for the same meaning.
6. **Forgetting qmd after edits.** A note that exists but is not indexed will feel missing to the agent.
7. **Claiming qmd success without verification.** If qmd fails, say so and keep the note path.
8. **Storing secrets.** Refuse or summarize safely when the content contains credentials or security material.
9. **Ignoring qmd collection-name collisions.** Verify that an existing collection resolves to the exact requested vault path; fail closed when it points elsewhere.
10. **Overwriting customized system files without recovery.** The bootstrap backs up managed files before `--overwrite`; report the backup path.

## Verification Checklist

- [ ] Vault starts with zero real projects, agendas, people, decisions, concepts, and sources.
- [ ] Folder skeleton exists.
- [ ] Hub files exist and say no records yet.
- [ ] Agent Rules uses first-person ownership language.
- [ ] Ontology Guide and Tag Registry exist.
- [ ] Templates exist for project, agenda, decision, person, source, log, and concept.
- [ ] `OBSIDIAN_VAULT_PATH` or equivalent config points to this vault only.
- [ ] qmd indexes only this vault.
- [ ] qmd update/embed completes or failure is reported.
- [ ] Search finds system files after qmd refresh.
- [ ] Test records route to the correct note types without tag duplication.
- [ ] No other user's private paths, names, projects, or notes were imported.
