---
name: x-composer
version: 2.0.0
description: Compose and post to X.com using browser automation. Use when user asks to "post to X", "tweet", "draft a tweet", "share on X", or "write a thread". Works with claude-in-chrome MCP (preferred, no setup) or CDP scripts (fallback).
---

# X Composer

Post to X.com via browser automation. Two modes:

1. **MCP mode** (preferred) — Uses claude-in-chrome MCP. No extra setup, uses existing browser.
2. **CDP mode** (fallback) — Uses CDP scripts when MCP is unavailable.

## MCP Mode (preferred)

Requires `claude-in-chrome` MCP server connected. No Chrome launch, no npm packages.

### Workflow

1. Get browser context: `mcp__claude-in-chrome__tabs_context_mcp`
2. Create new tab: `mcp__claude-in-chrome__tabs_create_mcp`
3. Navigate to compose: `mcp__claude-in-chrome__navigate` → `https://x.com/compose/post`
4. Wait for page load: `mcp__claude-in-chrome__browser_wait_for` (~3s)
5. Find compose box: `mcp__claude-in-chrome__find` → "compose text input" or "What is happening"
6. Type the post: `mcp__claude-in-chrome__form_input` or `mcp__claude-in-chrome__computer` with action `type`
7. **Ask user for confirmation before posting**
8. Click Post button: `mcp__claude-in-chrome__find` → "Post button", then `mcp__claude-in-chrome__computer` with action `left_click`

### Implementation Steps

```
1. tabs_context_mcp → get existing tabs
2. tabs_create_mcp → new tab
3. navigate(url: "https://x.com/compose/post", tabId: <tab>)
4. Wait 3 seconds for page load
5. Take screenshot to verify compose box is visible
6. find(query: "post text input", tabId: <tab>) → get compose box ref
7. computer(action: "left_click", ref: <compose_ref>, tabId: <tab>) → focus
8. computer(action: "type", text: "<post content>", tabId: <tab>) → type text
9. Take screenshot → show draft to user
10. ASK USER: "Post this to X?" — NEVER auto-post
11. If approved: find "Post button" → click
12. Verify post was published via screenshot
```

### Multi-line Posts

Use `\n` in the type text, or type in segments with Enter key presses between them:

```
computer(action: "type", text: "First line", tabId: <tab>)
computer(action: "key", text: "Enter", tabId: <tab>)
computer(action: "type", text: "Second line", tabId: <tab>)
```

### Thread Posts

After posting the first tweet:
1. Find "Add another post" or reply box
2. Type next tweet content
3. Confirm with user → click Post
4. Repeat

## CDP Mode (fallback)

Use when claude-in-chrome MCP is not available. Requires Chrome and `chrome-remote-interface`.

### Prerequisites

```bash
npm install -g chrome-remote-interface
```

### Workflow

```bash
# Step 1: Launch Chrome with CDP
NODE_PATH=$(npm root -g) node scripts/cdp-launch.js

# Step 2: Wait ~3s, then type draft
echo '[{"text":"Hello world!"}]' | NODE_PATH=$(npm root -g) node scripts/cdp-type.js

# Step 3: User reviews and clicks Post manually
```

### Segment Format (CDP)

| Segment | Effect |
|---------|--------|
| `{"text": "string"}` | Insert text (emoji/unicode safe) |
| `{"enter": true}` | Single line break |
| `{"enter": 2}` | Multiple line breaks |

### Example: Multi-paragraph post (CDP)

```bash
cat << 'EOF' | NODE_PATH=$(npm root -g) node scripts/cdp-type.js
[
  {"text": "Hook line"},
  {"enter": 2},
  {"text": "Main content."},
  {"enter": 2},
  {"text": "#hashtag"}
]
EOF
```

## Mode Selection

The agent should auto-select the mode:

1. Check if `mcp__claude-in-chrome__tabs_context_mcp` tool is available
2. If yes → use MCP mode (no setup needed)
3. If no → fall back to CDP mode (run scripts)

## Rules

- **NEVER auto-post** — always show draft and ask user for confirmation before clicking Post
- If X.com requires login, inform the user to log in manually
- Verify post content via screenshot before confirming
- Handle emoji and unicode text properly

## Troubleshooting

| Issue | Fix |
|-------|-----|
| MCP not connected | Fall back to CDP mode |
| X.com login required | User must log in manually in browser |
| Compose box not found | Take screenshot, try clicking the text area manually |
| CDP Chrome not connecting | `pkill -f "Chrome.*remote-debugging"` then relaunch |
| CDP module not found | `npm install -g chrome-remote-interface` |
