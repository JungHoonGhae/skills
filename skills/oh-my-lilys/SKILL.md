---
name: "oh-my-lilys"
description: "CLI tool for lilys.ai - Summarize YouTube, PDF, websites, and audio. Manage sessions, generate reports, search, export, and organize collections directly from the terminal. Use when user wants to summarize content from URLs, list/search/delete sessions, generate or fetch AI reports with note types, export reports as PDF or Markdown, manage collections, share sessions publicly, check usage/quota, or authenticate with lilys.ai. Triggers: summarize URL, generate report, get sessions, lilys, YouTube summary, search sessions, export PDF, collections."
---

# oh-my-lilys

CLI tool for lilys.ai.

## Installation

```bash
npm install -g oh-my-lilys
# or
bun add -g oh-my-lilys
```

## Authentication

```bash
# Auto-extract token from browser (Chrome, Arc, Dia, Brave, Edge)
lilys auth

# Manual with token
lilys auth <token>
```

## Commands

| Command | Description |
|---------|-------------|
| `auth` | Authenticate (auto browser extraction or manual token) |
| `summarize <url>` | Summarize a URL (YouTube, PDF, website, audio) |
| `sessions` | List all sessions |
| `search <keyword>` | Search sessions by keyword |
| `delete <id>` | Delete a session (`--yes` to skip confirm) |
| `report <id>` | Fetch or generate a report |
| `usage` | Show plan usage and quota |
| `share <id>` | Create public share link |
| `unshare <id>` | Remove public sharing |
| `export-pdf <id>` | Export report as PDF (`--output file.pdf`) |
| `collections` / `col` | Manage collections |
| `lang [code]` | Get/set AI result language |
| `whoami` | Check authentication status |
| `doctor` | Diagnose issues |
| `upgrade` | Check for updates |

## Report Generation

```bash
lilys report <id>                              # Fetch latest report
lilys report <id> --note-type detailed --watch # Generate & wait
lilys report <id> --note-type key_points       # Key report
lilys report <id> --generate textbook          # SSE streaming
lilys report <id> --export markdown            # Export as .md
```

**Note types:** `detailed`, `key_points`, `easy`, `script`, `animation`, `infographic`, `background`, `deep_dive`

## Collections

```bash
lilys col                                    # List collections
lilys col create "My Collection"             # Create
lilys col rename <col-id> "New Name"         # Rename
lilys col move <col-id> <session-id...>      # Move sessions in
lilys col delete <col-id>                    # Delete
```

## Examples

```bash
lilys auth
lilys summarize https://youtube.com/watch?v=abc123
lilys sessions
lilys search "machine learning" --limit 5
lilys report 8260019 --note-type detailed --watch
lilys report 8260019 --export markdown
lilys usage --json
lilys share 8260019
lilys export-pdf 8260019 --output report.pdf
lilys lang ko
```

## Error Handling

- **Auth errors**: Auto-detected (401/403), prompts re-authentication
- **Watch mode**: Polls every 3s until ready or timeout (default 120s)
- **Note generation timeout**: 504 errors don't fail — generation continues in background

## Disclaimer

This tool reverse-engineers the lilys.ai API. Use at your own risk.
