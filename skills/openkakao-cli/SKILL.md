---
name: openkakao-cli
description: >-
  Work with OpenKakao CLI (`openkakao-cli`) for KakaoTalk on macOS. Use whenever the user wants to send or read KakaoTalk messages from the terminal, inspect chats, automate from chat data, or wire KakaoTalk into local scripts/agents. On current KakaoTalk macOS builds the recommended path is the **login-free AX-automation commands** `local-send` and `ax-read`, which drive the KakaoTalk UI directly via the macOS Accessibility API (no server login, no network). Trigger on `local-send`, `ax-read`, `allow_ax_send`, `allowed_send_chats`, "Accessibility", "send kakao(talk)", "read kakao(talk)", as well as legacy terms `send`, `read`, `chats`, `watch`, `hook`, `webhook`, `LOCO`, `chat_id`, `local-chats`, `local-read`, `local-search`, `doctor`, `login`, `auth-status` (note: the server-login-based commands are broken on recent builds, see below). Also use it for focus-free automation (sending text or files without stealing the user's focus), opening chat windows, mentions, and incoming-message detection with `notif-watch`.
---

# OpenKakao CLI

`openkakao-cli` is a KakaoTalk CLI for macOS. The binary is **`openkakao-cli`** (older docs/skills said `openkakao-rs`: that name is obsolete).

> [!IMPORTANT]
> **Server login is broken on recent KakaoTalk macOS builds.** `login --save`/`login --manual` and everything that depends on a LOCO/REST session (`send`, `read`, `chats`, `watch`, `friends`, `me`, etc.) mostly do not work anymore, and **retrying login from an unregistered device can get the account's sub-device login blocked**: do not loop on it.
>
> **But the CLI still works without logging in.** `local-send` and `ax-read` drive the real KakaoTalk app UI via the macOS Accessibility (AX) API: no server session, no network contact: so they are the reliable path for sending and reading messages today. Prefer them.

## Focus-free recipes (verified 2026-11-06, KakaoTalk 26.9.0)

The 1.9.0 commands below raise KakaoTalk and press keys, so they fail with `could not verify focus` while the user is typing and leave the user's app unfocused. When the user must keep working on that Mac (or you drive it over SSH), use the AX-only JXA recipes in [references/focus-free-recipes.md](references/focus-free-recipes.md) instead; each was measured with the user's app staying frontmost:

- **Send text** to an open chat window (~3 s): insert via `AXSelectedText`, then `AXPress` the `전송` button. Open the reference when a plain `local-send` is not acceptable because of focus.
- **Send any file** (~10 s, `.docx` verified): `AXPress` the `파일전송` button, drive the file panel by selecting sidebar and list rows, then `AXPress` `N개 전송`. Open it for files (1.9.0 `local-send-photo` only takes images and fails on Korean button titles).
- **Open a closed chat / show a hidden main window**: chat-list row menu `채팅방 열기`; menu bar `창 > 채팅`. Open it when the target window is not open.
- **Incoming messages**: `notif-watch` needed no extra permission; its fields and limits are listed there.
- **Warnings** you must read before touching menus or keys: never post Escape to KakaoTalk; pid-posted keys do nothing in the background; bubble context menus are often invisible to AX.

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

- **Chats are matched by their exact display name in the chat list**: not a `chat_id`. Matching is exact (not substring), and if two visible chats share the same name the command refuses to guess. For the memo/self chat, use your own display name (KakaoTalk does not use the literal string "나와의 채팅" in its AX tree).
- **`ax-read` only returns messages currently rendered on screen.** Scroll up in KakaoTalk first for older history. Photos/files show as `"[사진]"`/`"[파일]"` placeholders; text messages carry their timestamp.
- **`local-send` requires an explicit opt-in AND an exact-match allowlist**: see Safety below. This is the only guard against sending to the wrong chat (there is no chat-id to cross-check).
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

- `allow_ax_send = true`: general opt-in for AX-based sending.
- `allowed_send_chats`: **exact-match allowlist**. A chat not on this list is rejected before anything is typed. `--dry-run` skips both checks so you can preview against any name.

## Quick checks

```bash
openkakao-cli --version
openkakao-cli doctor          # environment / installation diagnostics
```

Homebrew install/upgrade:

```bash
brew tap JungHoonGhae/openkakao
brew trust --formula junghoonghae/openkakao/openkakao-cli   # Homebrew 7+ refuses untrusted taps without this
brew install openkakao-cli
brew upgrade openkakao-cli
```

If `brew install` says *Refusing to load formula … from untrusted tap*, run the `brew trust --formula …` line above. Trusting the one formula is narrower than `brew trust junghoonghae/openkakao` (the whole tap).

## Local database commands: currently unreliable

```bash
openkakao-cli local-chats [-n 50]            # list chats from the local encrypted DB
openkakao-cli local-read <chat_id> [-n 30]   # read messages from local DB
openkakao-cli local-search "keyword" [-n 20] # search local DB
openkakao-cli local-schema                   # dump DB schema
```

These read the SQLCipher-encrypted KakaoTalk DB directly (no server contact). **On recent KakaoTalk macOS builds the key-derivation formula has drifted, so decryption often fails** even when the user ID and device UUID are recovered: treat these as unreliable and prefer `ax-read` for login-free reading.

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

## Driving another Mac over SSH

KakaoTalk desktop is usually signed in on one Mac (the one the user works on), while the agent may run on another. The AX commands work over SSH, with three one-time conditions:

1. **Install on the Mac that runs the signed-in KakaoTalk**, not the agent's Mac. Each Mac has its own `~/.config/openkakao/config.toml` allowlist.
2. **Check that KakaoTalk is signed in there.** A single window named `로그인` means it is signed out:
   ```bash
   ssh <mac> 'osascript -e "tell application \"System Events\" to tell process \"KakaoTalk\" to get name of every window"'
   ```
   Do not sign in on a second Mac just to send: the desktop session may move and sign the user's main Mac out.
3. **Grant Accessibility to the SSH process.** Over SSH the AX calls are attributed to `/usr/libexec/sshd-keygen-wrapper`, so the error is *Accessibility permission is not granted to this terminal app*. A human adds it once: System Settings → Privacy & Security → Accessibility → `+` → ⌘⇧G → `/usr/libexec/sshd-keygen-wrapper` → turn it on. Trade-off: every SSH session to that Mac can then drive its UI, so do this only on a Mac reachable by key-only SSH (for example over Tailscale).

macOS has no `timeout` command; do not wrap remote calls with it.

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

The name doesn't exactly match a row in KakaoTalk's main chat list. Check, in this order:

1. **The chat-list search box still holds a term.** The list then shows only matching chats, so everything else is "not found". Clear the search in KakaoTalk by hand: setting the field's AX value to empty clears the text but does not re-run the filter.
2. **Exact display name.** Use the name exactly as the row shows it (open chat windows are titled the same). For the memo/self chat, use your own display name.
3. **The list is lazily loaded.** Only rows KakaoTalk has loaded can match; scroll the chat list if the chat is far down.

To see the names the tool can match, dump the first text of each loaded row (run where KakaoTalk runs, with Accessibility granted):

```bash
cat > /tmp/kakao-rows.js <<'JS'
const w = Application('System Events').processes.byName('KakaoTalk').windows.byName('카카오톡');
const out = [];
(function walk(el, d) {
  if (d > 8 || out.length > 200) return;
  let role = ''; try { role = el.role(); } catch (e) { return; }
  if (role === 'AXRow') { try { const t = el.staticTexts(); out.push(t.length ? t[0].value() : ''); } catch (e) {} return; }
  let kids = []; try { kids = el.uiElements(); } catch (e) {}
  for (const k of kids) walk(k, d + 1);
})(w, 0);
out.join('\n');
JS
osascript -l JavaScript /tmp/kakao-rows.js
```

The main window's title depends on the UI language (`카카오톡` in Korean); adjust `byName(...)` if needed.

### "could not find KakaoTalk's main chat-list window"

The tool looks for the window whose `AXIdentifier` is `Main Window`. It is missing when the main window is closed, **or when it sits on another Space (virtual desktop)**: the Accessibility API drops windows on other Spaces from the window list entirely. By design the tool never brings KakaoTalk to the front, so fix it once by hand:

- Dock → right-click KakaoTalk → Options → Assign To → **All Desktops** (or, with the user's consent, `defaults write com.apple.spaces app-bindings -dict-add com.kakao.kakaotalkmac AllSpaces && killall Dock`; the Dock restarts for about a second), and
- make sure the main window is open and not minimized (a minimized main window gives its own error). A main window hidden with its close button comes back through the app menu bar `창 > 채팅` (`AXPress`) without activating the app; `tell application "KakaoTalk" to reopen` activates it and steals focus, so avoid it.

Opening the app with `open -a KakaoTalk` also works but steals the user's focus; avoid it on a Mac someone is using.

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
- **Never loop on `login`** from an unregistered device: it can get the account's sub-device login blocked (real cases reported).
- **`local-send` only sends to allowlisted chats.** Keep `allowed_send_chats` tight; recommend `--dry-run` first. Do not add a chat to the allowlist without the user's intent.
- **Test on the memo/self chat first.** Send to other people's chats only when the user explicitly says to, with the exact text they approved.
- **Never post the Escape key to KakaoTalk's pid.** KakaoTalk closes the focused chat window (and the main window) on Escape. Dismiss menus with `AXCancel` and sheets with their `취소` button.
- **Key events posted to KakaoTalk's pid do nothing while it is not frontmost.** Anything needing Return, ⌘V, ⌘O or ⌘⇧G needs a raise; prefer the AX-only recipes.
- **Bubble context menus are unreliable through AX.** If a menu opened by `AXShowMenu` is not found within a bounded poll, type nothing and tell the user to dismiss any visible menu by clicking elsewhere.
- **Prefix/traceability:** by default outgoing messages get `🤖 [Sent via openkakao]` prepended. Use `--no-prefix` to disable, or put a custom tag in the message text.
- Do not expose personal chat content unless the user explicitly asks; prefer summaries.
- `ax-read` reads only what's on screen: don't claim full history from it.
