"""flow/inbox/<강>_<이름>_v<N>.png → assets/illustrations/<강>/<이름>.png (가장 높은 버전) + SOURCES.csv 기록.

사용: python scripts/ingest_flow.py
"""
import csv
import re
from datetime import date
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "flow" / "inbox"
DEST = ROOT / "assets" / "illustrations"
SOURCES = ROOT / "assets" / "SOURCES.csv"
NAME = re.compile(r"^(\d{2})_(.+?)(?:_v(\d+))?$")
MAX_W = 2400                                  # 슬라이드용으로 충분한 폭


def main():
    best = {}
    for f in INBOX.iterdir():
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        m = NAME.match(f.stem)
        if not m:
            print(f"  이름 규칙 불일치, 건너뜀: {f.name}  (예: 01_cover_v2.png)")
            continue
        key, ver = (m[1], m[2]), int(m[3] or 0)
        if key not in best or ver > best[key][0]:
            best[key] = (ver, f)

    rows = list(csv.DictReader(SOURCES.open(encoding="utf-8"))) if SOURCES.exists() else []
    known = {r["file"]: r for r in rows}
    for (lec, name), (ver, f) in sorted(best.items()):
        out = DEST / lec / f"{name}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        img = Image.open(f).convert("RGB")
        if img.width > MAX_W:
            img = img.resize((MAX_W, round(img.height * MAX_W / img.width)), Image.LANCZOS)
        img.save(out, optimize=True)
        rel = out.relative_to(ROOT).as_posix()
        known[rel] = {"file": rel, "kind": "illustration", "source": f"Google Flow ({f.name})",
                      "created": date.today().isoformat(), "license": "AI 생성 (Google Flow)",
                      "note": f"prompt: flow/prompts/{lec}_lecture.md#{lec}_{name}"}
        print(f"  {f.name} → {rel}")

    with SOURCES.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "kind", "source", "created", "license", "note"])
        w.writeheader()
        w.writerows(known.values())


if __name__ == "__main__":
    main()
