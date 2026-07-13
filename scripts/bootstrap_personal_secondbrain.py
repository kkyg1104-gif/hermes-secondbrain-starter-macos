#!/usr/bin/env python3
"""Bootstrap an empty personal Obsidian SecondBrain / LLM Wiki vault.

This script creates structure, hub files, ontology files, templates, and first-person
Agent Rules only. It deliberately creates zero real projects, agendas, people,
decisions, concepts, or sources.
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
from pathlib import Path

SCHEMA = "personal-secondbrain-v1"


def frontmatter(type_: str, status: str, tags: list[str]) -> str:
    tag_text = ", ".join(tags)
    today = dt.date.today().isoformat()
    return f"""---
schema: {SCHEMA}
type: {type_}
domain: life
status: {status}
area:
project:
people: []
source_doc: []
tags: [{tag_text}]
created: {today}
updated: {today}
---
"""


def write_if_missing(path: Path, content: str, overwrite: bool = False) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return "exists"
    path.write_text(content, encoding="utf-8")
    return "written"


def template_body(type_: str, status: str, tags: list[str], title: str, sections: list[str]) -> str:
    body = [frontmatter(type_, status, tags), f"# {title}", ""]
    for section in sections:
        body.extend([f"## {section}", ""])
    return "\n".join(body).rstrip() + "\n"


def run_qmd_setup(vault: Path, collection: str) -> tuple[bool, list[str]]:
    """Best-effort qmd setup. Returns (success, log_lines)."""
    logs: list[str] = []
    qmd = shutil.which("qmd")
    if not qmd:
        return False, [
            "QMD_MISSING: qmd command not found.",
            "Install with: npm install -g @tobilu/qmd",
            "Then run:",
            f"  qmd collection add {vault} --name {collection}",
            f"  qmd context add qmd://{collection} 'My personal Obsidian SecondBrain / LLM Wiki.'",
            "  qmd update && qmd embed",
        ]

    commands = [
        [qmd, "collection", "add", str(vault), "--name", collection],
        [qmd, "context", "add", f"qmd://{collection}", "My personal Obsidian SecondBrain / LLM Wiki. It starts empty and grows from my own explicit records, sources, and decisions."],
        [qmd, "update"],
        [qmd, "embed"],
        [qmd, "status"],
        [qmd, "collection", "list"],
    ]

    success = True
    for cmd in commands:
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logs.append(f"$ {' '.join(cmd)}")
        output = (proc.stdout or "").strip()
        if output:
            logs.append(output)
        logs.append(f"exit={proc.returncode}")
        # collection/context may already exist; keep going but mark hard failures.
        if proc.returncode != 0 and cmd[1:3] not in (["collection", "add"], ["context", "add"]):
            success = False
    return success, logs


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an empty personal SecondBrain LLM Wiki vault skeleton.")
    parser.add_argument("vault", help="Path to the Obsidian vault to create/update")
    parser.add_argument("--year", type=int, default=dt.date.today().year, help="Year folder for logs/decisions")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing bootstrap files")
    parser.add_argument("--setup-qmd", action="store_true", help="Best-effort qmd collection/context/update/embed setup for this vault")
    parser.add_argument("--qmd-collection", default="my-secondbrain", help="qmd collection name to use with --setup-qmd")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    year = str(args.year)

    dirs = [
        "00_Inbox",
        "10_Dashboard",
        "20_Life/10_Projects",
        "20_Life/20_Agendas",
        f"20_Life/20_Logs/{year}",
        f"20_Life/30_Decisions/{year}",
        "30_Knowledge/People",
        "30_Knowledge/Concepts",
        "30_Knowledge/Sources/Message",
        "30_Knowledge/Sources/Image",
        "30_Knowledge/Sources/Document",
        "30_Knowledge/Sources/Web",
        "30_Knowledge/Assets",
        "40_Events/Calendar",
        "90_System/Templates",
        "90_System/Ontology",
    ]
    for d in dirs:
        (vault / d).mkdir(parents=True, exist_ok=True)

    files: dict[str, str] = {}

    files["00_Inbox/Inbox.md"] = template_body(
        "inbox", "active", ["system", "inbox"], "Inbox", ["Unrouted Notes"]
    ) + "This inbox starts empty. Route durable records into projects, agendas, decisions, people, sources, logs, or concepts.\n"

    files["10_Dashboard/Home.md"] = frontmatter("dashboard", "active", ["system", "dashboard"]) + """# Home

This is my personal SecondBrain and LLM Wiki.

## How I use this

I can ask my agent:

- “remember this”
- “record this”
- “save this”
- “기억해”
- “기록해”
- “세컨브레인에 넣어줘”

The agent should organize durable information into projects, agendas, decisions, people, sources, logs, or concepts.

## Hubs

- [[Projects Hub]]
- [[Agendas Hub]]
- [[People Hub]]
- [[Decisions Hub]]
- [[Tags & Ontology Hub]]

## Recent important notes

No records yet.
"""

    files["10_Dashboard/Projects Hub.md"] = frontmatter("hub", "active", ["system", "dashboard", "project"]) + """# Projects Hub

## Active Projects

No active projects yet.

## Waiting / Paused

No waiting or paused projects yet.

## Completed

No completed projects yet.
"""

    files["10_Dashboard/Agendas Hub.md"] = frontmatter("hub", "active", ["system", "dashboard", "agenda"]) + """# Agendas Hub

## Open Agendas

No open agendas yet.

## Waiting

No waiting agendas yet.

## Resolved

No resolved agendas yet.
"""

    files["10_Dashboard/People Hub.md"] = frontmatter("hub", "active", ["system", "dashboard", "person"]) + """# People Hub

No people recorded yet.
"""

    files["10_Dashboard/Decisions Hub.md"] = frontmatter("hub", "active", ["system", "dashboard", "decision"]) + """# Decisions Hub

## Recent Decisions

No decisions recorded yet.
"""

    files["10_Dashboard/Tags & Ontology Hub.md"] = frontmatter("hub", "active", ["system", "dashboard", "ontology"]) + """# Tags & Ontology Hub

- [[Ontology Guide]]
- [[Tag Registry]]

Use existing note types and tags before creating new ones.
"""

    files[f"20_Life/20_Logs/{year}/Life Log Index.md"] = frontmatter("hub", "active", ["system", "log"]) + f"""# {year} Life Log Index

No logs yet.
"""

    files["30_Knowledge/People/People Hub.md"] = frontmatter("hub", "active", ["system", "person"]) + """# People Hub

No people recorded yet.
"""

    files["90_System/Agent Rules.md"] = frontmatter("system", "active", ["system", "rules"]) + """# My SecondBrain Agent Rules

This is my personal SecondBrain and LLM Wiki. It starts empty and grows only from my own explicit records, sources, and decisions.

When I say “remember this,” “record this,” “save this,” “기억해,” “기록해,” “저장해,” “나중에 참고하게 해줘,” or similar phrases, treat it as a SecondBrain write request.

Do not dump entire chats. Extract durable facts and organize them into projects, agendas, decisions, people, sources, logs, or concepts.

## Recording workflow

1. Extract the durable fact, preference, decision, person, source, or next action.
2. Search existing notes before writing.
3. Reuse existing project, agenda, person, concept, decision, and tag records when possible.
4. Create new notes only when no existing note fits.
5. Keep source notes concise and use them for provenance.
6. Keep current usable knowledge in project, agenda, person, or concept notes.
7. After meaningful changes, refresh qmd and verify search when available.

## Tag policy

Search [[Tag Registry]] before adding tags. Reuse existing tags. Create a new tag only if it is a genuinely reusable classification signal.

## Secret policy

Do not store passwords, authentication codes, tokens, cookies, API keys, OAuth/device codes, or card security values.
"""

    files["90_System/Ontology/Ontology Guide.md"] = frontmatter("system", "active", ["system", "ontology"]) + """# Ontology Guide

| type | Meaning | Create when |
|---|---|---|
| `project` | Continuing effort | The topic has state, goals, constraints, or next actions |
| `agenda` | Recurring issue/question | It should stay visible but is not yet a project |
| `decision` | Choice, rejection, deferral, priority change | A direction has changed or been chosen |
| `person` | Person/relationship/contact | The person is likely to recur |
| `source` | Message/image/document/web evidence | Provenance matters |
| `log` | Date-specific event | The date is the main organizing key |
| `concept` | Reusable knowledge/rule/preference | It should be searchable beyond one project |
"""

    files["90_System/Ontology/Tag Registry.md"] = frontmatter("registry", "active", ["system", "ontology", "tags"]) + """# Tag Registry

## Principles

1. Search before adding a new tag.
2. Reuse existing tags for synonyms.
3. Prefer English lowercase kebab-case.
4. People, project names, and locations should be wikilinks/frontmatter, not tags.

## Starter Tags

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

## Alias / Do Not Duplicate

| Do not create | Use instead |
|---|---|
| `생활` | `life` |
| `가족` | `family` |
| `건강`, `병원` | `health` |
| `구매`, `쇼핑` | `shopping` |
| `여행` | `travel` |
| `돈`, `비용` | `finance` |
| `메모` | Use `type` and note content |
"""

    templates = {
        "Project.md": ("project", "active", ["life", "project"], "{{title}}", ["One-line Summary", "Current State", "Important Context", "People", "Decisions / Change History", "Next Actions", "Related Sources"]),
        "Agenda.md": ("agenda", "open", ["life", "agenda"], "{{title}}", ["Agenda Summary", "Background", "Current Questions", "Options", "To Check", "Related Notes"]),
        "Decision.md": ("decision", "decided", ["life", "decision"], "{{title}}", ["Decision", "Reason", "Options Considered", "Risks / Cautions", "Follow-up", "Sources"]),
        "Person.md": ("person", "active", ["person", "life"], "{{name}}", ["Relationship", "Contact", "Important Context", "Related Notes"]),
        "Source_Message.md": ("source", "captured", ["life", "source", "message"], "{{title}}", ["Source Summary", "Key Facts", "Linked Project / Agenda", "Follow-up Needed"]),
        "Source_Image.md": ("source", "captured", ["life", "source", "image"], "{{title}}", ["Image Summary", "Visible Facts", "Linked Notes", "Follow-up Needed"]),
        "Source_Document.md": ("source", "captured", ["life", "source", "document"], "{{title}}", ["Document Summary", "Key Facts", "Linked Notes", "Follow-up Needed"]),
        "Source_Web.md": ("source", "captured", ["life", "source", "web"], "{{title}}", ["Web Summary", "Key Facts", "URL", "Linked Notes", "Follow-up Needed"]),
        "Log.md": ("log", "recorded", ["life", "log"], "{{date}}", ["What Happened", "Why It Matters", "Linked Notes", "Follow-up"]),
        "Concept.md": ("concept", "active", ["life", "concept"], "{{title}}", ["Definition", "Useful Rule", "Examples", "Related Notes"]),
    }
    for filename, spec in templates.items():
        type_, status, tags, title, sections = spec
        files[f"90_System/Templates/{filename}"] = template_body(type_, status, tags, title, sections)

    written = 0
    existing = 0
    for rel, content in files.items():
        result = write_if_missing(vault / rel, content, overwrite=args.overwrite)
        if result == "written":
            written += 1
        else:
            existing += 1

    print(f"VAULT={vault}")
    print(f"DIRS_CREATED_OR_PRESENT={len(dirs)}")
    print(f"FILES_WRITTEN={written}")
    print(f"FILES_EXISTING_SKIPPED={existing}")
    print("REAL_PROJECTS_CREATED=0")
    print("REAL_AGENDAS_CREATED=0")
    print("REAL_PEOPLE_CREATED=0")
    print(f"REAL_DECISIONS_CREATED=0")
    if args.setup_qmd:
        ok, qmd_logs = run_qmd_setup(vault, args.qmd_collection)
        print(f"QMD_COLLECTION={args.qmd_collection}")
        print(f"QMD_SETUP_SUCCESS={str(ok).lower()}")
        print("QMD_LOG_START")
        for line in qmd_logs:
            print(line)
        print("QMD_LOG_END")
    else:
        print("QMD_SETUP_SKIPPED=true")
        print(f"NEXT: configure qmd for this vault only, then run: qmd collection add {vault} --name my-secondbrain && qmd update && qmd embed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
