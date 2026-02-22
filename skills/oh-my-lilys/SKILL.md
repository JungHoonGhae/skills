---
name: oh-my-lilys
description: CLI tool for lilys.ai - Summarize YouTube, PDF, websites, and audio. Use when user wants to summarize content from URLs, manage digest sessions, or generate AI reports.
version: 1.1.0
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

# Set language
lilys lang ko

# Run diagnostics
lilys doctor

# Check for updates
lilys upgrade
```

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

## Commands

- **auth** - Authenticate with lilys.ai (auto or manual token)
- **summarize** - Summarize a URL (YouTube, PDF, audio, website)
- **sessions** - List your digest sessions
- **report** - Get report for a session
- **lang** - Get/set AI result language
- **doctor** - Diagnose and fix issues
- **upgrade** - Check for new versions
- **logout** - Clear stored credentials
- **whoami** - Check authentication status

## Note Types

- detailed - Full detailed summary
- key_points - Key points
- easy - Easy summary
- script - Script
- animation - Animation
- infographic - Infographic
- background - Background
- deep_dive - Deep analysis

## Disclaimer

This tool reverse-engineers the lilys.ai API. Use at your own risk. Automated usage may violate lilys.ai's Terms of Service.
