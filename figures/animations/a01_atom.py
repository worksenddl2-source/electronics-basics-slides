"""01강: 원자 = 원자핵(+) + 주위를 도는 전자(−). 마지막에 전자 하나가 떨어져 나간다."""
from manim import (
    DOWN, LEFT, PI, UP, WHITE, Arrow, Create, Ellipse, FadeIn,
    GrowFromCenter, Scene, ValueTracker, VGroup, always_redraw, linear, smooth,
)

from parts import C, electron, label, manim_setup, particle

manim_setup()


class Main(Scene):
    def construct(self):
        center = DOWN * 0.35
        nucleus = particle(C["proton"], "+", r=0.55).move_to(center)
        orbits = VGroup(*[
            Ellipse(width=7.2, height=2.3, stroke_color=WHITE, stroke_opacity=0.28, stroke_width=2)
            .rotate(a).move_to(center)
            for a in (0, PI / 3, -PI / 3)
        ])
        t = ValueTracker(0)
        electrons = VGroup(*[electron(0.2) for _ in orbits])
        offsets = (0.0, 0.33, 0.66)

        def follow(i):
            def upd(e):
                e.move_to(orbits[i].point_from_proportion((t.get_value() + offsets[i]) % 1))
            return upd

        for i, e in enumerate(electrons):
            follow(i)(e)
            e.add_updater(follow(i))

        nucleus_label = label("원자핵 (+)", C["proton"]).move_to([-4.6, 2.2, 0])
        electron_label = label("전자 (−)", C["electron"]).move_to([5.0, 2.9, 0])
        nucleus_arrow = Arrow(nucleus_label.get_bottom(), nucleus.get_left() + UP * 0.2,
                              color=C["proton"], stroke_width=4, buff=0.15)
        electron_arrow = always_redraw(lambda: Arrow(
            electron_label.get_bottom(), electrons[0].get_center(),
            color=C["electron"], stroke_width=4, buff=0.35))

        self.play(GrowFromCenter(nucleus), run_time=0.8)
        self.play(Create(orbits), FadeIn(electrons), run_time=1.0)
        self.play(t.animate.set_value(1), FadeIn(nucleus_label), Create(nucleus_arrow),
                  run_time=2.5, rate_func=linear)
        self.add(electron_arrow)
        self.play(t.animate.set_value(2.2), FadeIn(electron_label), run_time=3, rate_func=linear)

        # 전자 하나가 원자를 떠난다 → 정전기·전류의 출발점
        self.remove(electron_arrow)
        leaver = electrons[0]
        leaver.clear_updaters()
        note = label("전자는 원자를 떠나 이동할 수 있다!", C["amber"], 38).to_edge(DOWN, buff=0.45)
        self.play(
            leaver.animate(rate_func=smooth).move_to([6.2, -1.6, 0]),
            t.animate(rate_func=linear).set_value(3.0),
            electron_label.animate.next_to([6.2, -1.6, 0], UP, buff=0.5).shift(LEFT * 0.4),
            FadeIn(note, shift=UP * 0.2),
            run_time=2.0,
        )
        self.play(t.animate.set_value(3.6), run_time=1.6, rate_func=linear)
        self.wait(0.4)
