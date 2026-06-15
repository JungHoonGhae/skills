#!/bin/bash
# macOS 자동 업데이트 차단 토글
# macOS 26 (Tahoe) / Apple Silicon에서 실제 동작 확인된 방법만 사용.
#  - 설정 6개: 자동 검색/다운로드/설치 차단 (구형 명령 softwareupdate --schedule,
#    CatalogURL, AutomaticDownloadAutoInstall 등은 현재 macOS에서 무효라 사용 안 함)
#  - /etc/hosts: 업데이트 탐색 서버 4개 차단 (제거된 CatalogURL 역할 대체)
# 사용법: [sudo] macos-update-block.sh {on|off|status}
set -euo pipefail

# macOS 전용. 다른 OS에선 sed -i '' 등이 깨지므로 즉시 중단.
if [ "$(uname -s)" != "Darwin" ]; then
  echo "이 스크립트는 macOS 전용입니다 (현재 감지: $(uname -s))." >&2
  exit 1
fi

SU="/Library/Preferences/com.apple.SoftwareUpdate"
COMMERCE="/Library/Preferences/com.apple.commerce"
HOSTS="/etc/hosts"
MARKER_START="# === macOS Update Block (managed by macos-update-block skill) START ==="
MARKER_END="# === macOS Update Block END ==="
BLOCK_HOSTS=(gdmf.apple.com mesu.apple.com swscan.apple.com swcdn.apple.com)
SU_KEYS=(AutomaticCheckEnabled AutomaticDownload AutomaticallyInstallMacOSUpdates ConfigDataInstall CriticalUpdateInstall)

need_root() {
  if [ "$(id -u)" -ne 0 ]; then
    echo "이 작업은 관리자 권한이 필요합니다. 다음처럼 실행하세요:" >&2
    echo "  sudo \"$0\" $1" >&2
    exit 1
  fi
}

flush_dns() {
  dscacheutil -flushcache 2>/dev/null || true
  killall -HUP mDNSResponder 2>/dev/null || true
}

hosts_has_block() {
  # 마커 형식과 무관하게, 차단 도메인이나 주석이 있으면 차단 중으로 판단
  if grep -q "macOS Update Block" "$HOSTS"; then return 0; fi
  for h in "${BLOCK_HOSTS[@]}"; do
    if grep -qF "0.0.0.0 $h" "$HOSTS"; then return 0; fi
  done
  return 1
}

remove_hosts_block() {
  # 마커 주석(언어/형식 무관) + 차단 도메인 줄을 직접 삭제 → 수동 추가분도 정리, 재실행 안전
  local args=(-e '/macOS Update Block/d')
  local h
  for h in "${BLOCK_HOSTS[@]}"; do
    args+=(-e "/^0\.0\.0\.0[[:space:]][[:space:]]*${h//./\\.}\$/d")
  done
  sed -i '' "${args[@]}" "$HOSTS"
}

cmd_on() {
  need_root on
  for k in "${SU_KEYS[@]}"; do defaults write "$SU" "$k" -bool false; done
  defaults write "$COMMERCE" AutoUpdate -bool false
  remove_hosts_block               # 중복 추가 방지
  {
    echo "$MARKER_START"
    for h in "${BLOCK_HOSTS[@]}"; do echo "0.0.0.0 $h"; done
    echo "$MARKER_END"
  } >> "$HOSTS"
  defaults delete "$SU" RecommendedUpdates 2>/dev/null || true  # 이미 뜬 배지 캐시 제거
  flush_dns
  echo "✅ 업데이트 차단 ON — 설정 6개 + 서버 ${#BLOCK_HOSTS[@]}개 차단."
  echo "   화면의 빨간 배지를 완전히 없애려면 재부팅하세요."
  echo "   ⚠️ 이 상태에선 보안 업데이트도 받지 않습니다."
}

cmd_off() {
  need_root off
  for k in "${SU_KEYS[@]}"; do defaults write "$SU" "$k" -bool true; done
  defaults write "$COMMERCE" AutoUpdate -bool true
  remove_hosts_block
  flush_dns
  echo "✅ 업데이트 차단 OFF — 자동 업데이트 재개, 서버 차단 해제."
}

cmd_status() {
  echo "=== macOS Update Block 상태 ==="
  echo "환경: macOS $(sw_vers -productVersion 2>/dev/null || echo '?') ($(uname -m))"
  echo "[설정]"
  for k in "${SU_KEYS[@]}"; do
    printf "  %-34s = %s\n" "$k" "$(defaults read "$SU" "$k" 2>/dev/null || echo '미설정(기본값)')"
  done
  printf "  %-34s = %s\n" "commerce AutoUpdate" "$(defaults read "$COMMERCE" AutoUpdate 2>/dev/null || echo '미설정(기본값)')"
  echo "[서버 차단(/etc/hosts)]"
  local blocked=no
  if hosts_has_block; then blocked=yes; fi
  if [ "$blocked" = yes ]; then echo "  차단 중 (${BLOCK_HOSTS[*]})"; else echo "  차단 없음"; fi
  # hosts 차단이 durable한 핵심 층. AutomaticCheckEnabled는 일부 macOS에서
  # defaults write로 넣어도 시스템이 되돌리므로 보조 지표로만 사용.
  local chk; chk="$(defaults read "$SU" AutomaticCheckEnabled 2>/dev/null || echo 1)"
  echo -n ">>> 종합: "
  if [ "$blocked" = yes ] && [ "$chk" = "0" ]; then echo "🔒 차단 ON (완전차단)"
  elif [ "$blocked" = yes ]; then echo "🔒 차단 ON (서버차단 — 탐색·다운로드 불가)"
  elif [ "$chk" = "0" ]; then echo "⚠️ 설정만 차단 (서버차단 OFF — 권장: on 재실행)"
  else echo "🔓 차단 OFF"; fi
}

case "${1:-status}" in
  on)     cmd_on ;;
  off)    cmd_off ;;
  status) cmd_status ;;
  *) echo "사용법: [sudo] \"$0\" {on|off|status}" >&2; exit 1 ;;
esac
