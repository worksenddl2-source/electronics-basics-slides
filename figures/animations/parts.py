"""여러 manim 장면에서 같이 쓰는 부품: 전자, 양전하, 라벨."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import C, FONT, manim_setup  # noqa: E402,F401

from manim import Circle, Text, VGroup, WHITE  # noqa: E402


def particle(color, sign, r=0.18, glow=True):
    """빛나는 원 + 부호(+/−)로 된 입자."""
    parts = []
    if glow:
        for k, op in ((2.4, 0.08), (1.7, 0.16)):
            parts.append(Circle(radius=r * k, stroke_width=0).set_fill(color, op))
    parts.append(Circle(radius=r, stroke_width=0).set_fill(color, 1))
    parts.append(Text(sign, font=FONT, weight="BOLD", color=WHITE).scale(r * 2.6))
    return VGroup(*parts)


def electron(r=0.18, glow=True):
    return particle(C["electron"], "−", r, glow)


def proton(r=0.18, glow=True):
    return particle(C["proton"], "+", r, glow)


def label(text, color=WHITE, size=34):
    return Text(text, font=FONT, color=color, font_size=size)
