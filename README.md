# 전자전기 기초 — 비전공자용 강의자료

전기를 처음 배우는 사람을 위한 10강짜리 PPTX 강의 슬라이드입니다.
개념마다 **움직이는 애니메이션(manim)**과 **일러스트(Google Flow)**로 설명하고,
공개 교재 **OpenStax *College Physics 2e***를 근거로 삼습니다.

**강의 페이지(슬라이드 미리보기 · 영상 · PPTX 다운로드):**
https://worksenddl2-source.github.io/electronics-basics-slides/

## 진행 상황

| 강 | 주제 | 상태 | 애니메이션 (manim) | 일러스트 (Google Flow) |
|---|---|---|---|---|
| 01 | 전기란 무엇인가 | **맛보기 공개 (12장)** | 원자, 전하 규칙, 도체·부도체, 전류 | 표지·스위치·풍선 — 생성 대기 |
| 02 | 전압·전류·저항 | 준비 중 | 수위차와 물 흐름 | 물탱크·수도관 비유 |
| 03 | 옴의 법칙 | 준비 중 | V-I 직선 그리기 | V=IR 삼각형 |
| 04 | 직렬과 병렬 | 준비 중 | 전류 갈라짐 비교 | 전구 줄 |
| 05 | 전력과 에너지 | 준비 중 | — | 계량기 |
| 06 | 직류와 교류 | 준비 중 | 회전 코일 → 사인파 | 발전소→콘센트 |
| 07 | 커패시터와 인덕터 | 준비 중 | 충방전 곡선 | 물풍선·물레방아 |
| 08 | 반도체와 다이오드 | 준비 중 | 정방향 통과 / 역방향 차단 | 일방통행 밸브 |
| 09 | 트랜지스터 | 준비 중 | 작은 전류로 큰 전류 제어 | 수도꼭지 |
| 10 | 디지털 기초 | 준비 중 | AND/OR 신호 흐름 | 전등 스위치 0/1 |

### 01강 구성
OpenStax 각 절의 흐름(학습 목표 → 개념 → PhET 탐구 → 요약 → 확인 문제)을 따릅니다.

표지 → 오늘의 질문 → 학습 목표 → 원자 → 전하 규칙 → 도체/부도체 → 정전기 → 전류
→ PhET 직접 해보기(QR) → 핵심 정리 → OX 퀴즈 → 참고자료

- 슬라이드마다 아래쪽에 근거가 된 교재 절을 표시합니다.
- 발표자 노트에 강의 멘트와 퀴즈 정답이 들어 있습니다.

## 참고자료

| 자료 | 용도 | 라이선스 |
|---|---|---|
| [OpenStax, *College Physics 2e*](https://openstax.org/details/books/college-physics-2e) — 18.1, 18.2, 20.1 | 기준 교재: 개념·학습 목표·수치 | CC BY 4.0 |
| [SparkFun, "What is Electricity?"](https://learn.sparkfun.com/tutorials/what-is-electricity/all) | 설명 순서와 비유 | CC BY-SA 4.0 |
| [PhET "풍선과 정전기"](https://phet.colorado.edu/ko/simulations/balloons-and-static-electricity) | 수업 중 탐구 활동 | PhET 이용 조건 |
| [NIST CODATA](https://physics.nist.gov/cuu) | 양성자/전자 질량비 | 공공 자료 |

수치의 근거와 확인 여부는 [`references/facts.yaml`](references/facts.yaml)에,
강별 조사 내용(흔한 오해, 비유 후보)은 [`references/lectures/`](references/lectures/)에 정리되어 있습니다.

## 폴더 구조

```
config/          theme.yaml (색·글꼴 — PPTX·manim·사이트 공통), course.yaml (강의 목록)
content/         강별 slides.yaml — 슬라이드 내용은 여기만 고치면 된다
references/      참고문헌, 용어집, 수치 근거, 강별 리서치 노트
flow/            Google Flow 화풍 가이드·프롬프트, inbox/ (생성 이미지를 넣는 곳)
assets/          정리된 일러스트·사진 + SOURCES.csv (출처 기록)
figures/         manim 애니메이션 소스 (animations/a<강>_<이름>.py)
scripts/         빌드 스크립트
docs/            GitHub Pages 사이트 (publish_site.py가 생성)
build/           빌드 결과물 (git 제외)
```

## 빌드 방법

Windows + Python 3.14 기준입니다. 미리보기 이미지를 만들려면 PowerPoint가 필요합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt

.\.venv\Scripts\python scripts\build_all.py 01      # Flow 이미지 정리 → manim 렌더 → PPTX
.\.venv\Scripts\python scripts\publish_site.py      # docs/ 사이트 갱신 (미리보기·영상·다운로드)
```

| 스크립트 | 하는 일 |
|---|---|
| `ingest_flow.py` | `flow/inbox/01_cover_v2.png` → `assets/illustrations/01/cover.png` (가장 높은 버전), SOURCES.csv에 기록 |
| `make_animations.py` | manim 장면 렌더 → `build/media/*.mp4` + 포스터 PNG (소스가 바뀐 것만 다시 렌더) |
| `build_deck.py` | `slides.yaml` → PPTX. 이미지가 없으면 점선 자리표시를 넣고 목록을 출력 |
| `publish_site.py` | PPTX·영상·미리보기를 `docs/`로 복사하고 `index.html` 생성 |

### slides.yaml 레이아웃

`cover` 표지 · `question` 질문 · `objectives` 학습 목표 · `video` 애니메이션 + 설명 ·
`figure` 그림 + 단계 · `try` PhET 실습(QR) · `summary` 요약 카드 · `quiz` OX 퀴즈 · `sources` 참고자료

```yaml
- layout: video
  title: 전자가 잘 다니는 물질, 못 다니는 물질
  animation: a01_conductor              # build/media/a01_conductor.mp4
  points:
    - {label: 도체, color: amber, text: "자유전자가 있어 전기가 잘 흐른다"}
  source: OpenStax College Physics 2e, 18.2   # 슬라이드 아래 출처
  notes: 발표자 노트
```

## 그림 제작 규칙

- **일러스트는 Google Flow로 만듭니다.** `flow/style_guide.md`의 공통 문구를 모든 프롬프트 앞에 붙여 화풍을 맞춥니다.
- **그림 안에는 글자를 넣지 않습니다.** 한글이 깨지기 때문에 라벨은 PPTX 텍스트로 얹습니다.
- **색은 통일합니다.** 전자는 청록(`#2EC4E6`), (+)는 코랄(`#F25C54`), 에너지와 빛은 앰버(`#FFB400`)로 그림과 애니메이션에 똑같이 씁니다.
- **외부 이미지는 출처를 기록합니다.** 모든 외부 이미지는 `assets/SOURCES.csv`에 출처와 라이선스를 남깁니다.

## 남은 작업

- [ ] 01강 Flow 일러스트 3장 생성 (`flow/prompts/01_lecture.md`)
- [ ] 01강 전선 단면 실물 사진
- [ ] 220V/60Hz 한전 공식 자료, NIST 질량비 직접 확인 (`references/facts.yaml`)
- [ ] 02강 제작
