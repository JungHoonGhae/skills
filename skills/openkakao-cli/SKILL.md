---
name: openkakao-cli
description: Work with OpenKakao CLI (`openkakao-cli`) for KakaoTalk on macOS. Use whenever the user wants to send or read KakaoTalk messages from the terminal, inspect chats, automate from chat data, or wire KakaoTalk into local scripts/agents. On current KakaoTalk macOS builds the recommended path is the **login-free AX-automation commands** `local-send` and `ax-read`, which drive the KakaoTalk UI directly via the macOS Accessibility API (no server login, no network). Trigger on `local-send`, `ax-read`, `allow_ax_send`, `allowed_send_chats`, "Accessibility", "send kakao(talk)", "read kakao(talk)", as well as legacy terms `send`, `read`, `chats`, `watch`, `hook`, `webhook`, `LOCO`, `chat_id`, `local-chats`, `local-read`, `local-search`, `doctor`, `login`, `auth-status` (note: the server-login-based commands are broken on recent builds — see below).
---

# OpenKakao CLI

`openkakao-cli` is a KakaoTalk CLI for macOS. The binary is **`openkakao-cli`** (older docs/skills said `openkakao-rs` — that name is obsolete).

> [!IMPORTANT]
> **Server login is broken on recent KakaoTalk macOS builds.** `login --save`/`login --manual` and everything that depends on a LOCO/REST session (`send`, `read`, `chats`, `watch`, `friends`, `me`, etc.) mostly do not work anymore, and **retrying login from an unregistered device can get the account's sub-device login blocked** — do not loop on it.
>
> **But the CLI still works without logging in.** `local-send` and `ax-read` drive the real KakaoTalk app UI via the macOS Accessibility (AX) API — no server session, no network contact — so they are the reliable path for sending and reading messages today. Prefer them.

## Login-free path (recommended): `local-send` / `ax-read`

These require only that KakaoTalk.app is running and already logged in, plus Accessibility permission granted to the terminal.

```bash
openkakao-cli ax-read "<chat display name>" -n 20            # read recent visible messages
openkakao-cli ax-read "<chat display name>" -n 20 --json     # structured output
openkakao-cli local-send "<chat display name>" "message" --dry-run   # preview (no allowlist needed)
openkakao-cli local-send "<chat display name>" "message" -y          # actually send
openkakao-cli local-send "<chat display name>" "message" -y --json
```

Key facts:

- **Chats are matched by their exact display name in the chat list** — not a `chat_id`. Matching is exact (not substring), and if two visible chats share the same name the command refuses to guess. For the memo/self chat, use your own display name (KakaoTalk does not use the literal string "나와의 채팅" in its AX tree).
- **`ax-read` only returns messages currently rendered on screen.** Scroll up in KakaoTalk first for older history. Photos/files show as `"[사진]"`/`"[파일]"` placeholders; text messages carry their timestamp.
- **`local-send` requires an explicit opt-in AND an exact-match allowlist** — see Safety below. This is the only guard against sending to the wrong chat (there is no chat-id to cross-check).
- No network, no tokens, no ban risk from these two commands (they never contact Kakao's servers).
- `OPENKAKAO_CLI_DEBUG=1` prints per-step timing to stderr for `local-send`/`ax-read`.

## Safety model for `local-send`

`local-send` types text and hits Enter in a real KakaoTalk window, so it is disabled by default and needs two config keys:

```toml
# ~/.config/openkakao/config.toml
[safety]
allow_ax_send = true
allowed_send_chats = ["exact display name you allow", "another allowed chat"]
```

- `allow_ax_send = true` — general opt-in for AX-based sending.
- `allowed_send_chats` — **exact-match allowlist**. A chat not on this list is rejected before anything is typed. `--dry-run` skips both checks so you can preview against any name.

## Quick checks

```bash
openkakao-cli --version
openkakao-cli doctor          # environment / installation diagnostics
```

Homebrew install/upgrade:

```bash
brew tap JungHoonGhae/openkakao
brew install openkakao-cli
brew upgrade openkakao-cli
```

## Local database commands — currently unreliable

```bash
openkakao-cli local-chats [-n 50]            # list chats from the local encrypted DB
openkakao-cli local-read <chat_id> [-n 30]   # read messages from local DB
openkakao-cli local-search "keyword" [-n 20] # search local DB
openkakao-cli local-schema                   # dump DB schema
```

These read the SQLCipher-encrypted KakaoTalk DB directly (no server contact). **On recent KakaoTalk macOS builds the key-derivation formula has drifted, so decryption often fails** even when the user ID and device UUID are recovered — treat these as unreliable and prefer `ax-read` for login-free reading.

## Server-login commands (mostly broken on recent builds)

These need a working LOCO/REST session, which recent builds break. Listed for completeness; do not rely on them, and never loop on `login`:

```bash
openkakao-cli login --save            # extract token from Cache.db (broken: no token cached on recent builds)
openkakao-cli login --manual --save   # email/password login (broken: status=-100 device-not-registered)
openkakao-cli auth / auth-status      # verify/inspect token state
openkakao-cli chats / read <id> / members <id>   # REST/LOCO reads
openkakao-cli send <chat_id> <msg> [-y]          # LOCO send (needs allow_loco_write)
openkakao-cli send-me <msg> [-y]                 # LOCO send to memo chat
openkakao-cli watch [--json] [--hook-cmd ...] [--webhook-url ...]   # real-time LOCO watch
openkakao-cli delete / mark-read / react / edit / download          # other LOCO write/read ops
openkakao-cli friends / me / settings / profile / stats             # profile & analytics
```

If server login is ever needed (older builds), it still uses `~/.config/openkakao/config.toml` (`[safety] allow_loco_write = true` gates LOCO writes) and `~/.config/openkakao/state.json` for recovery state. But default to the AX path above.

## Recommended workflow

1. Sanity: `openkakao-cli --version && openkakao-cli doctor`
2. **Read a chat (login-free):** `openkakao-cli ax-read "<chat name>" -n 20 --json`
3. **Preview a send:** `openkakao-cli local-send "<chat name>" "message" --dry-run`
4. **Allowlist the chat** in `~/.config/openkakao/config.toml` (`allow_ax_send = true`, add the exact name to `allowed_send_chats`)
5. **Send:** `openkakao-cli local-send "<chat name>" "message" -y`

## Multiline (줄바꿈) messages

`\n` typed literally on the command line is sent as the two characters `\n`, not a newline. Build a real newline and pass it as the argument:

- bash/zsh: `openkakao-cli local-send "<chat name>" "$(printf '첫줄\n\n둘째줄')" -y`
- bash ($'' quoting): `openkakao-cli local-send "<chat name>" $'첫줄\n\n둘째줄' -y`
- fish: `openkakao-cli local-send "<chat name>" (printf '첫줄\n\n둘째줄') -y`

## Troubleshooting

### "Accessibility permission is not granted"

`local-send`/`ax-read` need the terminal app added to **System Settings → Privacy & Security → Accessibility**. Enable it for Terminal.app / iTerm2 / etc., then re-run. This is a one-time GUI step a human must do.

### "chat '<name>' not found in visible/loaded chat list"

The name doesn't exactly match a chat in KakaoTalk's list. Use the exact display name as shown in the chat list. For the memo/self chat, use your own display name. Also make sure the KakaoTalk main window (chat list) is open.

### "could not find KakaoTalk's main chat-list window"

KakaoTalk's main window is closed. Open the app (`open -a KakaoTalk`) and make sure the chat list window is showing, then retry.

### Ambiguous match / refuses to send

Two visible chats share the exact display name; `local-send` won't guess. Rename one in KakaoTalk or target a uniquely-named chat.

### Homebrew formula not found

```bash
brew tap JungHoonGhae/openkakao
brew update
brew install openkakao-cli
```

## Guardrails

- **Prefer `local-send`/`ax-read`** (login-free, no ban risk) over the server-login commands, which are broken on current builds.
- **Never loop on `login`** from an unregistered device — it can get the account's sub-device login blocked (real cases reported).
- **`local-send` only sends to allowlisted chats.** Keep `allowed_send_chats` tight; recommend `--dry-run` first. Do not add a chat to the allowlist without the user's intent.
- **Prefix/traceability:** by default outgoing messages get `🤖 [Sent via openkakao]` prepended. Use `--no-prefix` to disable, or put a custom tag in the message text.
- Do not expose personal chat content unless the user explicitly asks; prefer summaries.
- `ax-read` reads only what's on screen — don't claim full history from it.
