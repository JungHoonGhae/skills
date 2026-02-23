---
name: oh-my-lilys
description: CLI tool for lilys.ai - Summarize YouTube, PDF, websites, and audio. Use when user wants to: (1) Summarize content from URLs, (2) List digest sessions, (3) Generate/fetch AI reports with different note types, (4) Manage authentication. Triggers: "summarize URL", "generate report", "get sessions", "lilys", "YouTube summary".
compatibility: npm, pnpm, or bun for global installation. Requires playwright-cli for auto-auth.
---

# oh-my-lilys

CLI tool for lilys.ai to summarize YouTube, PDF, websites, and audio directly from your terminal.

## Installation

```bash
npm install -g oh-my-lilys
# or
pnpm add -g oh-my-lilys
# or
bun add -g oh-my-lilys
```

### Prerequisites for Auto-Auth

For automatic token retrieval, install playwright-cli:

```bash
npm install -g playwright-cli
```

## Usage

```bash
# Authenticate (auto-detect from browser)
lilys auth

# Or manually with token
lilys auth <token>

# Check status
lilys whoami

# Summarize URL
lilys summarize <url>

# List sessions
lilys sessions

# Get report
lilys report <sessionId>

# Generate report with specific note type and wait for completion
lilys report <sessionId> --note-type detailed --watch --timeout 180

# Export report as markdown
lilys report <sessionId> --export markdown

# Set language
lilys lang ko

# Run diagnostics
lilys doctor

# Check for updates
lilys upgrade
```

## Commands

| Command   | Description                                       |
| --------- | ------------------------------------------------- |
| auth      | Authenticate with lilys.ai (auto or manual token) |
| summarize | Summarize a URL (YouTube, PDF, audio, website)    |
| sessions  | List your digest sessions                         |
| report    | Get report for a session                          |
| lang      | Get/set AI result language                        |
| doctor    | Diagnose and fix issues                           |
| upgrade   | Check for new versions                            |
| logout    | Clear stored credentials                          |
| whoami    | Check authentication status                       |

## Report Options

| Option               | Description                        |
| -------------------- | ---------------------------------- |
| --note-type <type>   | Generate specific note type        |
| --watch              | Watch for report completion (poll) |
| --timeout <seconds>  | Watch timeout (default: 120)       |
| --export markdown    | Export as markdown file            |

## Note Types

| Type        | Description          |
| ----------- | -------------------- |
| detailed    | Full detailed report |
| key_points  | Key points           |
| easy        | Easy summary         |
| script      | Script               |
| animation   | Animation            |
| infographic | Infographic          |
| background  | Background           |
| deep_dive   | Deep analysis        |

## Authentication

### Automatic (Recommended)

```bash
lilys auth
```

This will:
1. Check if you're already logged in at lilys.ai
2. If logged in, automatically extract the token from browser
3. If not logged in, open a browser for you to login with Google
4. Save the token for future use

The browser profile is stored at ~/.lilys-chrome-profile.

### Manual

```bash
# Get token manually:
# 1. Open https://lilys.ai in your browser
# 2. Log in with Google
# 3. Open DevTools (F12) → Application → Local Storage
# 4. Copy the 'access_token' value
# 5. Run: lilys auth <token>
```

## Error Handling

- **Auth errors**: Automatically detected (401/403/invalid_token). Prompts re-authentication.
- **Note generation timeout**: 504 errors don't fail - generation continues in background.
- **Watch mode**: Polls every 3 seconds until report is ready or timeout.

## Examples

```bash
# Auto-authenticate
lilys auth

# Summarize a YouTube video
lilys summarize https://youtube.com/watch?v=abc123

# List all sessions
lilys sessions

# Get existing report
lilys report 8260019

# Generate new detailed report and wait
lilys report 8260019 --note-type detailed --watch --timeout 180

# Export report as markdown file
lilys report 8260019 --export markdown
```

## Disclaimer

This tool reverse-engineers the lilys.ai API. Use at your own risk. Automated usage may violate lilys.ai's Terms of Service.
