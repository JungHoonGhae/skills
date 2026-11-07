---
name: openkakao-cli
description: >-
  Moved: the OpenKakao CLI skill (KakaoTalk on macOS via `openkakao-cli`: `local-send`, `local-send-file`, `local-send-photo`, `local-reply`, `local-edit`, `local-delete`, `ax-read`, `ax-login`) now ships with the CLI in JungHoonGhae/openkakao-cli. Trigger on `openkakao`, "send kakao(talk)", "read kakao(talk)", and openkakao error codes, then load the current skill as described below.
---

# OpenKakao CLI (moved)

This skill now lives with the CLI, so it updates with each release:
<https://github.com/JungHoonGhae/openkakao-cli/tree/main/skills/openkakao-cli>

Install the current version, then use it instead of this stub:

```bash
npx skills add JungHoonGhae/openkakao-cli
# or, with openkakao-cli 1.12.0+:
openkakao-cli init --skill all
```

Until it is installed, read and follow the current `SKILL.md` directly:
<https://raw.githubusercontent.com/JungHoonGhae/openkakao-cli/main/skills/openkakao-cli/SKILL.md>
