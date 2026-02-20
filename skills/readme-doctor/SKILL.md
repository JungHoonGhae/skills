---
name: readme-doctor
description: README diagnosis and treatment. Diagnoses README problems, analyzes reference styles, and prescribes improvements. Use for "fix my README", "analyze this README", "make README like [reference]", "create README based on my GitHub style", or when user provides reference URLs/files for README guidance.
---

# README Doctor

README 진단과 처방. 문제를 진단하고, 레퍼런스를 분석하고, 개선안을 처방합니다.

## 진단 프로세스

```
환자(README) 접수 → 진단 → 처방 → 치료
```

## Mode 1: 진단 & 치료 (기본)

현재 프로젝트의 README를 진단하고 처방합니다.

### Step 1: 접수

```bash
# 현재 디렉토리 README 확인
[ -f README.md ] && cat README.md

# 프로젝트 정보 수집
[ -f package.json ] && cat package.json | jq '{name, description, version}'
[ -f pyproject.toml ] && grep -E "^(name|version|description)" pyproject.toml
```

### Step 2: 진단 체크리스트

| 항목 | 진단 기준 |
|------|-----------|
| **제목** | 프로젝트 이름이 명확한가? |
| **설명** | 1-2문장으로 "무엇을, 왜" 설명하는가? |
| **설치** | 누구든 따라할 수 있는가? |
| **사용법** | 실행 가능한 예제가 있는가? |
| **맥락** | 필요한 배경 지식이 제공되는가? |
| **구조** | 인지적 퍼널링 (넓은 → 좁은)을 따르는가? |
| **최신성** | 내용이 현재 프로젝트 상태와 일치하는가? |

### Step 3: 처방서 출력

```markdown
## 진단 결과

### 건강함
- [x] 설치 섹션 존재
- [x] 라이선스 명시

### 주의 필요
- ⚠️ 설명이 너무 김 (3줄 → 1-2줄 권장)
- ⚠️ 사용 예제 없음

### 치료 필요
- ❌ 제목에 "프로젝트"만 있음 → 실제 이름으로 변경
- ❌ 설치 명령어 구식 (npm install → npm i 권장)

## 처방

### 1. 제목 수정
- 현재: `# 프로젝트`
- 권장: `# my-awesome-tool`

### 2. 설명 축약
- 현재: "이 프로젝트는... (3줄)"
- 권장: "CLI tool for X. One-liner."

### 3. 사용 예제 추가
\`\`\`bash
my-tool --input file.txt --output result.json
\`\`\`
```

## Mode 2: 레퍼런스 분석

사용자가 제공한 레퍼런스 README에서 스타일을 분석합니다.

### 입력 형태

```bash
# GitHub URL
"Analyze https://github.com/vercel/next.js/blob/canary/README.md"

# 로컬 파일
"Analyze ~/projects/example/README.md"

# 직접 붙여넣기
"Analyze this README style: [paste content]"
```

### 분석 항목

| 카테고리 | 분석 내용 |
|----------|-----------|
| **구조** | 섹션 순서, 계층 구조 |
| **스타일** | 배지, 이모지, 코드 블록 |
| **톤** | 격식/비격식, 간결/상세 |
| **포맷** | 테이블, 리스트, 인용구 사용 |

### 분석 결과 예시

```json
{
  "structure": ["Title", "Badges", "Description", "Features", "Install", "Usage", "Contributing", "License"],
  "styles": {
    "badges": true,
    "emoji_in_headers": false,
    "code_blocks": ["bash", "typescript"],
    "images": false,
    "toc": false
  },
  "tone": "professional-concise",
  "avg_section_length": "short"
}
```

## Mode 3: GitHub 패턴 분석

사용자의 GitHub 리포지토리에서 README 패턴을 추출합니다.

```bash
# 사용자 리포 분석
gh repo list <username> --limit 10 --json name,url

# README 가져오기
gh api /repos/<owner>/<repo>/readme --jq '.content' | base64 -d
```

최소 3개 이상의 README에서 공통 패턴 추출.

## Mode 4: 베스트 프랙티스 체크

`references/best-practices.md` 기반으로 README 품질 평가.

### 필수 체크

- [ ] 제목 + 1줄 설명
- [ ] 설치 방법
- [ ] 사용 예제
- [ ] 라이선스

### 권장 체크

- [ ] 배지 (npm version, license 등)
- [ ] 기여 가이드
- [ ] 변경 로그 링크

## 레퍼런스 활용

사용자가 레퍼런스를 제공하면:

1. **레퍼런스 분석** → 스타일/구조 추출
2. **현재 프로젝트 진단** → 문제 파악
3. **처방** → 레퍼런스 스타일로 개선안 제시

```
User: "Make my README like Vercel's style. Reference: https://github.com/vercel/next.js"

Process:
1. Fetch Vercel's README
2. Analyze: badges at top, concise sections, professional tone
3. Diagnose current README
4. Prescribe: "Add badges section", "Shorten description to 1 line", "Add Features table"
```

## 템플릿

프로젝트 타입별 템플릿은 `templates/` 폴더 참조:

| 템플릿 | 용도 |
|--------|------|
| `templates/oss.md` | 오픈소스 |
| `templates/personal.md` | 개인 프로젝트 |
| `templates/internal.md` | 내부 툴 |
| `templates/xdg-config.md` | 설정 파일 |

## 참고 문서

| 파일 | 내용 |
|------|------|
| `references/best-practices.md` | README 베스트 프랙티스 |
| `references/section-checklist.md` | 섹션 체크리스트 |
| `references/templates.md` | 언어별 패턴 |

## 사용 예시

```
# 진단 요청
"Fix my README"
"진단해줘"

# 레퍼런스 기반
"Make README like this: https://github.com/facebook/react"
"이 스타일로 바꿔: [README 내용]"

# GitHub 패턴
"Create README based on my GitHub style"
"내 GitHub 스타일로 README 만들어"

# 새 프로젝트
"I need a README for a new CLI tool"
```

## 전제 조건

- `gh` CLI (GitHub 패턴 분석용)
- `jq` (JSON 처리)
- Python 3.6+ (스크립트 실행 시)
