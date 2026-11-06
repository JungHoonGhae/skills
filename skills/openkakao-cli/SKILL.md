---
name: openkakao-cli
description: >-
  Work with OpenKakao CLI (`openkakao-cli` 1.10.0+) for KakaoTalk on macOS: send text and files, reply to or edit a message, read a chat, open a chat window, set the tool up (`init`, `doctor`), detect incoming messages (`notif-watch`), also over SSH to the Mac that runs KakaoTalk. Trigger on `openkakao`, `local-send`, `local-send-file`, `local-reply`, `local-edit`, `ax-read`, `allow_ax_send`, `allowed_send_chats`, "send kakao(talk)", "read kakao(talk)", "kakaotalk file", "focus-free", and the error codes `chat_window_not_open`, `delivery_uncertain`, `user_active`, `file_type_refused`. Legacy terms (`send`, `read`, `chats`, `watch`, `LOCO`, `login`) belong to the server-login path, which is broken on current builds; route them here too and use the AX commands instead.
---

# OpenKakao CLI

`openkakao-cli` drives the real KakaoTalk desktop app through the macOS Accessibility (AX) API: no server session, no network, no ban risk. Since 1.10.0 every default path is **focus-free**: it reads and sets AX attributes and presses AX buttons, never raises KakaoTalk and never posts keys, so the person at that Mac keeps working. The binary is `openkakao-cli` (`openkakao-rs` is an obsolete name).

> [!IMPORTANT]
> Server login (`login`, `send`, `read`, `chats`, `watch`, `friends`, `me`, …) is broken on recent KakaoTalk builds, and retrying `login` from an unregistered device can get the account's sub-device login blocked. Never loop on it. Use the AX commands below.

## Setup (once per Mac that runs KakaoTalk)

```bash
brew tap JungHoonGhae/openkakao
brew trust --formula junghoonghae/openkakao/openkakao-cli   # Homebrew 7 refuses untrusted taps otherwise
brew install openkakao-cli                                   # or: brew upgrade openkakao-cli
openkakao-cli init                                           # interactive: readiness checks, allowlist, agent skill
openkakao-cli init --yes --allow-chat "<exact chat name>" --skill none   # scripted: writes config only
openkakao-cli doctor --chat "<chat name>"                    # read-only: composer, 전송, 파일전송, send gate, auth grace
```

`init` writes `~/.config/openkakao/config.toml` (`[safety] allow_ax_send = true`, `allowed_send_chats = ["…"]`), keeps comments, and is idempotent. KakaoTalk must be running and signed in there, with Accessibility granted to the process that runs the command (Terminal/iTerm, or `/usr/libexec/sshd-keygen-wrapper` over SSH; see below).

## Commands

| Need | Command | Notes |
| --- | --- | --- |
| Read an open chat | `openkakao-cli ax-read "<chat>" -n 20 --json` | 0.1 s; only rendered rows, so no full history. Files show as `[파일]`, photos as `[사진]`. |
| Send text | `openkakao-cli local-send "<chat>" "<text>" -y --json` | ~3 s. Newlines: `$'첫줄\n둘째줄'`. Default prefix `🤖 [Sent via openkakao]`; `--no-prefix` to drop it. |
| Send any file | `openkakao-cli local-send-file "<chat>" <path> -y --json` | docx, xlsx, pdf, zip, txt, images; up to `[ax] max_file_mb` (300). A file outside the top level of Desktop/Documents/Downloads is hard-linked into `~/Downloads` and removed after the upload finishes. `verified_by` is `file_name` or `[파일]`. |
| Send a photo | `openkakao-cli local-send-photo "<chat>" <image> -y` | thin wrapper over the file path with image checks (50 MiB). |
| Reply to a message | `openkakao-cli local-reply "<chat>" "<text>" --to-last -y` or `--match "<exact bubble text>"` | experimental; needs the bubble's whole text; duplicates refuse. |
| Edit your message | `openkakao-cli local-edit "<chat>" --match "<old exact text>" "<new text>" -y` | experimental; verified by the `수정됨` label. |
| Open a closed chat | add `--open-if-needed` to any command above | opens it from the chat list's context menu; marks the chat read. |
| Preview | add `--dry-run` | shows what would be sent, no allowlist or authentication needed. |
| Incoming messages | `openkakao-cli notif-watch --json` | reads Notification Center; works with windows closed. |

Chats are matched by their **exact display name** (the window title). The memo chat is titled with the user's own display name, not "나와의 채팅". Two open windows with the same title refuse.

## What a real send needs

1. `allow_ax_send = true` and the exact name in `allowed_send_chats` (`init --allow-chat` does both). Do not add a chat without the user's intent.
2. The chat window open on the active Space, or `--open-if-needed`.
3. **The person at that Mac approves a macOS device-owner prompt (Touch ID or password) for every real send, reply and edit.** `-y` skips only the terminal confirmation. Tell the user the prompt will appear. If they set `[safety] device_owner_auth_grace_secs` (default 0, sudo-style reuse of one approval), later sends within that window skip the prompt; only the human sets it, never the agent.

## Reading results

Success prints JSON with `"status": "sent"` (text, file) or `"verified"` (reply, edit). Failures print one JSON object on stdout and exit 1:

```json
{"error": {"code": "chat_window_not_open", "message": "…", "fix": "…"}}
```

| Code | Meaning | Do |
| --- | --- | --- |
| `accessibility_not_granted` | the process has no AX permission | a human adds it in System Settings → Privacy & Security → Accessibility (over SSH: `/usr/libexec/sshd-keygen-wrapper`) |
| `kakaotalk_signed_out`, `kakaotalk_not_running` | sign in / start KakaoTalk on that Mac | never sign in on a second Mac just to send; the session may move |
| `main_window_not_visible` | main window closed, minimized, or on another Space | see Spaces below |
| `chat_window_not_open` | no open window with that exact title | re-run with `--open-if-needed`, or ask the user to open the chat |
| `chat_list_filtered` | the chat list's search box holds a term | the user clears it in KakaoTalk; setting the field's AX value does not re-run the filter |
| `chat_not_found`, `chat_ambiguous` | name mismatch, lazily loaded list, or duplicate names | use the exact window title; scroll the list |
| `user_active` | a KakaoTalk menu was already open, or the mouse cursor is over the menu | ask the user to close the menu by clicking elsewhere (never Esc); retry |
| `staging_conflict` | `~/Downloads/<name>` already exists | do not overwrite; rename the file or let the user clear it |
| `file_type_refused` | KakaoTalk's picker greys this type out (seen with `.bin`) | zip it and send the archive |
| `delivery_uncertain` | the send may have happened | look at the chat (`ax-read`) before anything else; **never retry blindly** |
| `send_button_missing`, `menu_not_found`, `action_unverified` | the UI differs from the measured build | stop and report; `--fallback-keys` exists for old builds but raises KakaoTalk |

`OPENKAKAO_CLI_DEBUG=1` prints per-step timings to stderr.

## Over SSH (agent on one Mac, KakaoTalk on another)

1. Install and configure on the Mac that runs the signed-in KakaoTalk; each Mac has its own allowlist.
2. Grant Accessibility to `/usr/libexec/sshd-keygen-wrapper` there once (System Settings → Privacy & Security → Accessibility → `+` → ⌘⇧G → the path). Every SSH session can then drive that Mac's UI, so do this only behind key-only SSH.
3. The Touch ID / password prompt appears on **that** Mac's screen; the person there approves it. Nothing else changes their focus.
4. macOS has no `timeout` command; do not wrap remote calls with it. Non-login shells lack `/opt/homebrew/bin` in `PATH`; call `/opt/homebrew/bin/openkakao-cli` or export the path.

## Spaces (virtual desktops)

AX lists only the windows of the active Space. Two ways to live with it:

- Leave KakaoTalk on one desktop: commands work while that desktop is active, and report `main_window_not_visible` / `chat_window_not_open` otherwise.
- `openkakao-cli init --all-spaces` (Dock → Options → Assign To → All Desktops; restarts the Dock): commands work from every desktop, but KakaoTalk's windows then follow every desktop switch and surface on top. Ask before changing this; it is a preference of the person using the Mac.

## Guardrails

- Test on the memo chat first. Send to other people only when the user explicitly says so, with the exact text they approved. Keep `allowed_send_chats` tight and preview with `--dry-run`.
- Expect one authentication prompt per real send; do not try to avoid it.
- On `delivery_uncertain`, read the chat and report; a second attempt duplicates the message.
- Never post the Escape key to KakaoTalk (it closes the chat window and the main window). Never raise KakaoTalk or post keys yourself; the CLI's default paths do not need to.
- Do not sign in on the agent's Mac, and never loop on `login`.
- Do not expose personal chat content unless asked; prefer summaries. `ax-read` shows only what is rendered.

## Older builds and diagnostics

`references/focus-free-recipes.md` holds the measured AX facts (composer `AXSelectedText`, `전송`/`파일전송` buttons, the open panel's outlines, bubble menus in CoreGraphics layer-101 windows, grouped-time rows) and JXA scripts. Open it when the installed CLI is older than 1.10.0, when a command reports a UI mismatch and you need to inspect the AX tree, or when KakaoTalk's labels differ from the Korean ones measured here.
