---
name: figma-to-pptx
description: >-
  Convert Figma frames into a fully editable PowerPoint (.pptx). Boxes, borders and shadows become PowerPoint
  shapes, icons become freeform shapes, text becomes text boxes in the same fonts as Figma (embedded, so it looks
  the same on PCs that do not have them), image fills become pictures and Figma layers become groups. Use this
  whenever someone needs to hand Figma screens, wireframes, screen specs (화면설계서), storyboards or slide designs
  to people who only use PowerPoint or MS Office, including phrases like "Figma를 PPT로", "피그마 화면설계서 PPT
  변환", "편집 가능한 PPT로 내보내기", "PPT로 전달해야 해", "figma to pptx", "export Figma frames to editable
  PowerPoint", "convert this Figma page to slides". Needs a Figma personal access token (FIGMA_TOKEN) and Python 3.10+.
---

# Figma → 편집 가능한 PowerPoint

Figma 페이지·섹션·프레임을 받아 **모든 요소가 PowerPoint에서 고쳐지는** `.pptx`로 바꿉니다. 그림 한 장으로 덮지 않고 Figma 레이어를 하나씩 PowerPoint 개체로 옮깁니다. 모든 로직은 번들 스크립트 한 곳에 있습니다.

```
scripts/figma_to_pptx.py <Figma 링크> -o 결과.pptx
```

## 무엇으로 바뀌나

| Figma | PowerPoint |
|---|---|
| 프레임·사각형·원 (단색·그러데이션, 둥근 모서리, 테두리, 그림자) | 도형 (둥근 사각형·타원, 선, 그림자·안쪽 그림자) |
| 벡터·아이콘·불리언 | 자유형 도형 (점 편집 가능) |
| 글자 (굵기·크기·색·줄 간격·글머리표·밑줄·링크·「…」 말줄임) | 글상자. Figma와 같은 글꼴을 파일에 넣음 |
| 사진 채우기 (FILL·FIT) | 그림 (잘라내기 유지) |
| 레이어 구조 | 그룹 (기본 3단계), 선택 창 이름 = Figma 레이어 이름 |
| 마스크·블러·회전·블렌드 모드 | 그 레이어만 그림으로 (보고에 표시) |
| 프레임 이름·링크 | 슬라이드 노트 |

슬라이드 크기는 첫 프레임 크기를 따릅니다(1920×1080 → 16:9, 13.33in). 크기가 다른 프레임은 비율을 지켜 가운데에 맞춥니다.

## 준비

1. **Figma 토큰**: Figma → 왼쪽 위 계정 메뉴 → Settings → Security → Personal access tokens → Generate new token(범위 *File content: Read-only*). 변환할 파일을 열 수 있는 계정에서 발급하고, 창을 닫기 전에 복사합니다. 스크립트는 환경 변수 `FIGMA_TOKEN`을 먼저 보고, 없으면 `~/.config/figma-to-pptx/token` 파일을 읽습니다. **토큰을 대화창에 붙여 달라고 하지 말고**, 사용자가 토큰을 복사한 채로 자기 터미널에서 아래 한 줄을 직접 실행하게 안내합니다(토큰이 화면·기록에 남지 않음).
   - macOS: `mkdir -p ~/.config/figma-to-pptx && pbpaste > ~/.config/figma-to-pptx/token && chmod 600 ~/.config/figma-to-pptx/token`
   - Windows PowerShell: `New-Item -Force -ItemType Directory "$HOME\.config\figma-to-pptx" | Out-Null; Get-Clipboard | Set-Content -Encoding ascii -NoNewline "$HOME\.config\figma-to-pptx\token"`
2. **Python 3.10+**와 패키지 `python-pptx`, `pillow`, `fonttools`. `uv`가 있으면 설치 없이 바로 돌립니다.
3. 처음 한 번은 Figma에 쓰인 글꼴을 Google Fonts에서 받아 `~/.cache/figma-to-pptx`에 굵기별로 만들어 둡니다(한글 글꼴은 몇 분).

환경을 처음 갖췄으면 인터넷 없이 도는 자체 점검부터 합니다.

```bash
uv run --with python-pptx --with pillow --with fonttools python scripts/figma_to_pptx.py --self-test
```

## 실행

```bash
export FIGMA_TOKEN=figd_...
uv run --with python-pptx --with pillow --with fonttools python scripts/figma_to_pptx.py \
  "https://www.figma.com/design/<파일키>/<이름>?node-id=280-2" -o 로그인.pptx
```

링크의 `node-id`가 **페이지**면 그 페이지의 모든 프레임(섹션 안 포함), **섹션**이면 그 안의 프레임, **프레임**이면 그 한 장입니다. `node-id`가 없으면 첫 페이지를 씁니다.

| 옵션 | 뜻 |
|---|---|
| `--match REGEX` | 이름이 맞는 프레임만 (예: `'^\d+(-\d+)+ '` = 번호로 시작하는 지면만) |
| `--sort position\|name` | 슬라이드 순서. 기본은 캔버스 읽는 순서(위→아래, 왼→오), `name`은 이름의 번호 순 |
| `--group-depth N` | 그룹으로 남길 레이어 단계(기본 3, 0이면 그룹 없음) |
| `--font "Pretendard=/경로/Pretendard-Regular.ttf,/경로/Pretendard-Bold.ttf"` | Google Fonts에 없는 글꼴의 파일(TrueType). 여러 번 쓸 수 있음 |
| `--no-embed` | 글꼴을 넣지 않고 이름만 (파일이 작아지지만 글꼴이 없는 PC에서는 다르게 보임) |
| `--full-fonts` | 쓴 글자만이 아니라 글꼴 전체를 넣음 |
| `--cache DIR` | 받은 Figma 데이터를 두고 다시 쓰기 (여러 번 고쳐 돌릴 때) |

## 순서

1. 링크를 받지 못했으면 변환할 Figma 페이지나 프레임 링크를 묻습니다(Figma에서 페이지 이름 우클릭 → Copy link, 프레임은 선택 후 Copy link to selection). 토큰이 `FIGMA_TOKEN`이나 토큰 파일에 있는지만 확인하고(값은 보지 않음), 없으면 위 「준비」 1번대로 발급·저장을 안내합니다.
2. 위 명령으로 변환하고 마지막 보고를 읽습니다.
3. 보고에 아래가 있으면 사용자에게 그대로 알립니다.
   - `font not found …`: Google Fonts에 없는 글꼴입니다. 글꼴 파일을 `--font`로 주고 다시 돌립니다.
   - `font is OpenType CFF …`: .otf 글꼴이라 PowerPoint에 넣을 수 없습니다. TrueType(.ttf) 판을 구해 `--font`로 줍니다.
   - `pictures for layers PowerPoint cannot draw (mask|blur|rotated …)`: 그 레이어만 그림이라 그 부분은 고칠 수 없습니다.
   - `text boxes shrunk slightly …`: PowerPoint와 Figma 줄바꿈 차이로 넘치는 글상자만 최대 20% 줄였습니다.
4. 가능하면 PowerPoint로 열어 몇 장을 Figma와 비교합니다. 파일 경로, 슬라이드 수, 넣은 글꼴, 보고 항목을 짧게 전합니다.

## 알아 둘 점

- **Auto Layout·컴포넌트 연결은 넘어가지 않습니다.** PowerPoint에는 없는 기능이라 위치와 크기만 그대로 옮깁니다.
- **한글 줄바꿈**: Figma처럼 글자 단위로 넘기게 설정합니다. PowerPoint는 따르지만 LibreOffice 미리보기는 단어 단위로 보여 줍니다.
- **넣은 글꼴**: PowerPoint(Windows·Mac)는 파일 안의 글꼴을 씁니다. Mac PowerPoint에서 고쳐 저장하면 넣은 글꼴이 빠질 수 있으니, 고친 파일을 보낼 때는 Windows PowerPoint의 「파일에 글꼴 포함」을 켜고 저장합니다. Keynote는 넣은 글꼴을 쓰지 않습니다.
- **파일 크기**: 한글 글꼴은 한글 11,172자를 모두 넣어(새로 입력해도 같은 글꼴) 굵기마다 3MB 정도 늘어납니다.
- **데이터**: 디자인 데이터는 Figma API에서 받아 이 PC에서만 변환합니다. 밖으로 나가는 것은 Google Fonts·GitHub에서 글꼴을 받는 요청뿐입니다.
