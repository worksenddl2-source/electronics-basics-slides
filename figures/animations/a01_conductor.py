"""01강: 도체(구리)는 자유전자가 돌아다니고, 부도체(고무)는 전자가 원자에 묶여 있다.

근거: OpenStax College Physics 2e, 18.2 Conductors and Insulators
"""
import numpy as np
from manim import UP, WHITE, FadeIn, Line, Scene, VGroup

from parts import C, electron, label, manim_setup, particle

manim_setup()

LEFT_BOX = (-6.3, -0.7)        # 구리 영역 x 범위
RIGHT_BOX = (0.7, 6.3)         # 고무 영역 x 범위
Y_BOX = (-2.3, 1.7)


def lattice(x0, x1):
    xs = np.linspace(x0 + 0.6, x1 - 0.6, 4)
    ys = np.linspace(Y_BOX[0] + 0.5, Y_BOX[1] - 0.5, 3)
    return [np.array([x, y, 0.0]) for y in ys for x in xs]


class Main(Scene):
    def construct(self):
        rng = np.random.default_rng(3)
        divider = Line([0, 2.6, 0], [0, -3.4, 0], stroke_color=WHITE, stroke_opacity=0.15)

        # 왼쪽: 구리 — 원자핵 격자 사이를 자유전자가 돌아다님
        cu_sites = lattice(*LEFT_BOX)
        cu_atoms = VGroup(*[particle(C["proton"], "+", r=0.2, glow=False).move_to(p) for p in cu_sites])
        n = 12
        pos = np.column_stack([rng.uniform(*LEFT_BOX, n), rng.uniform(*Y_BOX, n)])
        vel = rng.normal(0, 1, (n, 2))
        vel = vel / np.linalg.norm(vel, axis=1, keepdims=True) * 1.6
        free = VGroup(*[electron(0.12) for _ in range(n)])

        def wander(group, dt):
            pos[:] += vel * dt
            for axis, (lo, hi) in ((0, LEFT_BOX), (1, Y_BOX)):       # 벽에 닿으면 튕김
                out = (pos[:, axis] < lo) | (pos[:, axis] > hi)
                vel[out, axis] *= -1
                pos[:, axis] = np.clip(pos[:, axis], lo, hi)
            for e, p in zip(group, pos):
                e.move_to([p[0], p[1], 0])

        wander(free, 0)
        free.add_updater(wander)

        # 오른쪽: 고무 — 전자가 각자 자기 원자 주위만 맴돎
        rb_sites = lattice(*RIGHT_BOX)
        rb_atoms = VGroup(*[particle(C["proton"], "+", r=0.2, glow=False).move_to(p) for p in rb_sites])
        phase = rng.uniform(0, 2 * np.pi, len(rb_sites))
        clock = {"t": 0.0}
        bound = VGroup(*[electron(0.12) for _ in rb_sites])

        def orbit(group, dt):
            clock["t"] += dt
            for e, c, ph in zip(group, rb_sites, phase):
                a = 3.2 * clock["t"] + ph
                e.move_to(c + 0.42 * np.array([np.cos(a), np.sin(a), 0]))

        orbit(bound, 0)
        bound.add_updater(orbit)

        cu_title = label("구리 (도체)", C["amber"], 40).move_to([-3.5, 2.9, 0])
        rb_title = label("고무 (부도체)", WHITE, 40).move_to([3.5, 2.9, 0])
        cu_note = label("자유전자가 자유롭게 돌아다닌다", C["electron"], 30).move_to([-3.5, -3.1, 0])
        rb_note = label("전자가 원자에 꽉 묶여 있다", WHITE, 30).move_to([3.5, -3.1, 0])

        self.play(FadeIn(divider), FadeIn(cu_title), FadeIn(rb_title),
                  FadeIn(cu_atoms), FadeIn(rb_atoms), run_time=0.8)
        self.add(free, bound)
        self.play(FadeIn(free), FadeIn(bound), run_time=0.6)
        self.wait(1.6)
        self.play(FadeIn(cu_note, shift=UP * 0.2), run_time=0.6)
        self.wait(1.4)
        self.play(FadeIn(rb_note, shift=UP * 0.2), run_time=0.6)
        self.wait(3.0)
