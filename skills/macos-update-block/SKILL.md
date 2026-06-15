---
name: macos-update-block
description: >-
  Turn macOS automatic-update blocking on or off, or check its status. Use this
  whenever the user wants to stop, block, disable, freeze, pause, or re-enable
  macOS software updates — including phrases like "맥 업데이트 차단/막아줘/꺼줘",
  "업데이트 알림 없애줘", "지금 업그레이드하기 안 뜨게", "macOS 자동 업데이트 끄기/켜기",
  "stop macOS from updating", "block the Tahoe update", or "turn updates back on".
  Also use when the user asks to toggle this on/off or check whether updates are
  currently blocked. Works on Intel and Apple Silicon Macs, macOS Big Sur (11)
  through Tahoe (26) and later; applies only methods that still work on modern
  macOS and ignores outdated tricks that silently fail.
---

# macOS Update Block

자동 업데이트를 **언제든 켜고(on) 끌(off)** 수 있게 토글하고, 현재 상태(status)를 확인하는 스킬입니다. 모든 로직은 번들 스크립트 한 곳에 있습니다:

```
scripts/macos-update-block.sh {on|off|status}
```

스크립트는 **재실행해도 안전(idempotent)** 합니다 — `on`을 두 번 해도 hosts 항목이 중복되지 않고, 상태가 어떻든 `off`로 깨끗이 되돌아갑니다.

## 무엇을 하는가

`on` (완전차단)이 적용하는 것:
1. **설정 6개** (`/Library/Preferences/com.apple.SoftwareUpdate` + `com.apple.commerce`): 자동 검색·다운로드·설치·중요업데이트·앱자동업데이트를 모두 false. 핵심은 `AutomaticCheckEnabled=false` — 이게 켜져 있으면 다운로드를 꺼놔도 업데이트 배지가 다시 뜹니다.
2. **`/etc/hosts` 서버 차단** (`gdmf / mesu / swscan / swcdn .apple.com`): macOS가 업데이트를 *탐색*하는 경로 자체를 막아 배지가 새로 생기지 않게 합니다.
3. 이미 떠 있던 업데이트 알림 캐시(`RecommendedUpdates`) 삭제.

`off`는 위를 모두 되돌립니다(설정 true 복원 + hosts 블록 제거).

## 대상 환경

- **macOS 전용** (Intel · Apple Silicon 공통). 스크립트는 macOS가 아니면 즉시 중단합니다.
- macOS **Big Sur(11) ~ Tahoe(26) 이상**에서 동작. 설정 키와 hosts 차단은 버전·아키텍처와 무관하게 같은 방식으로 작동하므로 분기 처리가 없습니다.
- `status`가 실행 환경(`macOS 버전 (칩)`)을 출력하니, 사용자 환경이 내 가정과 다른지 먼저 확인할 수 있습니다.

## 실행 방법 (중요: sudo 필요)

`on`/`off`는 `/Library/Preferences`와 `/etc/hosts`를 수정하므로 **반드시 sudo**가 필요합니다. 비대화형 환경에선 sudo 비밀번호를 직접 넣을 수 없으니, **사용자가 직접 실행하도록 정확한 명령을 안내**하세요. 명령을 클립보드에 복사해 주면(`pbcopy`) 편합니다.

`status`는 읽기 전용이라 sudo 없이 바로 실행해 결과를 보여줄 수 있습니다.

스크립트 경로는 **이 스킬이 설치된 위치의 `scripts/macos-update-block.sh`** 입니다 — 설치 방식에 따라 `~/.claude/skills/`, `~/.opencode/skills/`, 프로젝트 `.claude/skills/` 등으로 다를 수 있으니, 이 SKILL.md가 있는 디렉터리 기준으로 경로를 잡으세요. 아래 예시는 Claude Code 기본 설치 위치 기준입니다.

**on (차단):**
```
sudo "<skill-dir>/scripts/macos-update-block.sh" on
# 예: sudo ~/.claude/skills/macos-update-block/scripts/macos-update-block.sh on
```
실행 후 빨간 배지를 완전히 없애려면 **재부팅**을 안내하세요.

**off (해제):**
```
sudo "<skill-dir>/scripts/macos-update-block.sh" off
```

**status (직접 실행 가능, sudo 불필요):**
```
"<skill-dir>/scripts/macos-update-block.sh" status
```

## 진행 패턴

1. 사용자의 의도(켜기/끄기/확인)를 파악한다.
2. `status`를 먼저 돌려 현재 상태를 보여주면 사용자가 무엇이 바뀔지 이해하기 쉽다.
3. `on`/`off`는 sudo가 필요하므로 해당 명령을 클립보드에 복사하고 "터미널에 붙여넣고 비밀번호 입력" 단계를 안내한다.
4. 실행 후 다시 `status`로 결과를 확인해 준다.

## 꼭 알릴 점

- **`on` 상태에선 보안 업데이트도 받지 못합니다.** OS 버전을 의도적으로 고정하려는 경우에만 권장하고, 사용자에게 이 트레이드오프를 분명히 알리세요.
- 되돌리기는 항상 `off` 한 번이면 됩니다. 수동으로 `/etc/hosts`를 건드리지 말고 스크립트를 쓰는 게 안전합니다.
- **`AutomaticCheckEnabled` 키는 일부 macOS에서 유지되지 않습니다** — `defaults write`로 꺼도 시스템이 며칠 뒤 되돌릴 수 있습니다. 그래서 **durable한 핵심 차단 층은 hosts 서버차단**이고 설정 키는 보조입니다. `status` 종합 판정도 hosts 차단을 우선으로 봅니다(hosts가 살아있으면 탐색·다운로드가 막혀 실질 차단). 설정이 풀린 게 거슬리면 `on`을 다시 실행하면 됩니다.

## 왜 구형 방법을 안 쓰는가 (검증 결과)

흔히 떠도는 가이드의 다음 방법들은 현대 macOS(Big Sur 이후)에서 **무효**임을 확인했으므로 스크립트에 넣지 않았습니다:
- `softwareupdate --schedule off` → 플래그 자체가 삭제됨
- `CatalogURL "http://localhost"` → Catalina에서 deprecated, Big Sur에서 완전 제거 ("Catalog management is no longer supported")
- `AutomaticDownloadAutoInstall` 키 → 실제 존재하지 않는 키
- `softwareupdate --ignore "macOS ..."` → 대형 OS 업데이트엔 차단됨
