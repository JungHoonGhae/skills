---
name: capacities-cli
description: >
  Unofficial CLI for Capacities.io — manage your knowledge base from the terminal using the `capx`
  command. Use this skill whenever the user mentions Capacities, capacities-cli, capx, or wants to:
  create/update/search objects in Capacities, manage tasks and projects, register information from
  screenshots or messages into Capacities, archive completed tasks, save weblinks, write daily notes,
  or manage organizations and people. Also trigger when the user pastes a screenshot of chat messages
  (Slack, KakaoTalk, Teams, etc.) and wants to register or log that information, or when the user
  mentions "capacities" in any context related to note-taking or knowledge management.
---

# capacities-cli — Unofficial CLI for Capacities.io

`capacities-cli` is a Rust CLI (command: `capx`) for managing your [Capacities.io](https://capacities.io) knowledge base from the terminal. It wraps the Capacities Portal API and supports full CRUD on objects, tasks, daily notes, weblinks, and more.

> **Disclaimer**: This project is not affiliated with or endorsed by Capacities. "Capacities" is a trademark of Capacities GmbH.

## Setup

### Installation

```bash
cargo install capacities-cli
```

Or clone and build locally:

```bash
git clone https://github.com/JungHoonGhae/capacities-cli && cd capacities-cli && cargo build --release
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
| `daily get` | `capx daily get` — Read today's daily note |
| `daily delete` | `capx daily delete --last 1 --yes` — Delete last block |
| `daily delete` | `capx daily delete --marker "text" --yes` — Delete blocks containing text |
| `daily set` | `capx daily set -b "# New content" --yes` — Replace entire daily note |
| `link` | `capx link "https://..." -t "Title" -d "desc"` |
| `context` | `capx context <object-id> "search term" [<uuid>...]` |

### Export & Edit

| Command | Usage |
|---------|-------|
| `export` | `capx export` — Export all objects as markdown to stdout |
| `export` | `capx export -t Page --format json` — Export Pages as JSON |
| `export` | `capx export -o ./backup` — Export to directory |
| `edit` | `capx edit <id>` — Edit object in `$EDITOR` |

### Diagnostics

| Command | Usage |
|---------|-------|
| `auth` | `capx auth` — Check authentication status |
| `doctor` | `capx doctor` — Check API connection, auth, and config |
| `completions` | `capx completions bash` — Generate shell completions (bash/zsh/fish) |

### Global Flags

- `--json` — JSON output for scripting
- `--space-id <UUID>` — Override auto-detected space
- `--appversion <VER>` — Override Portal API app version (or set `CAP_APPVERSION`)
- `--portal-url <URL>` — Override Portal API base URL (or set `CAP_PORTAL_URL`)

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

### Enriching organization notes from external data

When syncing information from emails, CRM, or other sources into an Organization's notes:

1. **Gather data** from external source (emails, project files, etc.)
2. **Update notes** with structured markdown — contacts, activity timeline, pending items:
   ```bash
   capx update <org-id> -b "$(cat <<'EOF'
   ## Contacts
   | Name | Role | Email |
   |------|------|-------|
   | Jane Doe | CEO | jane@acme.com |
   | John Smith | CTO | john@acme.com |

   ## Recent Activity
   - **2026-03**: SSL certificate renewed
   - **2026-02**: API credentials migrated

   ## Pending Items
   - Contract renewal due Q2
   EOF
   )"
   ```

Note: `-b` replaces the entire notes body. To preserve existing notes, read first with `capx get <id>` and merge content.

### Bulk updating tasks

When updating multiple tasks (e.g., reconciling statuses from email evidence), run updates in parallel for efficiency:

```bash
# Update statuses in parallel
capx update <id1> -p status=done &
capx update <id2> -p status=done &
capx update <id3> -p status=in-progress &
wait
```

Or from a script, loop through IDs:

```bash
for id in <id1> <id2> <id3>; do
  capx update "$id" -p status=done
done
```

**Important**: Only pass the properties you intend to change. Extra `-p` flags overwrite existing values — omitting a property leaves it unchanged.

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

## Gotchas

- **`get` with multiple task IDs may fail**: `capx get <id1> <id2>` can return "No objects found" for RootTask entities. Workaround: get tasks individually with `capx get <id> --raw`.
- **Empty status arrays**: Some tasks have `"status": {"val": []}` (no status set) in raw output. Handle this in scripts with fallback defaults.
- **`-p date=` sets date resolution to day**: When setting task dates, use ISO format (`2026-03-15`). Omitting `-p date=` on update leaves the existing date unchanged.
- **`-b` replaces entire notes**: The body flag overwrites all existing notes/blocks content. There is no append mode — read existing content first if you need to merge.
