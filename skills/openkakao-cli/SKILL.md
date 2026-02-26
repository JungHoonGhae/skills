---
name: openkakao-cli
description: Work with OpenKakao CLI (`openkakao-rs`) for read-only KakaoTalk workflows on macOS. Use when user asks to install OpenKakao, authenticate token, list chats, read messages, inspect friends/members/profile/settings, debug `-950` token errors, or build automation/reporting pipelines from chat data.
---

# OpenKakao CLI

Use `openkakao-rs` to authenticate and query KakaoTalk read-only data.

## Quick checks

Run these first:

```bash
openkakao-rs --version
openkakao-rs auth
```

If Homebrew install is needed:

```bash
brew tap JungHoonGhae/openkakao
brew install JungHoonGhae/openkakao/openkakao-rs
```

## Core commands

```bash
openkakao-rs login --save
openkakao-rs chats
openkakao-rs read <chat_id> -n 30
openkakao-rs members <chat_id>
openkakao-rs friends -s "name"
openkakao-rs me
openkakao-rs settings
openkakao-rs scrap https://example.com
```

## Workflow

1. Verify binary and token status with `--version` and `auth`.
2. If token invalid, refresh by opening KakaoTalk and running `openkakao-rs login --save`.
3. Get chat IDs from `openkakao-rs chats`.
4. Read messages via `openkakao-rs read <chat_id> -n <count>`.
5. Build automation output (CSV/JSON/report) from command output.

## Troubleshooting

### `Token is invalid or expired` or API `status=-950`

- Open KakaoTalk desktop app and ensure account is logged in.
- Open chat list once in app to refresh cached request headers.
- Re-run:

```bash
openkakao-rs login --save
openkakao-rs auth
```

### Homebrew formula not found

```bash
brew tap JungHoonGhae/openkakao
brew update
brew info JungHoonGhae/openkakao/openkakao-rs
```

## Guardrails

- Treat this as read-only tooling; do not promise message sending.
- Do not expose personal chat content unless the user explicitly asks.
- Prefer summary/aggregation output for logs and reports.
