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
openkakao-rs read <id> [-n N] [--all] # Read messages (Pilsner, limited cache)
openkakao-rs members <id>          # List chat room members
```

## LOCO Protocol Commands (full access, real-time)

```bash
openkakao-rs loco-test                          # Test full LOCO connection
openkakao-rs send <chat_id> <message> [-y]        # Send text message via LOCO WRITE (add -y to skip prompt)
openkakao-rs send-photo <chat_id> <file> [-y]  # Send photo (JPEG/PNG/GIF) via LOCO SHIP+POST
openkakao-rs send-file <chat_id> <file> [-y]   # Send any file (photo/video/doc) via LOCO
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

- **REST** (`read`): Uses Pilsner cache — only returns messages for recently opened chats in the KakaoTalk app. Many chats return empty.
- **LOCO** (`loco-read`): Uses SYNCMSG protocol — returns all server-retained messages. Preferred for full history access.

## Token Management

```bash
openkakao-rs relogin [--fresh-xvc]    # Refresh token via login.json + X-VC
openkakao-rs renew                     # Attempt token renewal via refresh_token
openkakao-rs watch-cache [--interval N] # Poll Cache.db for fresh tokens
```

LOCO commands automatically refresh tokens via login.json + X-VC when needed.

## Workflow (LOCO-first)

1. Quick sanity: `openkakao-rs --version && openkakao-rs loco-test`
2. Get chat IDs: `openkakao-rs loco-chats --all --json` *(note: `--all` can be slower)*
3. Send message: `openkakao-rs send -y <chat_id> "message text"` *(default prefix on; add `--no-prefix` to disable)*
4. Read messages: `openkakao-rs loco-read <chat_id> -n 50` (or `--all`)
5. Only when you need REST-only features: open KakaoTalk app → `openkakao-rs login --save` → `openkakao-rs auth`

## Speed tips

- Prefer **LOCO** for send/read/history — REST token expiry + `login --save` can block waiting on Cache.db.
- Cache `chat_id`s you use often; avoid running `loco-chats --all` repeatedly.
- Use `-y/--yes` for non-interactive sends when you're confident the `chat_id` is correct.

## Multiline (줄바꿈) 메시지 보내기

주의: 커맨드라인에서 `\n`을 그냥 쓰면 **줄바꿈이 아니라 문자 그대로** `\n`이 전송될 수 있음. 실제 개행 문자를 만들어서 인자로 넘겨야 함.

예시:

- bash/zsh:
  - `openkakao-rs send -y <chat_id> "$(printf '첫줄\n\n둘째줄')"`
- bash 전용($'' quoting):
  - `openkakao-rs send -y <chat_id> $'첫줄\n\n둘째줄'`
- fish:
  - `openkakao-rs send -y <chat_id> (printf '첫줄\n\n둘째줄')`

## Troubleshooting

### Token invalid or `-950` error

```bash
# Open KakaoTalk app first, then:
openkakao-rs login --save
openkakao-rs auth
```

LOCO commands auto-refresh tokens, so `-950` is usually handled automatically.

### `login --save` seems to hang

`login --save` may wait until KakaoTalk updates Cache.db.

- Open KakaoTalk → open the chat list once (forces a cache refresh)
- (Optional) `openkakao-rs watch-cache --interval 2` to see when tokens change
- Or skip REST entirely and use LOCO (`loco-test` / `send` / `loco-read`).

### GETMSGS returns `-300`

This is expected on Mac (dtype=2). Use `loco-read` (SYNCMSG) instead of REST `read` (GETMSGS).

### Homebrew formula not found

```bash
brew tap JungHoonGhae/openkakao
brew update
brew install JungHoonGhae/openkakao/openkakao-rs
```

## Guardrails

- **Prefix/traceability**: By default, `openkakao-rs` prepends `🤖 [Sent via openkakao]` to outgoing messages. Use `--no-prefix` to disable it.
  - If you want a custom tag (e.g. `🤖 [openkakao]`), either add it *in the message text* (and keep default prefix), or disable the default prefix and add your own — avoid double-prefixing unless you want it.
- Use `-y/--yes` only when you are sure the `chat_id` is correct.
- Avoid `--force` unless you know what you're doing (higher ban risk).
- Do not expose personal chat content unless the user explicitly asks.
- Prefer summary/aggregation output for logs and reports.
