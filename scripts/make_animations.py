"""figures/animations/a*.py 의 Main 장면을 렌더 → build/media/<이름>.mp4 + 포스터 PNG.

사용: python scripts/make_animations.py [이름 ...]   (이름 생략 시 전체, 소스가 바뀐 것만 다시 렌더)
"""
import shutil
import subprocess
import sys
from pathlib import Path

import av

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "figures" / "animations"
OUT = ROOT / "build" / "media"
CACHE = ROOT / "build" / "manim_cache"


def poster(mp4: Path, png: Path):
    """마지막 프레임을 포스터로 저장 (PDF 배포본·슬라이드 정지 화면용)."""
    with av.open(str(mp4)) as box:
        last = None
        for frame in box.decode(video=0):
            last = frame
        last.to_image().save(png)


def render(src: Path, force=False):
    mp4, png = OUT / f"{src.stem}.mp4", OUT / f"{src.stem}.png"
    deps = [src, SRC / "parts.py", ROOT / "figures" / "common.py", ROOT / "config" / "theme.yaml"]
    if not force and mp4.exists() and mp4.stat().st_mtime > max(d.stat().st_mtime for d in deps):
        print(f"skip  {src.stem}")
        return
    print(f"render {src.stem}")
    subprocess.run([sys.executable, "-m", "manim", "render", "-q", "h", "--fps", "30",
                    "--media_dir", str(CACHE), "-o", src.stem, str(src), "Main"],
                   check=True, cwd=SRC)
    built = next(CACHE.rglob(f"{src.stem}.mp4"))
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy(built, mp4)
    poster(mp4, png)


if __name__ == "__main__":
    names = sys.argv[1:]
    for f in sorted(SRC.glob("a*.py")):
        if not names or f.stem in names:
            render(f, force=bool(names))
