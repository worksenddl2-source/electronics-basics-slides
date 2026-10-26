"""build/ 결과물 → docs/ (GitHub Pages 사이트)

- 최신 PPTX → docs/downloads/lectureNN.pptx
- manim 영상·포스터 → docs/media/
- 슬라이드 미리보기 PNG → docs/previews/NN/ (Windows + PowerPoint 필요, 없으면 건너뜀)
- docs/index.html 생성 (config/course.yaml + content/*/slides.yaml 기준)

사용: python scripts/publish_site.py
"""
import html
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BUILD = ROOT / "build"
COURSE = yaml.safe_load((ROOT / "config" / "course.yaml").read_text(encoding="utf-8"))
COL = yaml.safe_load((ROOT / "config" / "theme.yaml").read_text(encoding="utf-8"))["colors"]
REPO_URL = "https://github.com/worksenddl2-source/electronics-basics-slides"

EXPORT_PS = r"""
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open('{src}', $true, $false, $false)
$pres.Export('{out}', 'PNG', 1280, 720)
$pres.Close()
"""


def latest_pptx(deck):
    """build_deck.py 가 '_새버전' 으로 저장했을 수도 있으니 가장 최근 파일을 고른다."""
    files = sorted(BUILD.glob(f"pptx/{deck['id']}_*.pptx"), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None


def export_previews(pptx, out_dir):
    if sys.platform != "win32":
        print("  미리보기: PowerPoint가 없어 건너뜀")
        return
    tmp = BUILD / "preview_tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    EXPORT_PS.format(src=pptx, out=tmp)], check=True)
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True)
    for f in tmp.iterdir():                          # '슬라이드3.PNG' → 'slide-03.png'
        n = int("".join(ch for ch in f.stem if ch.isdigit()))
        shutil.move(f, out_dir / f"slide-{n:02d}.png")
    shutil.rmtree(tmp, ignore_errors=True)


def publish_lecture(lec):
    src = ROOT / "content" / lec["dir"] / "slides.yaml"
    if not src.exists():
        return None
    deck = yaml.safe_load(src.read_text(encoding="utf-8"))
    pptx = latest_pptx(deck)
    if pptx is None:
        print(f"  {lec['id']}: PPTX 없음 — build_deck.py 먼저 실행")
        return None
    dl = DOCS / "downloads" / f"lecture{lec['id']}.pptx"
    dl.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(pptx, dl)

    videos = []
    for s in deck["slides"]:
        name = s.get("animation")
        if name and (BUILD / "media" / f"{name}.mp4").exists() and name not in [v[0] for v in videos]:
            for ext in (".mp4", ".png"):
                (DOCS / "media").mkdir(parents=True, exist_ok=True)
                shutil.copy(BUILD / "media" / f"{name}{ext}", DOCS / "media" / f"{name}{ext}")
            videos.append((name, s["title"]))

    export_previews(pptx, DOCS / "previews" / lec["id"])
    previews = sorted((DOCS / "previews" / lec["id"]).glob("slide-*.png"))
    sources = next((s["items"] for s in deck["slides"] if s["layout"] == "sources"), [])
    print(f"  {lec['id']}: {pptx.name} · 영상 {len(videos)} · 미리보기 {len(previews)}")
    return {"deck": deck, "videos": videos, "previews": previews, "sources": sources,
            "download": dl, "size_mb": dl.stat().st_size / 1e6}


# ── HTML ────────────────────────────────────────────────

def e(s):
    return html.escape(str(s))


def lecture_cards(published):
    cards = []
    for lec in COURSE["lectures"]:
        done = lec["id"] in published
        status = '<span class="tag on">공개</span>' if done else '<span class="tag">준비 중</span>'
        inner = (f'<span class="num">{e(lec["id"])}</span><span class="name">{e(lec["title"])}</span>{status}')
        cards.append(f'<a class="lec on" href="#lecture-{lec["id"]}">{inner}</a>' if done
                     else f'<div class="lec">{inner}</div>')
    return "\n".join(cards)


def lecture_section(lid, p):
    d = p["deck"]
    slides = "\n".join(
        f'<a href="previews/{lid}/{f.name}" target="_blank" rel="noopener">'
        f'<img src="previews/{lid}/{f.name}" alt="{e(d["title"])} 슬라이드 {i}" loading="lazy"></a>'
        for i, f in enumerate(p["previews"], start=1))
    videos = "\n".join(
        f'<figure><video controls preload="none" poster="media/{n}.png" playsinline>'
        f'<source src="media/{n}.mp4" type="video/mp4"></video><figcaption>{e(t)}</figcaption></figure>'
        for n, t in p["videos"])
    srcs = "\n".join(
        f'<li><strong>{e(s["name"])}</strong><span>{e(s["use"])}</span><em>{e(s["license"])}</em></li>'
        for s in p["sources"])
    return f"""
<section class="lecture" id="lecture-{lid}">
  <div class="lec-head">
    <div>
      <p class="kicker">LECTURE {e(lid)}</p>
      <h2>{e(d["title"])}</h2>
      <p class="sub">{e(d.get("subtitle", ""))}</p>
    </div>
    <a class="btn" href="downloads/lecture{lid}.pptx" download>PPTX 다운로드 <small>{p["size_mb"]:.1f} MB · {len(d["slides"])}장</small></a>
  </div>
  <h3>애니메이션 <small>manim으로 제작 · 슬라이드 안에서는 클릭하면 재생</small></h3>
  <div class="videos">{videos}</div>
  <h3>슬라이드 미리보기 <small>클릭하면 크게 보기</small></h3>
  <div class="slides">{slides}</div>
  <h3>참고자료</h3>
  <ul class="sources">{srcs}</ul>
</section>"""


def render(published):
    c = COL
    sections = "\n".join(lecture_section(lid, p) for lid, p in published.items())
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>전자전기 기초 강의</title>
<meta name="description" content="비전공자를 위한 전자전기 기초 강의자료 — 슬라이드, 애니메이션, PPTX 다운로드">
<style>
:root {{
  --stage: #{c["stage"]}; --stage-2: #{c["stage_2"]}; --ink: #{c["ink"]}; --muted: #{c["muted"]};
  --paper: #{c["paper"]}; --soft: #{c["soft"]}; --line: #{c["line"]};
  --amber: #{c["amber"]}; --electron: #{c["electron"]}; --proton: #{c["proton"]};
  --bg: var(--paper); --fg: var(--ink); --panel: var(--soft); --sub: var(--muted);
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #0F1226; --fg: #E8EAF4; --panel: var(--stage-2); --sub: #A3A8C3; --line: #343A66; }}
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--fg);
  font-family: "Pretendard", "Malgun Gothic", "Apple SD Gothic Neo", system-ui, sans-serif;
  line-height: 1.6; word-break: keep-all; }}
a {{ color: inherit; }}
.wrap {{ max-width: 1120px; margin: 0 auto; padding: 0 20px; }}
header {{ background: var(--stage); color: #fff; padding: 72px 0 56px; }}
.kicker {{ color: var(--amber); font-weight: 700; letter-spacing: .08em; font-size: 14px; margin: 0 0 8px; }}
h1 {{ font-size: clamp(34px, 6vw, 56px); line-height: 1.15; margin: 0 0 16px; }}
header p.lead {{ font-size: clamp(16px, 2.2vw, 20px); color: #D8DBEA; max-width: 640px; margin: 0 0 28px; }}
.pills {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.pill {{ border: 1px solid #3A4070; border-radius: 999px; padding: 6px 14px; font-size: 14px; color: #D8DBEA; }}
.dot {{ display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 6px; vertical-align: 1px; }}
main section {{ padding: 56px 0 8px; }}
h2 {{ font-size: clamp(26px, 4vw, 34px); margin: 0 0 6px; }}
h3 {{ font-size: 20px; margin: 40px 0 14px; }}
h3 small, .sub {{ color: var(--sub); font-weight: 400; font-size: 14px; }}
h3 small {{ margin-left: 8px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(200px, 100%), 1fr)); gap: 12px; margin-top: 20px; }}
.lec {{ display: flex; align-items: center; gap: 12px; padding: 14px 16px; border-radius: 14px;
  background: var(--panel); text-decoration: none; color: var(--sub); }}
.lec.on {{ color: var(--fg); outline: 2px solid var(--amber); }}
.lec .num {{ font-weight: 800; font-size: 18px; color: var(--amber); }}
.lec .name {{ flex: 1; font-weight: 600; }}
.tag {{ font-size: 12px; padding: 2px 8px; border-radius: 999px; border: 1px solid var(--line); white-space: nowrap; }}
.tag.on {{ background: var(--amber); color: var(--stage); border-color: var(--amber); font-weight: 700; }}
.lec-head {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 20px; }}
.btn {{ display: inline-flex; flex-direction: column; background: var(--amber); color: var(--stage);
  padding: 12px 22px; border-radius: 12px; font-weight: 800; text-decoration: none; }}
.btn small {{ font-weight: 500; font-size: 12px; }}
.videos {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(320px, 100%), 1fr)); gap: 16px; }}
figure {{ margin: 0; }}
video {{ width: 100%; aspect-ratio: 16/9; border-radius: 12px; background: var(--stage); display: block; }}
figcaption {{ font-size: 14px; color: var(--sub); margin-top: 6px; }}
.slides {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(240px, 100%), 1fr)); gap: 12px; }}
.slides img {{ width: 100%; aspect-ratio: 16/9; object-fit: cover; border-radius: 10px;
  border: 1px solid var(--line); display: block; }}
.sources {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }}
.sources li {{ background: var(--panel); border-radius: 12px; padding: 12px 16px;
  display: grid; grid-template-columns: 1fr auto; gap: 2px 16px; }}
.sources span {{ color: var(--sub); font-size: 14px; grid-column: 1; }}
.sources em {{ font-style: normal; font-size: 13px; color: var(--sub); grid-column: 2; grid-row: 1 / span 2; align-self: center; }}
.how {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); gap: 12px; }}
.how div {{ background: var(--panel); border-radius: 14px; padding: 18px; }}
.how b {{ display: block; margin-bottom: 4px; }}
.how p {{ margin: 0; color: var(--sub); font-size: 15px; }}
footer {{ margin-top: 64px; padding: 28px 0 40px; border-top: 1px solid var(--line); color: var(--sub); font-size: 14px; }}
@media (max-width: 560px) {{
  .grid {{ grid-template-columns: 1fr 1fr; }}
  .lec {{ flex-wrap: wrap; gap: 4px 10px; }}
  .sources li {{ grid-template-columns: 1fr; }}
  .sources em {{ grid-column: 1; grid-row: auto; }}
  .videos {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <p class="kicker">{e(COURSE["course"])} · {e(COURSE["audience"])}용 강의자료</p>
    <h1>눈에 보이지 않는 전기를,<br>눈으로 보면서 배우기</h1>
    <p class="lead">전기를 처음 배우는 사람을 위한 10강짜리 강의 슬라이드입니다.
    개념마다 움직이는 애니메이션과 그림으로 설명하고, 공개 교재를 근거로 삼았습니다.</p>
    <div class="pills">
      <span class="pill"><span class="dot" style="background:var(--electron)"></span>manim 애니메이션</span>
      <span class="pill"><span class="dot" style="background:var(--amber)"></span>Google Flow 일러스트</span>
      <span class="pill"><span class="dot" style="background:var(--proton)"></span>OpenStax 교재 기준</span>
    </div>
  </div>
</header>
<main class="wrap">
  <section id="lectures">
    <h2>강의 목록</h2>
    <p class="sub">공개된 강의를 누르면 슬라이드와 영상으로 이동합니다.</p>
    <div class="grid">{lecture_cards(published)}</div>
  </section>
  {sections}
  <section id="how">
    <h2>어떻게 만들었나</h2>
    <div class="how">
      <div><b>내용</b><p>강의마다 slides.yaml 한 파일에 슬라이드 내용을 적습니다. 근거가 된 교재 절은 각 슬라이드 아래에 표시합니다.</p></div>
      <div><b>애니메이션</b><p>Python manim으로 전자의 움직임을 그려 MP4로 만들고 슬라이드에 넣습니다.</p></div>
      <div><b>일러스트</b><p>Google Flow로 생성합니다. 한글이 깨지지 않도록 그림에는 글자를 넣지 않고 라벨은 슬라이드에서 얹습니다.</p></div>
      <div><b>빌드</b><p>python-pptx가 이 모두를 모아 PPTX를 만들고, 같은 결과물로 이 페이지도 만듭니다.</p></div>
    </div>
  </section>
</main>
<footer>
  <div class="wrap">
    소스 코드와 제작 방법: <a href="{REPO_URL}">{REPO_URL.removeprefix("https://")}</a><br>
    참고 교재: OpenStax <i>College Physics 2e</i> (CC BY 4.0) · SparkFun "What is Electricity?" (CC BY-SA 4.0)
  </div>
</footer>
</body>
</html>
"""


if __name__ == "__main__":
    published = {}
    for lec in COURSE["lectures"]:
        if (p := publish_lecture(lec)):
            published[lec["id"]] = p
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    (DOCS / "index.html").write_text(render(published), encoding="utf-8")
    print(f"saved docs/index.html  (공개 강의 {len(published)}개)")
