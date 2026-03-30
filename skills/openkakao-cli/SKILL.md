---
name: openkakao-cli
description: Work with OpenKakao CLI (`openkakao-rs`) for KakaoTalk on macOS. Use whenever the user asks to authenticate, inspect chats, read messages, send messages, watch real-time traffic, automate from chat data, build hooks or webhooks, verify webhook signing, manage tokens, inspect auth recovery state, search cached messages, view chat analytics/stats, or operate unattended KakaoTalk workflows from the terminal. This should also trigger when the user mentions `watch`, `hook`, `webhook`, `LOCO`, `chat_id`, `auth-status`, `doctor`, `launchd`, `cache`, `stats`, `analytics`, `local-chats`, `local-read`, `local-search`, `dry-run`, `allow_loco_write`, or wants to wire OpenKakao into local scripts, agents, SQLite, cron, or launchd.
---

# OpenKakao CLI

`openkakao-rs` is a KakaoTalk CLI with REST, LOCO, and local DB support. **LOCO write operations (send, delete, edit, react) are disabled by default** — they require `safety.allow_loco_write = true` in config. Prefer safe local-db commands for reads, use `--dry-run` to preview writes.

## Safety model

LOCO write operations risk account bans. They are disabled by default.

```toml
# ~/.config/openkakao/config.toml
[safety]
allow_loco_write = true   # Required to enable send/delete/edit/react
```

## Quick checks

```bash
openkakao-rs --version
openkakao-rs auth
openkakao-rs auth-status
openkakao-rs doctor          # Now checks local DB access + LOCO write status
```

If Homebrew install is needed:

```bash
brew tap JungHoonGhae/openkakao
brew install JungHoonGhae/openkakao/openkakao-rs
```

If the user seems to have an older binary than the repo docs or source imply, check:

```bash
which openkakao-rs
openkakao-rs --version
openkakao-rs send --help
openkakao-rs watch --help
```

Persistent operator policy can live in:

```bash
~/.config/openkakao/config.toml
```

Persisted runtime state now also lives in:

```bash
~/.config/openkakao/state.json
```

## Local Database Commands (zero server contact, zero risk)

```bash
openkakao-rs local-chats [-n 50]           # List chats from encrypted local DB
openkakao-rs local-read <chat_id> [-n 30]  # Read messages from local DB
openkakao-rs local-search "keyword" [-n 20] # Search all messages in local DB
openkakao-rs local-schema                   # Show database table schema
```

These read the SQLCipher-encrypted KakaoTalk database directly — no network, no tokens, no ban risk. Use `--json` for structured output.

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

## LOCO Protocol Commands (full access, real-time — write ops require opt-in)

```bash
openkakao-rs loco-test                          # Test full LOCO connection
openkakao-rs send <chat_id> <message> [-y]        # Send text message (requires allow_loco_write)
openkakao-rs send --me <message> [-y]             # Send to memo chat (나와의 채팅, v1.1.0+)
openkakao-rs send <chat_id> <message> --dry-run   # Preview without executing (v1.1.0+)
openkakao-rs send <chat_id> <message> -y --json   # Send and get JSON response
openkakao-rs send-photo <chat_id> <file> [-y]  # Send photo (JPEG/PNG/GIF) via LOCO SHIP+POST
openkakao-rs send-file <chat_id> <file> [-y]   # Send any file (photo/video/doc) via LOCO
openkakao-rs watch [--chat-id ID] [--raw]       # Watch real-time incoming messages
openkakao-rs watch --json                       # Watch with NDJSON output (v0.7.0+)
openkakao-rs watch --read-receipt               # Watch + send read receipts (NOTIREAD)
openkakao-rs watch --max-reconnect 10           # Auto-reconnect on disconnect (default 5)
openkakao-rs watch --download-media             # Auto-download media attachments
openkakao-rs watch --resume                     # Resume from last saved watch state (v0.6.0+)
openkakao-rs watch --capture                    # Output unknown push packets as NDJSON for protocol RE (v0.9.0+)
openkakao-rs delete <chat_id> <log_id> [-y]   # Delete a message via DELETEMSG (v0.9.0+)
openkakao-rs mark-read <chat_id> <log_id>     # Mark messages read up to logId via NOTIREAD (v0.9.0+)
openkakao-rs react <chat_id> <log_id> [-t N]  # Add reaction via ACTION (type=1=like, v0.9.1+)
openkakao-rs edit <chat_id> <log_id> <msg> [-y]  # Edit message via REWRITE (macOS: -203, v0.9.2+)
openkakao-rs download <chat_id> <log_id> [-o D] # Download media from a specific message
openkakao-rs loco-chats [--all]                 # List all chat rooms
openkakao-rs loco-read <chat_id> [-n N] [--all] # Read message history (SYNCMSG)
openkakao-rs loco-read <chat_id> --all --json   # JSON output
openkakao-rs loco-members <chat_id>             # List members
openkakao-rs loco-chatinfo <chat_id>            # Raw chat room info
```

### JSON output (v0.7.0+)

All commands support `--json` (global flag). Key additions in v0.7.0:

- `send --dry-run --json`: `{"dry_run": true, "action": "send", "chat_id": ..., "message": ...}` (v1.1.0+)
- `send --json`: `{"chat_id": ..., "log_id": ..., "status": "sent"}`
- `send-file --json`: `{"chat_id": ..., "file": ..., "type": ..., "status": "sent"}`
- `delete --json`: `{"chat_id": ..., "log_id": ..., "status": "deleted"}` (v0.9.0+)
- `react --json`: `{"chat_id": ..., "log_id": ..., "reaction_type": ..., "status": "reacted"}` (v0.9.1+)
- `edit --json`: `{"chat_id": ..., "log_id": ..., "status": "edited"}` (v0.9.2+, macOS: -203)
- `mark-read --json`: `{"chat_id": ..., "watermark": ..., "status": "marked_read"}` (v0.9.0+)
- `watch --json`: NDJSON stream, one JSON object per event line
- `chats --json`, `read --json`, `members --json`, `stats --json`: already supported pre-v0.7.0

## Analytics & Local Cache (v0.5.0+)

```bash
openkakao-rs stats <chat_id>              # Message counts, hourly activity histogram, top senders
openkakao-rs cache <chat_id> [-n N]       # Sync messages to local SQLite cache
openkakao-rs cache-search <query>         # Full-text search across cached messages
openkakao-rs cache-stats                  # Show local cache statistics (row counts, db size)
```

### LOCO vs REST for messages

- **REST** (`read`): Uses Pilsner cache — only returns messages for recently opened chats in the KakaoTalk app. Many chats return empty.
- **LOCO** (`loco-read`): Uses SYNCMSG protocol — returns all server-retained messages. Preferred for full history access.
- **Local cache merge (v0.9.3+)**: `read` automatically merges LOCO results with locally cached messages from `watch`. Messages captured during watch sessions appear in subsequent reads even when LOCO returns a limited window.

## Token Management

```bash
openkakao-rs relogin [--fresh-xvc]    # Refresh token via login.json + X-VC
openkakao-rs renew                     # Attempt token renewal via refresh_token
openkakao-rs watch-cache [--interval N] # Poll Cache.db for fresh tokens
openkakao-rs auth-status               # Show persisted auth recovery state and cooldowns
openkakao-rs doctor [--loco]           # Environment, token, recovery, and safety diagnostics
```

LOCO commands automatically refresh tokens via login.json + X-VC when needed, and REST/LOCO now share the same persisted recovery state.

## Workflow (safety-first)

1. Quick sanity: `openkakao-rs --version && openkakao-rs doctor`
2. **Safe read**: `openkakao-rs local-chats --json` (zero server contact)
3. **Safe read**: `openkakao-rs local-read <chat_id> --json`
4. **Preview write**: `openkakao-rs send <chat_id> "message" --dry-run`
5. **Full history**: `openkakao-rs read <chat_id> --all` (LOCO, needs auth)
6. **Send** (requires `allow_loco_write`): `openkakao-rs send -y <chat_id> "message text"`
7. Only when you need REST-only features: open KakaoTalk app → `openkakao-rs login --save` → `openkakao-rs auth`

## Watch automation workflow

Use this order:

1. Confirm `watch` behavior first: `openkakao-rs watch --help`
2. Start local-only with `--hook-cmd`
3. Add filters:
   - `--hook-chat-id`
   - `--hook-keyword`
   - `--hook-type`
4. Only then move to `--webhook-url` if the user explicitly wants external delivery
5. If using a webhook, prefer `--webhook-signing-secret` and tell the user to verify:
   - `X-OpenKakao-Timestamp`
   - `X-OpenKakao-Signature`

Local-first example:

```bash
openkakao-rs watch \
  --hook-cmd 'jq . > /tmp/openkakao-event.json' \
  --hook-chat-id 382416827148557 \
  --hook-type 1
```

Webhook example:

```bash
openkakao-rs watch \
  --webhook-url https://hooks.example.com/openkakao \
  --webhook-header 'Authorization: Bearer token' \
  --webhook-signing-secret 'super-secret' \
  --hook-keyword urgent
```

## Unattended and policy gates

OpenKakao separates:

- `--unattended`: declare non-interactive operation
- `--allow-non-interactive-send`: allow `send -y`, `send-file -y`, `send-photo -y`, `edit -y`
- `--allow-watch-side-effects`: allow `watch --read-receipt`, `--hook-cmd`, `--webhook-url`
- `--completion-promise`: print `[DONE]` to stdout after successful command completion (v0.9.2+, useful for LLM agent integration)

Recommended persistent config:

```toml
[mode]
unattended = true

[send]
allow_non_interactive = true
default_prefix = true

[watch]
allow_side_effects = true
default_max_reconnect = 10

[auth]
prefer_relogin = true
auto_renew = true

[safety]
allow_loco_write = true                   # Required for send/delete/edit/react (v1.1.0+)
min_unattended_send_interval_secs = 10
min_hook_interval_secs = 2
min_webhook_interval_secs = 2
hook_timeout_secs = 20
webhook_timeout_secs = 10
allow_insecure_webhooks = false
```

Interpretation:

- unattended sends are rate-limited by default
- local hooks are rate-limited and timed out
- webhooks are rate-limited, timed out, and default to HTTPS only unless localhost
- `auth-status` and `doctor` are the first checks before assuming a long-running job is healthy

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
openkakao-rs auth-status
```

LOCO commands auto-refresh tokens, so `-950` is usually handled automatically.

If the machine has been running unattended for a while, inspect:

- `openkakao-rs auth-status --json`
- `openkakao-rs doctor --loco`

Look for:

- `last_failure_kind`
- `consecutive_failures`
- `auth_cooldown_remaining_secs`
- `last_recovery_source`

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

- **LOCO write disabled by default**: send/delete/edit/react require `safety.allow_loco_write = true`. Always recommend `--dry-run` first. Use `local-chats`/`local-read` for safe reads.
- **Prefix/traceability**: By default, `openkakao-rs` prepends `🤖 [Sent via openkakao]` to outgoing messages. Use `--no-prefix` to disable it.
  - If you want a custom tag (e.g. `🤖 [openkakao]`), either add it *in the message text* (and keep default prefix), or disable the default prefix and add your own — avoid double-prefixing unless you want it.
- Use `-y/--yes` only when you are sure the `chat_id` is correct.
- Do not assume unattended send can burst freely; the CLI now rate-limits it by default.
- Avoid `--force` unless you know what you're doing (higher ban risk).
- Prefer `watch --hook-cmd` over webhooks when the task can stay on the same machine.
- If using `--webhook-url`, be explicit that chat content leaves the local trust boundary.
- Expect non-HTTPS remote webhooks to be blocked unless the user has explicitly loosened `safety.allow_insecure_webhooks`.
- Treat `watch` hooks/webhooks as best-effort delivery, not a durable queue or exactly-once event bus.
- Treat unattended mode as a policy decision. If the user is building a service, push them toward `config.toml` instead of repeating long flag strings.
- For macOS services, steer users toward `examples/launchd/` in the repo instead of ad-hoc LaunchAgent files.
- Do not expose personal chat content unless the user explicitly asks.
- Prefer summary/aggregation output for logs and reports.
