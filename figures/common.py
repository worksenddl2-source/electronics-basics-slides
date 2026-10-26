"""theme.yaml을 읽어 manim·matplotlib 그림의 색과 글꼴을 통일한다."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
THEME = yaml.safe_load((ROOT / "config" / "theme.yaml").read_text(encoding="utf-8"))
FONT = THEME["font"]
C = {k: "#" + v for k, v in THEME["colors"].items()}


def manim_setup():
    """manim 장면 공통 설정: 1080p·30fps·어두운 무대."""
    from manim import config

    config.background_color = C["stage"]
    config.pixel_width, config.pixel_height = 1920, 1080
    config.frame_rate = 30
