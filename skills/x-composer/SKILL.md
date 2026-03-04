---
name: x-composer
version: 3.0.0
description: Compose and post to X.com using browser automation. Use when user asks to "post to X", "tweet", "draft a tweet", "share on X", or "write a thread". Supports Playwright MCP (recommended), CDP, and clipboard fallback.
---

# X Composer

Post to X.com via browser automation. No API key required.

## Mode Priority

1. **Playwright MCP (recommended)** — Headless, most reliable, supports image upload
2. **CDP mode** — Auto-scans ports 9222-9230 for Chrome CDP
3. **Clipboard fallback** — Copies to clipboard and pastes via AppleScript

## Playwright MCP Mode (Recommended)

Use Playwright MCP tools directly. Handles text, images, and posting without visible browser.

### Post with text only

```
1. browser_navigate → https://x.com/compose/post
2. browser_snapshot → find textbox ref
3. browser_run_code → force click textbox, keyboard.type(content, {delay: 10})
4. browser_take_screenshot → verify draft
5. Ask user confirmation
6. browser_run_code → page.locator('[data-testid="tweetButton"]').dispatchEvent('click')
```

### Post with image

```
1. Type content (same as above)
2. browser_run_code → page.locator('input[type="file"][accept*="image"]').first().setInputFiles('/path/to/image.png')
3. browser_take_screenshot → verify image attached
4. Post after confirmation
```

### Key notes

- X.com has an overlay that blocks normal clicks — always use `{ force: true }` or `dispatchEvent('click')`
- To clear text: `Cmd+A` then `Backspace` via `page.keyboard`
- Login persists in Playwright session — if not logged in, user must log in once manually
- `fill()` can cause duplicate text — prefer `keyboard.type()` with delay

## CDP Mode (Fallback)

### Quick Post

```bash
bash scripts/x-post.sh "Your post content here"
```

### CDP Auto Port Detection

- Scans ports 9222-9230 for existing Chrome CDP (verifies it's Chrome, not Electron apps)
- Finds first available port to launch new Chrome instance
- Saves active port to `~/.chrome-cdp-port`

### Individual Scripts

```bash
# Open compose page
NODE_PATH=$(npm root -g) node scripts/cdp-launch.js [URL]

# Type text
echo '[{"text":"Hello"},{"enter":true},{"text":"World"}]' | NODE_PATH=$(npm root -g) node scripts/cdp-type.js
```

### Clipboard Fallback

If CDP is unavailable (Chrome already running without debugging):
1. Copies text to clipboard via `pbcopy`
2. Focuses Chrome via AppleScript
3. Pastes via Cmd+V

## Prerequisites

- Playwright MCP: `playwright` MCP server configured
- CDP mode: `npm install -g chrome-remote-interface`

## Rules

- **NEVER auto-post** — always show draft and ask user for confirmation
- If X.com requires login, inform user to log in manually
- Take screenshot to verify content before posting
- For image posts, verify image is attached before posting

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Overlay blocks clicks | Use `{ force: true }` or `dispatchEvent('click')` |
| `fill()` duplicates text | Use `keyboard.type()` with `{ delay: 10 }` instead |
| Port 9222 occupied | Auto-handled — scans 9222-9230 |
| Not logged in | User must log in manually once, session persists |
