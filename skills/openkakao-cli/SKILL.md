---
name: openkakao-cli
description: Work with OpenKakao CLI (`openkakao-rs`) for KakaoTalk on macOS. Use when user asks to authenticate, list chats, read messages (REST or LOCO), send messages, watch real-time messages, inspect friends/members/profile/settings, manage tokens, or build automation from chat data.
---

# OpenKakao CLI

`openkakao-rs` — KakaoTalk CLI client with REST API and LOCO protocol support.

## Quick checks

```bash
openkakao-rs --version
openkakao-rs auth
```

If Homebrew install is needed:

```bash
brew tap JungHoonGhae/openkakao
brew install JungHoonGhae/openkakao/openkakao-rs
```

## REST API Commands (read-only, cached token)

```bash
openkakao-rs login --save          # Extract credentials from KakaoTalk's Cache.db
openkakao-rs auth                  # Verify token validity
openkakao-rs me                    # Show your profile
openkakao-rs friends [-f] [-s q]   # List friends (favorites/search)
openkakao-rs settings              # Show account settings
openkakao-rs chats                 # List chat rooms (Pilsner REST API)
openkakao-rs messages <id> [-n N]  # Read messages (Pilsner, limited cache)
openkakao-rs members <id>          # List chat room members
```

## LOCO Protocol Commands (full access, real-time)

```bash
openkakao-rs loco-test                          # Test full LOCO connection
openkakao-rs send <chat_id> <message>           # Send message via LOCO WRITE
openkakao-rs watch [--chat-id ID] [--raw]       # Watch real-time incoming messages
openkakao-rs watch --read-receipt               # Watch + send read receipts (NOTIREAD)
openkakao-rs watch --max-reconnect 10           # Auto-reconnect on disconnect (default 5)
openkakao-rs watch --download-media             # Auto-download media attachments
openkakao-rs download <chat_id> <log_id> [-o D] # Download media from a specific message
openkakao-rs loco-chats [--all]                 # List all chat rooms
openkakao-rs loco-read <chat_id> [-n N] [--all] # Read message history (SYNCMSG)
openkakao-rs loco-read <chat_id> --all --json   # JSON output
openkakao-rs loco-members <chat_id>             # List members
openkakao-rs loco-chatinfo <chat_id>            # Raw chat room info
```

### LOCO vs REST for messages

- **REST** (`messages`): Uses Pilsner cache — only returns messages for recently opened chats in the KakaoTalk app. Most chats return empty.
- **LOCO** (`loco-read`): Uses SYNCMSG protocol — returns all server-retained messages. Preferred for full history access.

## Token Management

```bash
openkakao-rs relogin [--fresh-xvc]    # Refresh token via login.json + X-VC
openkakao-rs renew                     # Attempt token renewal via refresh_token
openkakao-rs watch-token [--interval N] # Poll Cache.db for fresh tokens
```

LOCO commands automatically refresh tokens via login.json + X-VC when needed.

## Workflow

1. Verify binary and token: `openkakao-rs --version && openkakao-rs auth`
2. If token invalid: open KakaoTalk app, then `openkakao-rs login --save`
3. Get chat IDs: `openkakao-rs loco-chats` (or `chats` for REST)
4. Read messages: `openkakao-rs loco-read <chat_id> --all` (full history)
5. Send message: `openkakao-rs send <chat_id> "message text"`
6. Watch real-time: `openkakao-rs watch`

## Troubleshooting

### Token invalid or `-950` error

```bash
# Open KakaoTalk app first, then:
openkakao-rs login --save
openkakao-rs auth
```

LOCO commands auto-refresh tokens, so `-950` is usually handled automatically.

### GETMSGS returns `-300`

This is expected on Mac (dtype=2). Use `loco-read` (SYNCMSG) instead of `messages` (GETMSGS).

### Homebrew formula not found

```bash
brew tap JungHoonGhae/openkakao
brew update
brew install JungHoonGhae/openkakao/openkakao-rs
```

## Guardrails

- **Message prefix**: Always prepend `🤖 ` to every outgoing message for traceability. Example: `openkakao-rs send <id> "🤖 your message" -y`
- Do not expose personal chat content unless the user explicitly asks.
- Prefer summary/aggregation output for logs and reports.
- Message sending (`send`) is functional — confirm chat_id before sending.
