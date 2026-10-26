"""01강: 다른 부호는 끌어당기고(+−), 같은 부호는 밀어낸다(−−)."""
from manim import (
    LEFT, RIGHT, WHITE, Arrow, FadeIn, GrowArrow, Line, Scene, VGroup, Write,
    rush_from, rush_into,
)

from parts import C, electron, label, manim_setup, proton

manim_setup()


def force_arrows(a, b, inward):
    """두 입자 사이의 힘 방향 화살표 한 쌍."""
    if inward:
        return VGroup(
            Arrow(a.get_center() + RIGHT * 0.5, a.get_center() + RIGHT * 1.6, color=C["amber"], buff=0),
            Arrow(b.get_center() + LEFT * 0.5, b.get_center() + LEFT * 1.6, color=C["amber"], buff=0),
        )
    return VGroup(
        Arrow(a.get_center() + LEFT * 0.5, a.get_center() + LEFT * 1.6, color=C["amber"], buff=0),
        Arrow(b.get_center() + RIGHT * 0.5, b.get_center() + RIGHT * 1.6, color=C["amber"], buff=0),
    )


class Main(Scene):
    def construct(self):
        top_y, bot_y = 1.7, -1.9
        divider = Line([-6.6, -0.1, 0], [6.6, -0.1, 0], stroke_color=WHITE, stroke_opacity=0.15)

        # 1) + 와 − : 끌어당긴다
        p, e = proton(0.32).move_to([-2.6, top_y, 0]), electron(0.32).move_to([2.6, top_y, 0])
        top_tag = label("다른 부호", WHITE, 32).move_to([-5.6, top_y, 0])
        top_res = label("끌어당긴다", C["amber"], 40).move_to([5.3, top_y, 0])
        pull = force_arrows(p, e, inward=True)

        self.play(FadeIn(top_tag), FadeIn(p, scale=0.6), FadeIn(e, scale=0.6), run_time=0.8)
        self.play(*[GrowArrow(a) for a in pull], run_time=0.6)
        self.wait(0.4)
        self.play(p.animate.move_to([-0.45, top_y, 0]), e.animate.move_to([0.45, top_y, 0]),
                  pull.animate.set_opacity(0), rate_func=rush_into, run_time=1.1)
        self.play(Write(top_res), run_time=0.6)
        self.add(divider)

        # 2) − 와 − : 밀어낸다
        e1, e2 = electron(0.32).move_to([-0.55, bot_y, 0]), electron(0.32).move_to([0.55, bot_y, 0])
        bot_tag = label("같은 부호", WHITE, 32).move_to([-5.6, bot_y, 0])
        bot_res = label("밀어낸다", C["amber"], 40).move_to([5.3, bot_y, 0])
        push = force_arrows(e1, e2, inward=False)

        self.play(FadeIn(bot_tag), FadeIn(e1, scale=0.6), FadeIn(e2, scale=0.6), run_time=0.8)
        self.play(*[GrowArrow(a) for a in push], run_time=0.6)
        self.wait(0.4)
        self.play(e1.animate.move_to([-2.9, bot_y, 0]), e2.animate.move_to([2.9, bot_y, 0]),
                  push.animate.set_opacity(0), rate_func=rush_from, run_time=1.1)
        self.play(Write(bot_res), run_time=0.6)
        self.wait(1.5)
