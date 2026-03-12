"""
The Swing That Keeps a Secret — deep-dive narrative version.
Every concept explained with parallel metaphors and graphics.
Run:  .venv/bin/python -m manimlib test-video-sripts/quantum_paper_explainer_scene.py QuantumPaperExplainer -w
"""

from manimlib import *
import numpy as np

CENTER = np.array([0, 0, 0])
SWING_BAR_Y = 1.8
SEAT_Y = -0.4
SEAT_W, SEAT_H = 0.9, 0.25
COIN_R = 0.12


# ═══════════════════════════════════════════
#  Swing diagram
# ═══════════════════════════════════════════


def _swing_world(include_coin=True, push_scale=1.0, coin_on_seat=True):
    bar = Line(
        CENTER + np.array([-0.8, SWING_BAR_Y, 0]),
        CENTER + np.array([0.8, SWING_BAR_Y, 0]),
        color=GREY_B,
        stroke_width=6,
    )
    lr = Line(
        CENTER + np.array([-0.35, SWING_BAR_Y - 0.1, 0]),
        CENTER + np.array([-SEAT_W / 2 - 0.02, SEAT_Y + SEAT_H / 2, 0]),
        color=GREY_B,
        stroke_width=3,
    )
    rr = Line(
        CENTER + np.array([0.35, SWING_BAR_Y - 0.1, 0]),
        CENTER + np.array([SEAT_W / 2 + 0.02, SEAT_Y + SEAT_H / 2, 0]),
        color=GREY_B,
        stroke_width=3,
    )
    seat = Rectangle(width=SEAT_W, height=SEAT_H)
    seat.set_fill(GREY_C, opacity=0.9).set_stroke(GREY_A, width=2)
    seat.move_to(CENTER + np.array([0, SEAT_Y, 0]))
    swing = VGroup(bar, lr, rr, seat)

    p_end = CENTER + np.array([-SEAT_W / 2 - 0.3, SEAT_Y, 0])
    p_st = p_end + LEFT * (0.8 * push_scale + 0.5)
    pa = Arrow(
        p_st,
        p_end,
        thickness=0.06 * push_scale,
        color=GREEN_C,
        max_tip_length_to_length_ratio=0.25,
    )
    pl = Text(
        "push" if push_scale < 1.0 else "big push",
        font_size=20,
        font="Arial",
        color=GREEN_C,
    )
    pl.next_to(pa, LEFT, buff=0.12)

    wpts = (
        np.array([[2.2, 0.5, 0], [1.7, 0.3, 0], [1.2, 0, 0], [0.9, -0.4, 0]]) + CENTER
    )
    w = VMobject()
    w.set_points_smoothly(wpts)
    w.set_stroke(GREY_A, width=2)
    wl = Text("wind", font_size=18, font="Arial", color=GREY_A)
    wl.next_to(w, RIGHT, buff=0.1)

    grp = VGroup(swing, pa, pl, w, wl)
    if include_coin:
        cp = (
            CENTER + np.array([0.05, SEAT_Y, 0])
            if coin_on_seat
            else CENTER + np.array([0.3, SEAT_Y - 0.8, 0])
        )
        c = Circle(radius=COIN_R)
        c.set_fill(GOLD_E, opacity=0.95).set_stroke(YELLOW, width=1.5)
        c.move_to(cp)
        cl = Text("coin = qubit", font_size=16, font="Arial", color=YELLOW)
        cl.next_to(c, DOWN, buff=0.12)
        grp.add(c, cl)
    return grp


# ═══════════════════════════════════════════
#  Helper graphics
# ═══════════════════════════════════════════


def _icon_row():
    labels = ["Drug discovery", "Cryptography", "New materials", "Optimization"]
    colors = [GREEN_C, BLUE_C, TEAL_C, YELLOW]
    out = []
    for i, (lb, co) in enumerate(zip(labels, colors)):
        s = Circle(radius=0.3) if i != 1 else Rectangle(width=0.5, height=0.4)
        s.set_fill(co, opacity=0.25).set_stroke(co, width=2)
        s.move_to(np.array([-3.5 + 2.3 * i, 0.2, 0]))
        t = Text(lb, font_size=17, font="Arial", color=co)
        t.next_to(s, DOWN, buff=0.15)
        out.append(VGroup(s, t))
    return out


def _qubit_coin(pos=CENTER, glow=True):
    c = Circle(radius=0.35)
    c.set_fill(GOLD_E, opacity=0.9).set_stroke(YELLOW, width=2).move_to(pos)
    if glow:
        h = Circle(radius=0.5)
        h.set_fill(YELLOW, opacity=0.12).set_stroke(width=0).move_to(pos)
        return VGroup(h, c)
    return VGroup(c)


def _active_panel(ctr):
    t = Text("Active", font_size=22, font="Arial", color=BLUE_C)
    t.move_to(ctr + UP * 1.1)
    d = VGroup(
        *[
            Dot(
                ctr + np.array([-0.6 + 0.3 * (i % 5), 0.5 - 0.3 * (i // 5), 0]),
                color=BLUE_C,
                radius=0.09,
            )
            for i in range(15)
        ]
    )
    a = Text("measure & fix", font_size=16, font="Arial", color=GREY_A)
    a.next_to(d, DOWN, buff=0.15)
    ch = Text("Protected ✓  Scalable ✗", font_size=15, font="Arial", color=RED_C)
    ch.next_to(a, DOWN, buff=0.12)
    return VGroup(t, d, a, ch)


def _passive_panel(ctr):
    t = Text("Passive (static)", font_size=22, font="Arial", color=GREEN_C)
    t.move_to(ctr + UP * 1.1)
    b = Rectangle(width=0.7, height=0.5)
    b.set_fill(GREY_D, opacity=0.5).set_stroke(GREY_A, width=2).move_to(ctr + UP * 0.3)
    c = Circle(radius=0.12)
    c.set_fill(GOLD_E, opacity=0.9).set_stroke(YELLOW, width=1.5).move_to(
        b.get_center()
    )
    lk = Text("frozen", font_size=15, font="Arial", color=RED_C)
    lk.next_to(b, DOWN, buff=0.1)
    ch = Text("Protected ✓  Can compute ✗", font_size=15, font="Arial", color=RED_C)
    ch.next_to(lk, DOWN, buff=0.12)
    return VGroup(t, b, c, lk, ch)


def _spinning_top(ctr):
    body = Dot(ctr, radius=0.25, color=TEAL_C)
    tip = Line(ctr, ctr + DOWN * 0.4, color=GREY_A, stroke_width=3)
    ring = Circle(radius=0.3)
    ring.set_stroke(TEAL_C, width=2, opacity=0.5).move_to(ctr)
    lbl = Text("spinning top", font_size=16, font="Arial", color=TEAL_C)
    lbl.next_to(body, UP, buff=0.2)
    return VGroup(body, tip, ring, lbl)


def _bowl_and_ball(ctr):
    pts = [ctr + np.array([x, 0.4 * x * x - 0.35, 0]) for x in np.linspace(-1, 1, 30)]
    bowl = VMobject()
    bowl.set_points_smoothly(np.array(pts))
    bowl.set_stroke(GREY_A, width=3)
    ball = Dot(ctr + DOWN * 0.35, radius=0.12, color=GOLD_E)
    lbl = Text("ball in a bowl", font_size=16, font="Arial", color=GREY_A)
    lbl.next_to(bowl, DOWN, buff=0.15)
    return VGroup(bowl, ball, lbl)


def _two_swings_rope(ctr):
    bar1 = Line(
        ctr + np.array([-1.4, 0.7, 0]),
        ctr + np.array([-0.8, 0.7, 0]),
        color=GREY_B,
        stroke_width=4,
    )
    seat1 = Rectangle(width=0.35, height=0.12)
    seat1.set_fill(GREY_C, opacity=0.8).set_stroke(GREY_A, width=1)
    seat1.move_to(ctr + np.array([-1.1, 0, 0]))
    bar2 = Line(
        ctr + np.array([0.8, 0.7, 0]),
        ctr + np.array([1.4, 0.7, 0]),
        color=GREY_B,
        stroke_width=4,
    )
    seat2 = Rectangle(width=0.35, height=0.12)
    seat2.set_fill(GREY_C, opacity=0.8).set_stroke(GREY_A, width=1)
    seat2.move_to(ctr + np.array([1.1, 0, 0]))
    rope = Line(seat1.get_right(), seat2.get_left(), color=YELLOW, stroke_width=2)
    rl = Text("rope (coupling)", font_size=15, font="Arial", color=YELLOW)
    rl.next_to(rope, DOWN, buff=0.1)
    l1 = Text("Swing A", font_size=14, font="Arial", color=TEAL_C)
    l1.next_to(seat1, DOWN, buff=0.15)
    l2 = Text("Swing B", font_size=14, font="Arial", color=MAROON_A)
    l2.next_to(seat2, DOWN, buff=0.15)
    return VGroup(bar1, seat1, bar2, seat2, rope, rl, l1, l2)


def _bhd_schematic(ctr=CENTER):
    b = Circle(radius=0.45)
    b.set_fill(TEAL_C, opacity=0.25).set_stroke(TEAL_C, width=2)
    b.move_to(ctr + LEFT * 0.8 + UP * 0.15)
    a = Circle(radius=0.35)
    a.set_fill(MAROON_A, opacity=0.2).set_stroke(MAROON_A, width=2)
    a.move_to(ctr + RIGHT * 0.8 + UP * 0.15)
    dr = Arrow(b.get_top() + UP * 0.35, b.get_top(), color=GREEN_C, thickness=0.04)
    dn = Arrow(
        b.get_bottom(), b.get_bottom() + DOWN * 0.35, color=RED_C, thickness=0.04
    )
    lk = Line(b.get_right(), a.get_left(), color=YELLOW, stroke_width=3)
    bl = Text("B (bonding)\ndrive + drain", font_size=14, font="Arial", color=TEAL_C)
    bl.next_to(b, DOWN, buff=0.18)
    al = Text("A (antibonding)\ncoupled", font_size=14, font="Arial", color=MAROON_A)
    al.next_to(a, DOWN, buff=0.18)
    tt = Text("Bose–Hubbard dimer", font_size=20, font="Arial", color=YELLOW)
    tt.move_to(ctr + UP * 1.15)
    return VGroup(b, a, dr, dn, lk, bl, al, tt)


def _term_table(ctr=CENTER):
    rows = [
        ("Swing", "Bonding mode (B)"),
        ("Coin", "Qubit / noiseless subsystem"),
        ("Push", "Drive F̃"),
        ("Wind", "Dissipation (Lindblad)"),
        ("Strong enough", "F̃ > 0.93 — phase transition"),
        ("Never stops", "Dissipative time crystal"),
        ("Two parts + rope", "Bonding + antibonding coupled"),
        ("Ball returns to bowl", "Robust to dephasing"),
        ("Real system", "Bose–Hubbard dimer"),
    ]
    g = VGroup()
    for i, (l, r) in enumerate(rows):
        lt = Text(l, font_size=15, font="Arial", color=WHITE)
        rt = Text(r, font_size=15, font="Arial", color=TEAL_C)
        lt.move_to(ctr + np.array([-2.2, 1.1 - 0.32 * i, 0]))
        rt.move_to(ctr + np.array([0.8, 1.1 - 0.32 * i, 0]))
        g.add(lt, rt)
    h = Text("Story  →  Paper", font_size=22, font="Arial", color=YELLOW)
    h.move_to(ctr + UP * 1.7)
    g.add(h)
    return g


# ═══════════════════════════════════════════
#  Utility: write text, wait, clear
# ═══════════════════════════════════════════


def _txt(s, sz=20, col=WHITE):
    return Text(s, font_size=sz, font="Arial", color=col)


# ═══════════════════════════════════════════
#  SCENE
# ═══════════════════════════════════════════


class QuantumPaperExplainer(Scene):
    def construct(self):
        self._act_i()
        self._act_ii()
        self._act_iii()
        self._act_iv()

    # helper: show text at bottom, wait, fade
    def _bottom(self, t, wait=2.0, buff=0.4, rt=1.5):
        t.to_edge(DOWN, buff=buff)
        self.play(Write(t), run_time=rt)
        self.wait(wait)
        self.play(FadeOut(t), run_time=0.3)

    # ── ACT I ──────────────────────────────

    def _act_i(self):
        # S1 title
        t1 = _txt("The swing that keeps a secret", 36)
        t1s = _txt("Why one physics paper could change quantum computing", 20, GREY_A)
        t1s.next_to(t1, DOWN, buff=0.4)
        self.play(Write(t1), Write(t1s), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(t1), FadeOut(t1s), run_time=0.5)

        # S2 promise
        h2 = _txt(
            "Quantum computers promise to solve problems\nclassical computers never will",
            22,
        )
        h2.to_edge(UP, buff=0.35)
        self.play(Write(h2), run_time=1.2)
        icons = _icon_row()
        for ic in icons:
            self.play(FadeIn(ic), run_time=0.5)
        self.wait(1.5)
        c2 = _txt("...if we can build them.", 22, YELLOW)
        c2.to_edge(DOWN, buff=0.5)
        self.play(Write(c2), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(h2), FadeOut(VGroup(*icons)), FadeOut(c2), run_time=0.5)

        # S3 qubit
        h3 = _txt("The magic ingredient: the qubit", 26, YELLOW)
        h3.to_edge(UP, buff=0.35)
        self.play(Write(h3), run_time=0.8)
        coin = _qubit_coin(UP * 0.2, glow=True)
        self.play(FadeIn(coin), run_time=0.8)
        self._bottom(
            _txt(
                "Normal bit: 0 or 1.  Qubit: both at once = superposition.\n"
                "Like a spinning coin — while it spins, it's neither heads nor tails.",
                19,
            ),
            2.5,
        )

        # S4 decoherence — WHY
        wpts = np.array([[3, 1, 0], [2.2, 0.6, 0], [1.4, 0.2, 0], [0.9, -0.2, 0]])
        wl = VMobject()
        wl.set_points_smoothly(wpts)
        wl.set_stroke(GREY_A, width=3)
        wlbl = _txt("environment\n(heat, noise)", 16, GREY_A)
        wlbl.next_to(wl, RIGHT, buff=0.1)
        self.play(ShowCreation(wl), Write(wlbl), run_time=1)
        self.play(coin[0].animate.set_fill(opacity=0), run_time=0.8)

        e4 = _txt("Decoherence: the environment destroys the superposition.", 20, RED_C)
        e4.to_edge(DOWN, buff=0.55)
        self.play(Write(e4), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(e4), run_time=0.3)

        # WHY it happens — parallel metaphor
        why4 = _txt(
            "Why? Like whispering a secret in a crowded room —\n"
            "every air molecule carries a bit of the secret away.\n"
            "Any interaction (photon, vibration) leaks quantum info.",
            17,
        )
        why4.to_edge(DOWN, buff=0.35)
        self.play(Write(why4), run_time=2)
        self.wait(3)
        self.play(
            FadeOut(h3),
            FadeOut(coin),
            FadeOut(wl),
            FadeOut(wlbl),
            FadeOut(why4),
            run_time=0.5,
        )

        # S5 stakes
        s5 = VGroup(
            _txt("Without protection, qubits lose their state in microseconds.", 21),
            _txt(
                "No protection → no reliable computation → no quantum advantage.",
                21,
                YELLOW,
            ),
        )
        s5.arrange(DOWN, buff=0.3)
        self.play(Write(s5[0]), run_time=1.2)
        self.play(Write(s5[1]), run_time=1.2)
        self.wait(2)
        self.play(FadeOut(s5), run_time=0.4)

    # ── ACT II ─────────────────────────────

    def _act_ii(self):
        # S6 active
        h6 = _txt("Solution A: Active error correction", 24, BLUE_C)
        h6.to_edge(UP, buff=0.35)
        self.play(Write(h6), run_time=0.8)
        ap = _active_panel(UP * 0.1)
        self.play(FadeIn(ap), run_time=1)
        self._bottom(
            _txt(
                "Like hiring 1,000 people to watch one coin and stand it back up.\n"
                "Works, but ~1,000 physical qubits per protected qubit.",
                17,
                GREY_A,
            ),
            2.5,
        )
        self.play(FadeOut(h6), FadeOut(ap), run_time=0.4)

        # S7 passive static
        h7 = _txt("Solution B: Passive protection (but static)", 24, GREEN_C)
        h7.to_edge(UP, buff=0.35)
        self.play(Write(h7), run_time=0.8)
        pp = _passive_panel(UP * 0.1)
        self.play(FadeIn(pp), run_time=1)
        self._bottom(
            _txt(
                "Like putting the coin in a safe: protected, but you can't use it.\n"
                "You can store information, but you can't compute.",
                17,
                GREY_A,
            ),
            2.5,
        )
        self.play(FadeOut(h7), FadeOut(pp), run_time=0.4)

        # S8 bottleneck
        h8 = _txt("The real bottleneck", 26, YELLOW)
        h8.to_edge(UP, buff=0.35)
        self.play(Write(h8), run_time=0.8)
        lp = _active_panel(LEFT * 2.6)
        rp = _passive_panel(RIGHT * 2.6)
        self.play(FadeIn(lp), FadeIn(rp), run_time=1)
        q8 = _txt("Can we protect a qubit AND keep it moving?", 22)
        q8.to_edge(DOWN, buff=0.6)
        a8 = _txt("This is what the paper solves.", 20, YELLOW)
        a8.next_to(q8, DOWN, buff=0.15)
        self.play(Write(q8), run_time=1.2)
        self.play(Write(a8), run_time=1)
        self.wait(2)
        self.play(
            FadeOut(h8),
            FadeOut(lp),
            FadeOut(rp),
            FadeOut(q8),
            FadeOut(a8),
            run_time=0.5,
        )

        # S9 consequences
        h9 = _txt("If this isn't solved…", 26, RED_C)
        h9.to_edge(UP, buff=0.35)
        self.play(Write(h9), run_time=0.8)
        buls = [
            "Active → need millions of physical qubits. Way beyond current tech.",
            "Passive stays limited to memory → can't do quantum gates.",
            "Quantum computers remain too fragile for real use.",
            "Drug discovery, cryptography, materials, optimization — out of reach.",
        ]
        bg = VGroup()
        for i, tx in enumerate(buls):
            t = _txt(tx, 18)
            t.move_to(UP * (0.3 - 0.42 * i))
            bg.add(t)
        for b in bg:
            self.play(Write(b), run_time=0.9)
        self.wait(2)
        self.play(FadeOut(h9), FadeOut(bg), run_time=0.4)

    # ── ACT III ────────────────────────────

    def _act_iii(self):
        # S10 introduce swing + explain push/wind
        h10 = _txt("This paper's idea — in one picture", 24, YELLOW)
        h10.to_edge(UP, buff=0.3)
        self.play(Write(h10), run_time=0.8)
        world = _swing_world(include_coin=True, push_scale=1.0, coin_on_seat=True)
        self.play(FadeIn(world), run_time=1.2)
        self._bottom(
            _txt(
                "Swing = the system.  Push = drive (energy in).  Wind = dissipation (energy out).\n"
                "Coin = the qubit we want to protect.",
                17,
            ),
            2.5,
        )

        # WHY push and wind exist
        self._bottom(
            _txt(
                "Why 'wind'? Nothing is perfectly isolated. The qubit sits in a real device.\n"
                "Heat, photons, vibrations constantly steal energy. That IS the wind.",
                17,
                GREY_A,
            ),
            3,
        )
        self._bottom(
            _txt(
                "Why 'push'? We deliberately pump energy in (lasers, microwaves).\n"
                "Without the push, the wind drains everything and the system goes silent.",
                17,
                GREY_A,
            ),
            3,
        )
        self.play(FadeOut(h10), run_time=0.3)

        # S11 weak push
        self.play(FadeOut(world), run_time=0.3)
        weak = _swing_world(include_coin=True, push_scale=0.45, coin_on_seat=True)
        h11 = _txt("Weak push (F̃ < 0.93)", 22, RED_C)
        h11.to_edge(UP, buff=0.35)
        self.play(Write(h11), FadeIn(weak), run_time=0.8)
        fp = CENTER + np.array([0.3, SEAT_Y - 0.8, 0])
        self.play(
            weak[5].animate.move_to(fp),
            weak[6].animate.next_to(fp, DOWN, buff=0.12),
            run_time=1,
        )
        self._bottom(
            _txt("Wind wins → coin falls off. No protected qubit.", 21, RED_C), 2
        )
        self.play(FadeOut(h11), FadeOut(weak), run_time=0.4)

        # S12 strong push + WHY strong helps + phase transition + NS explained
        strong = _swing_world(include_coin=True, push_scale=1.5, coin_on_seat=True)
        h12 = _txt("Strong push (F̃ > 0.93)", 22, GREEN_C)
        h12.to_edge(UP, buff=0.35)
        self.play(Write(h12), FadeIn(strong), run_time=0.8)

        sg = strong[0]
        piv = sg[0].get_center() + DOWN * 0.05
        rs = VGroup(sg[1], sg[2], sg[3])
        c12 = strong[5]
        cl12 = strong[6]
        for ang in [0.35, -0.35, 0.3, -0.3]:
            self.play(
                Rotate(rs, ang, about_point=piv),
                Rotate(c12, ang, about_point=piv),
                Rotate(cl12, ang, about_point=piv),
                run_time=0.35,
            )

        self._bottom(
            _txt(
                "The swing's motion keeps the coin on — nobody holds it.\n"
                "That's passive protection.",
                19,
                GREEN_C,
            ),
            2,
        )

        # WHY strong push helps — spinning top
        self.play(FadeOut(h12), run_time=0.2)
        h12b = _txt("Why does a stronger push help?", 22, TEAL_C)
        h12b.to_edge(UP, buff=0.35)
        self.play(Write(h12b), run_time=0.8)
        top = _spinning_top(RIGHT * 3.5 + UP * 0.3)
        self.play(FadeIn(top), run_time=0.8)
        self._bottom(
            _txt(
                "Think of a spinning top. Spin weakly → wobbles and falls.\n"
                "Spin hard → stable. Tap the table, it barely notices.\n"
                "Strong push = strong stable oscillation that resists disturbances.",
                16,
                TEAL_C,
            ),
            3.5,
        )
        self.play(FadeOut(top), FadeOut(h12b), run_time=0.3)

        # Phase transition explained
        h12c = _txt("What is a 'phase transition'?", 22)
        h12c.to_edge(UP, buff=0.35)
        self.play(Write(h12c), run_time=0.8)
        self._bottom(
            _txt(
                "A sudden change at a threshold. Like water → ice at 0°C.\n"
                "Here: below F̃ = 0.93 = no protected qubit. Above = protected qubit.\n"
                "Not gradual — it's a switch.",
                17,
            ),
            3,
        )

        # Noiseless subsystem explained
        self.play(FadeOut(h12c), run_time=0.2)
        h12d = _txt("What is a 'noiseless subsystem'?", 22, YELLOW)
        h12d.to_edge(UP, buff=0.35)
        self.play(Write(h12d), run_time=0.8)
        self._bottom(
            _txt(
                "A pocket inside the system where the noise can't reach.\n"
                "Not a physical space — a math property: certain state combinations\n"
                "are invisible to the environment. The qubit lives there.",
                16,
                YELLOW,
            ),
            3.5,
        )
        self.play(FadeOut(h12d), run_time=0.3)

        # S13 what "coupled" means — dedicated scene
        h13 = _txt("What does 'coupled' mean?", 24)
        h13.to_edge(UP, buff=0.35)
        self.play(Write(h13), run_time=0.8)
        two_sw = _two_swings_rope(CENTER + UP * 0.3)
        self.play(FadeIn(two_sw), run_time=1)
        self._bottom(
            _txt(
                "Coupled = connected so that what happens to one affects the other.\n"
                "Two swings connected by a rope: when one moves, the rope tugs the other.",
                17,
            ),
            3,
        )

        self._bottom(
            _txt(
                "In the paper: two 'modes' (vibrations) connected by a nonlinear interaction.\n"
                "Bonding (big, driven, dissipated) + antibonding (small, quantum).\n"
                "When the bonding mode is strong, its stability transfers to the antibonding mode.",
                16,
                GREY_A,
            ),
            3.5,
        )
        self.play(FadeOut(h13), FadeOut(two_sw), run_time=0.4)

        # S14 how the protection works — step by step
        h14 = _txt("How the protection actually works — step by step", 22, YELLOW)
        h14.to_edge(UP, buff=0.35)
        self.play(Write(h14), run_time=0.8)

        steps = [
            (
                "Step 1: The swing locks into a strong, stable rhythm.",
                "The push is strong enough → bonding mode reaches a large stable orbit.",
            ),
            (
                "Step 2: The coin rides along (they're coupled).",
                "The antibonding mode's dynamics are tied to the bonding mode through coupling.",
            ),
            (
                "Step 3: The wind hits the swing, not the coin directly.",
                "The dissipator (L = a_B) only acts on bonding. The coin is sheltered behind it.",
            ),
            (
                "Step 4: A symmetry creates the protected pocket.",
                "Strong parity symmetry → even/odd sectors evolve independently → noiseless subsystem.",
            ),
        ]
        for label, detail in steps:
            s_grp = VGroup(
                _txt(label, 18, GREEN_C),
                _txt(detail, 16, GREY_A),
            )
            s_grp.arrange(DOWN, buff=0.1)
            s_grp.to_edge(DOWN, buff=0.35)
            self.play(Write(s_grp[0]), run_time=1)
            self.play(Write(s_grp[1]), run_time=1)
            self.wait(2)
            self.play(FadeOut(s_grp), run_time=0.3)

        self.play(FadeOut(h14), run_time=0.3)

        # S15 time crystal — oscillating qubit
        h15 = _txt("The qubit oscillates — that's the breakthrough", 22, TEAL_C)
        h15.to_edge(UP, buff=0.35)
        self.play(Write(h15), run_time=0.8)
        for ang in [0.3, -0.3, 0.25, -0.25]:
            self.play(
                Rotate(rs, ang, about_point=piv),
                Rotate(c12, ang, about_point=piv),
                Rotate(cl12, ang, about_point=piv),
                run_time=0.3,
            )

        self._bottom(
            _txt(
                "The swing never stops = dissipative time crystal.\n"
                "The qubit is DYNAMIC — not frozen like previous passive schemes.",
                18,
                TEAL_C,
            ),
            2.5,
        )

        self._bottom(
            _txt(
                "Why does oscillating matter? If the qubit is frozen, you'd have to\n"
                "'wake it up' to compute — which might break the protection.\n"
                "Here, the qubit is already moving in a predictable rhythm.\n"
                "That rhythm itself can be used for quantum gates.",
                16,
            ),
            3.5,
        )
        self.play(FadeOut(h15), run_time=0.3)

        # S16 why the coin comes back — expanded with bowl metaphor
        h16 = _txt("Why does the coin come back after a kick?", 22, GREEN_C)
        h16.to_edge(UP, buff=0.35)
        self.play(Write(h16), run_time=0.8)

        self.play(c12.animate.shift(RIGHT * 0.3 + UP * 0.15), run_time=0.4)
        self.wait(0.3)
        self.play(
            c12.animate.move_to(CENTER + np.array([0.05, SEAT_Y, 0])), run_time=0.7
        )

        bowl = _bowl_and_ball(RIGHT * 3.2 + DOWN * 0.2)
        self.play(FadeIn(bowl), run_time=0.8)

        self._bottom(
            _txt(
                "Think of a ball in a bowl. Push it — it rolls up the wall.\n"
                "But gravity pulls it back to the bottom. The bottom = stable point.",
                17,
            ),
            2.5,
        )

        self._bottom(
            _txt(
                "Same here: the strong push created a deep 'bowl' (stable orbit).\n"
                "If something kicks the coin, dissipation (the SAME wind that causes\n"
                "decoherence!) now acts like gravity: it pulls the system back.\n"
                "And coupling means the swing drags the coin back too.",
                16,
                GREY_A,
            ),
            4,
        )

        self._bottom(
            _txt(
                "So ironically: the environment (which normally destroys qubits)\n"
                "also helps with recovery — it damps out disturbances.",
                17,
                YELLOW,
            ),
            3,
        )

        self.play(FadeOut(bowl), FadeOut(h16), run_time=0.4)

        # S17 real system — BHD
        self.play(FadeOut(strong), run_time=0.3)
        h17 = _txt("The real system: Bose–Hubbard dimer (BHD)", 22)
        h17.to_edge(UP, buff=0.35)
        self.play(Write(h17), run_time=0.8)
        bhd = _bhd_schematic(UP * 0.1)
        self.play(FadeIn(bhd), run_time=1)
        self._bottom(
            _txt(
                "Two coupled bosonic modes. B: driven + dissipated. A: coupled.\n"
                "Phase transition at F̃ ≈ 0.93. Can be built in Kerr resonators\n"
                "or cat-qubit architectures (superconducting circuits).",
                16,
                GREY_A,
            ),
            3,
        )
        self.play(FadeOut(h17), FadeOut(bhd), run_time=0.4)

    # ── ACT IV ─────────────────────────────

    def _act_iv(self):
        # S18 terminology recap
        tbl = _term_table()
        self.play(FadeIn(tbl), run_time=1.2)
        self.wait(4)
        self.play(FadeOut(tbl), run_time=0.5)

        # S19 specific applications
        h19 = _txt("What is this specifically useful for?", 24, YELLOW)
        h19.to_edge(UP, buff=0.35)
        self.play(Write(h19), run_time=0.8)

        apps = [
            (
                "Phase gates (single-qubit operations)",
                "Qubit oscillates at known frequency → wait precise time = phase rotation.\n"
                "No manipulation needed during the gate — the rhythm does it.",
            ),
            (
                "Reducing overhead for fault-tolerant computing",
                "If passive dynamic protection works, you could replace ~1,000 physical\n"
                "qubits with one oscillating system. Dramatically smaller & cheaper.",
            ),
            (
                "Experimental platforms that exist today",
                "Driven Kerr resonators (microwave cavities), cat-qubit setups\n"
                "(e.g. Alice & Bob), superconducting circuits, spin ensembles.",
            ),
        ]
        for title, detail in apps:
            ag = VGroup(
                _txt(title, 19, GREEN_C),
                _txt(detail, 15, WHITE),
            )
            ag.arrange(DOWN, buff=0.12)
            ag.move_to(DOWN * 0.2)
            self.play(Write(ag[0]), run_time=0.8)
            self.play(Write(ag[1]), run_time=1.2)
            self.wait(2)
            self.play(FadeOut(ag), run_time=0.3)

        self.play(FadeOut(h19), run_time=0.3)

        # S20 specific limitations
        h20 = _txt("What are the specific limitations?", 24, RED_C)
        h20.to_edge(UP, buff=0.35)
        self.play(Write(h20), run_time=0.8)

        lims = [
            (
                "Only global (symmetric) noise",
                "Both modes must share the SAME noise bath (same cavity).\n"
                "If they're in separate cavities with separate noise → protection fails.\n"
                "Limits how you can wire multiple qubits together.",
            ),
            (
                "Needs large system size (thermodynamic limit)",
                "At N=4 (tiny): noticeable errors. At N=20: much better, not perfect.\n"
                "How big N must be for a practical device? Unknown.\n"
                "Paper simulations go to N=20; real devices might need N=100+.",
            ),
            (
                "Full gate set not yet designed",
                "Paper shows protection + suggests phase gates. But has NOT proven:\n"
                "universal gate set, fault tolerance, or two-qubit gates.\n"
                "Without two-qubit gates → no entanglement → no quantum computer.",
            ),
            (
                "Theoretical — not yet built",
                "All results from numerical simulations (solving Lindblad equation).\n"
                "Nobody has built this in a lab. But platforms exist to test it.",
            ),
        ]
        for title, detail in lims:
            lg = VGroup(
                _txt(title, 18, RED_C),
                _txt(detail, 14, GREY_A),
            )
            lg.arrange(DOWN, buff=0.1)
            lg.move_to(DOWN * 0.1)
            self.play(Write(lg[0]), run_time=0.8)
            self.play(Write(lg[1]), run_time=1.2)
            self.wait(2.5)
            self.play(FadeOut(lg), run_time=0.3)

        self.play(FadeOut(h20), run_time=0.3)

        # S21 summary
        h21 = _txt("Summary", 28, YELLOW)
        h21.to_edge(UP, buff=0.35)
        lines = [
            "Quantum computers need protected qubits. Decoherence destroys them.",
            "Active correction works but costs ~1,000 qubits per qubit.",
            "Passive protection existed, but only for frozen (static) memory.",
            "This paper: a dissipative time crystal that protects AND oscillates.",
            "Above F̃ ≈ 0.93, a noiseless subsystem in the BHD — passive, dynamic, robust.",
        ]
        sg = VGroup()
        for i, tx in enumerate(lines):
            c = WHITE if i < 3 else YELLOW
            t = _txt(tx, 17, c)
            t.move_to(UP * (0.4 - 0.35 * i))
            sg.add(t)
        self.play(Write(h21), run_time=0.6)
        for s in sg:
            self.play(Write(s), run_time=0.9)
        self.wait(3.5)
        self.play(FadeOut(h21), FadeOut(sg), run_time=0.5)

        # S22 end card
        e1 = _txt("The swing that keeps a secret.", 30)
        e2 = _txt(
            "Dissipative Time Crystals as Passively Protected Oscillating Qubits",
            18,
            GREY_A,
        )
        e3 = _txt(
            "Esencan, Lvovsky & Buča — Oxford · Paris-Saclay · Copenhagen", 16, GREY_B
        )
        e2.next_to(e1, DOWN, buff=0.35)
        e3.next_to(e2, DOWN, buff=0.25)
        self.play(Write(e1), Write(e2), Write(e3), run_time=1.8)
        self.wait(3)
