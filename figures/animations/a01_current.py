"""01강: 스위치 OFF면 전자가 제자리에서 꼼지락, ON이면 다 함께 한 방향으로 → 전류, 전구가 켜진다."""
import numpy as np
from manim import (
    DOWN, UP, WHITE, Circle, FadeIn, RoundedRectangle, Scene, Transform, ValueTracker,
    VGroup, smooth,
)

from parts import C, electron, label, manim_setup

manim_setup()

X_MIN, X_MAX = -5.6, 4.9       # 양 끝은 건전지·전구 뒤에 숨는다
WIRE_Y = 0.0


class Main(Scene):
    def construct(self):
        rng = np.random.default_rng(7)
        wire = RoundedRectangle(width=11.2, height=1.7, corner_radius=0.85,
                                stroke_color=WHITE, stroke_opacity=0.3, stroke_width=3)
        wire.set_fill(C["stage_2"], 1).move_to([-0.2, WIRE_Y, 0])

        n = 24
        base = np.column_stack([
            np.linspace(X_MIN, X_MAX, n, endpoint=False) + rng.uniform(0, 0.3, n),
            WIRE_Y + rng.uniform(-0.45, 0.45, n),
        ])
        freq = rng.uniform(5, 9, (n, 2))
        phase = rng.uniform(0, 2 * np.pi, (n, 2))
        drift = ValueTracker(0)          # 0 = OFF, 1 = ON
        clock = {"t": 0.0}
        electrons = VGroup(*[electron(0.13) for _ in range(n)])

        def jiggle(group, dt):
            clock["t"] += dt
            base[:, 0] += drift.get_value() * 1.7 * dt
            span = X_MAX - X_MIN
            base[:, 0] = (base[:, 0] - X_MIN) % span + X_MIN
            wobble = 0.09 * np.sin(freq * clock["t"] + phase) * (1 - 0.6 * drift.get_value())
            for i, e in enumerate(group):
                e.move_to([base[i, 0] + wobble[i, 0], base[i, 1] + wobble[i, 1], 0])

        jiggle(electrons, 0)
        electrons.add_updater(jiggle)

        # 왼쪽: 건전지(전자를 밀어주는 펌프), 오른쪽: 전구
        battery = RoundedRectangle(width=1.6, height=2.6, corner_radius=0.25, stroke_width=0)
        battery.set_fill("#3A4070", 1).move_to([-6.0, WIRE_Y, 0])
        battery_tag = label("건전지", WHITE, 28).next_to(battery, DOWN, buff=0.25)
        bulb_glow = VGroup(*[Circle(radius=r, stroke_width=0).set_fill(C["amber"], 0)
                             for r in (1.55, 1.25)])
        bulb = Circle(radius=1.05, stroke_color=WHITE, stroke_opacity=0.5, stroke_width=3)
        bulb.set_fill(C["stage_2"], 1)
        bulb_group = VGroup(bulb_glow, bulb).move_to([5.6, WIRE_Y, 0])
        bulb_tag = label("전구", WHITE, 28).next_to(bulb_glow, DOWN, buff=0.15)

        caption = label("스위치 OFF — 전자는 제자리에서 꼼지락", WHITE, 40).to_edge(UP, buff=0.7)
        caption_on = label("스위치 ON — 모두 함께 한 방향으로 = 전류", C["amber"], 40).to_edge(UP, buff=0.7)

        self.play(FadeIn(wire), FadeIn(caption), run_time=0.6)
        self.add(electrons, battery, bulb_group)   # 전자 → 전선 위, 건전지·전구 → 전자 위
        self.play(FadeIn(electrons), FadeIn(battery), FadeIn(bulb_group),
                  FadeIn(battery_tag), FadeIn(bulb_tag), run_time=0.6)
        self.wait(2.6)
        self.play(
            Transform(caption, caption_on),
            drift.animate(rate_func=smooth).set_value(1),
            bulb.animate.set_fill(C["amber"], 1),
            bulb_glow[0].animate.set_fill(C["amber"], 0.12),
            bulb_glow[1].animate.set_fill(C["amber"], 0.25),
            run_time=1.2,
        )
        self.wait(4.5)
