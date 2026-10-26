"""Flow 이미지 정리 → manim 렌더 → PPTX 빌드를 한 번에.

사용: python scripts/build_all.py [강 번호 ...]
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for step in ("ingest_flow.py", "make_animations.py"):
    subprocess.run([sys.executable, str(HERE / step)], check=True)
subprocess.run([sys.executable, str(HERE / "build_deck.py"), *sys.argv[1:]], check=True)
