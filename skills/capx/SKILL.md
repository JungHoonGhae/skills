---
name: capx
description: >
  Unofficial CLI for Capacities.io — manage your knowledge base from the terminal using the `capx`
  command. Use this skill whenever the user mentions Capacities, capx, or wants to:
  create/update/search objects in Capacities, manage tasks and projects, register information from
  screenshots or messages into Capacities, archive completed tasks, save weblinks, write daily notes,
  or manage organizations and people. Also trigger when the user pastes a screenshot of chat messages
  (Slack, KakaoTalk, Teams, etc.) and wants to register or log that information, or when the user
  mentions "capacities" in any context related to note-taking or knowledge management.
---

# capx — Unofficial CLI for Capacities.io

`capx` is a Rust CLI for managing your [Capacities.io](https://capacities.io) knowledge base from the terminal. It wraps the Capacities Portal API and supports full CRUD on objects, tasks, daily notes, weblinks, and more.

> **Disclaimer**: This project is not affiliated with or endorsed by Capacities. "Capacities" is a trademark of Capacities GmbH.

## Setup

### Installation

```bash
cargo install --git https://github.com/user/capx
```

Or clone and build locally:

```bash
git clone https://github.com/user/capx && cd capx && cargo build --release
```

### Authentication

`capx` reads the auth token automatically from the Capacities desktop app's cookie database. Just make sure the Capacities app is installed and you're logged in.

Alternatively, set the `CAP_TOKEN` environment variable:

```bash
export CAP_TOKEN="your-auth-token"
```

### Space Selection

The CLI auto-selects your first space. Override with:

```bash
export CAP_SPACE_ID="your-space-uuid"
# or per-command:
capx spaces  # find your space ID
capx search "query" --space-id <uuid>
```

## Command Reference

### Discovery

| Command | Usage | Purpose |
|---------|-------|---------|
| `spaces` | `capx spaces` | List all workspaces |
| `whoami` | `capx whoami` | Check auth status |
| `search` | `capx search "query" --limit 20` | Full-text search |
| `types` | `capx types` | List object types and their properties |
| `ls` | `capx ls` or `capx ls -t Page -t Person` | List objects, optionally filtered by type |
| `get` | `capx get <id> [<id2>...]` | View formatted objects |
| `get --raw` | `capx get <id> --raw` | Raw API response (useful for inspecting property values) |

### CRUD

| Command | Usage |
|---------|-------|
| `create` | `capx create <Type> "Title" -d "desc" -b "body" -p key=value --context "term"` |
| `update` | `capx update <id> -t "title" -d "desc" -b "body" -p key=value` |
| `rm` | `capx rm <id> --yes` |
| `undo` | `capx undo <id>` |
| `dup` | `capx dup <id>` |
| `trash` | `capx trash` |

### Specialized

| Command | Usage |
|---------|-------|
| `task` | `capx task "Title" -b "body" -p status=next-up -p priority=high -c "context"` |
| `daily` | `capx daily "markdown text"` or `capx daily "text" --no-timestamp` |
| `link` | `capx link "https://..." -t "Title" -d "desc"` |
| `context` | `capx context <object-id> "search term" [<uuid>...]` |

### Global Flags

- `--json` — JSON output for scripting
- `--space-id <UUID>` — Override auto-detected space

## Object Types

Run `capx types` to see the user's actual schema. Capacities ships with built-in types, and users can create custom ones. Common built-in types:

- **Organization** — Relation (label), Category (label), CEO (entity→Person), Employee (entity→Person), Contact Information (blocks), Website (entity→WebResource)
- **Project** — Status (label: Planned/In Progress/Completed/On Hold), Client Company (entity→Organization), Time frame (datetime)
- **Person** — Can be linked to Organization as CEO/Employee
- **Task** (RootTask) — status, priority, date, notes
- **Page**, **Idea**, **Atomic note**, **Meeting**, **Place**

Always run `capx types` first to discover the user's actual types and property names — custom types vary by user.

## Property Types

The `-p key=value` flag auto-normalizes values based on the property's data type:

| Type | Example | Behavior |
|------|---------|----------|
| **label** | `-p status=done` | Case-insensitive match against defined options |
| **entity** | `-p CEO=<uuid>` | Links to another entity by UUID |
| **blocks** | `-p "Notes=## Heading\n- item"` | Markdown → Capacities block format |
| **datetime** | `-p date=2026-03-15` | Parses to ISO datetime |
| **string** | `-p title="New Title"` | Plain text |

## Context Linking

`--context` (on `create`, `task`) and the `context` command accept UUIDs or search terms. Search terms auto-resolve to the best match:

```bash
# Search term — auto-resolves
capx task "Review contract" --context "Acme Corp"

# UUID
capx context <object-id> 7ccca7ef-5c1f-4bf6-a098-4d50de921b20

# Multiple
capx create Project "Website Redesign" --context "Acme Corp" --context "Design Team"
```

## Workflow Patterns

### Registering information from screenshots or messages

When the user shares a screenshot (Slack, KakaoTalk, Teams, email, etc.) and wants to log it:

1. **Extract** key information from the image: who said what, dates, action items, project names
2. **Search** for existing entities: `capx search "company or project name"`
3. **Create missing entities** in dependency order:
   - Organization (if new): `capx create Organization "Name" -p Relation=Client -p Category=Company`
   - Person: `capx create Person "Name" -d "Role at Company" --context "Company Name"`
   - Project: `capx create Project "Name" -p Status="In Progress" --context "Company Name"`
4. **Create task(s)** with structured body and context links:
   ```bash
   capx task "[Project] Task description" \
     -b "$(cat <<'EOF'
   ## Source
   - Key point from message
   - Action item with deadline
   - People involved
   EOF
   )" \
     -p status=next-up -p priority=high \
     --context "Project Name"
   ```
5. **Enrich entities** — search the web for company details, then fill in properties:
   ```bash
   capx update <org-id> -d "Brief description" -b "## Details..."
   capx update <org-id> -p CEO=<person-uuid> -p Website=<weblink-uuid>
   ```

The dependency order matters because `--context` resolves search terms at creation time — the target entity must already exist.

### Archiving completed tasks

1. **Search**: `capx search "project name"` to find related tasks
2. **Inspect**: `capx get <id1> <id2> ... --raw` to check current status values
3. **Identify**: look for `"status": {"val": ["done"]}` in the raw output
4. **Archive**: `capx update <id> -p status=archived` for each completed task
5. Run updates in parallel when archiving multiple tasks

### Building a complete company profile

1. `capx create Organization "Acme Corp" -p Relation=Client -p Category=Company`
2. Search the web for company info (CEO name, address, phone, website URL)
3. `capx create Person "Jane Doe" -d "CEO of Acme Corp"`
4. `capx link "https://acme.com" -t "Acme Corp Website"`
5. Wire everything together:
   ```bash
   capx update <org-id> \
     -d "Short company description" \
     -b "$(cat <<'EOF'
   ## Company Info
   - **Founded**: 2015
   - **Employees**: 50
   - **Address**: 123 Main St

   ## Contact
   - **Phone**: 555-0100
   - **Email**: info@acme.com
   EOF
   )" \
     -p CEO=<person-uuid> \
     -p Employee=<person-uuid> \
     -p Website=<weblink-uuid> \
     -p "Contact Information=**Phone**: 555-0100\n**Email**: info@acme.com"
   ```

### Daily notes

```bash
# Timestamped entry (default)
capx daily "Had sync with design team. Agreed on new dashboard layout."

# Multi-line, no timestamp
capx daily "$(cat <<'EOF'
## Sprint Review
- Completed auth module
- Started API integration
- Blocked on database migration
EOF
)" --no-timestamp
```

## Task Properties

| Property | Values |
|----------|--------|
| **status** | `not-started`, `next-up`, `in-progress`, `done`, `archived` |
| **priority** | `low`, `medium`, `high` |
| **date** | ISO date (e.g., `2026-03-15`) |

## Tips

- Create entities in dependency order: Organization → Person → Project → Task (so context links resolve)
- Use `--raw` with `get` to see actual property structures when debugging
- `--context` accepts plain search terms — no need to look up UUIDs first
- Body (`-b`) supports markdown: headings, bold, italic, code blocks, links, tables
- Use heredoc `$(cat <<'EOF' ... EOF)` for multi-line body content
- Batch operations: pass multiple IDs to `get` for efficient retrieval
- All commands support `--json` for scripting and piping
