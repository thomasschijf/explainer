"""
Aircraft lift explainer — follows docs/how-lift-works-explainer.md step by step.
- Text: colored and styled (key terms highlighted), all captions outside the figure.
- Streamlines: horizontal parallel approach, curve over/under wing, color bands (free stream / high-velocity / low-velocity).
Run with: manimgl lift_explainer_scene.py LiftExplainer -w
"""

from manimlib import *
import numpy as np

# Scale for wing and diagram
CHORD = 2.2
THICKNESS_SCALE = 0.5
# Diagram sits in upper part; text panel below (no text in figure)
DIAGRAM_CENTER_Y = 0.6
TEXT_PANEL_TOP = -1.0


def naca_upper_lower(t):
    """NACA 00xx-style thickness distribution (symmetric). t in [0,1] along chord."""
    coeffs = (0.2969, -0.1260, -0.3516, 0.2843, -0.1015)
    y_t = (
        coeffs[0] * np.sqrt(t)
        + coeffs[1] * t
        + coeffs[2] * t**2
        + coeffs[3] * t**3
        + coeffs[4] * t**4
    )
    return y_t


def airfoil_vertices(n_points=24):
    """Closed polygon vertices for a NACA-style airfoil. Chord from -1 to 1."""
    t = np.linspace(1e-6, 1.0, n_points // 2)
    x = 2 * t - 1
    y_top = THICKNESS_SCALE * naca_upper_lower(t)
    y_bot = -THICKNESS_SCALE * naca_upper_lower(t)
    top_pts = np.column_stack([x, y_top, np.zeros_like(x)])
    bot_pts = np.column_stack([x[::-1], y_bot[::-1], np.zeros_like(x)])
    vertices = np.vstack([top_pts, bot_pts])
    return vertices


def make_wing_polygon():
    """Wing as an explicit closed geometric shape (Polygon)."""
    verts = airfoil_vertices()
    verts = verts * CHORD * 0.5
    points = [tuple(v) for v in verts]
    wing = Polygon(*points)
    wing.set_fill(GREY_B, opacity=0.95)
    wing.set_stroke(GREY_A, width=2)
    return wing


def make_streamline(points_xy, color=BLUE, stroke_width=1.2):
    """One streamline as a smooth curve through points_xy (Nx2)."""
    pts = np.column_stack([np.array(points_xy), np.zeros(len(points_xy))])
    line = VMobject()
    line.set_points_smoothly(pts)
    line.set_stroke(color=color, width=stroke_width)
    line.set_fill(opacity=0)
    return line


def streamlines_reference_style(
    wing_center_x, wing_center_y, chord_half, n_above=6, n_below=6
):
    """
    Streamlines like the reference: horizontal and parallel on left, curve over/under
    the wing, horizontal again on right. Color bands: free stream (red), high-velocity
    above (green), low-velocity below (blue).
    """
    x_left = wing_center_x - chord_half - 1.4
    x_right = wing_center_x + chord_half + 1.4
    lines = []
    # Above wing: start horizontal, dip over wing (longer path), exit horizontal
    y_above = np.linspace(wing_center_y + 0.35, wing_center_y + 1.1, n_above)
    for y0 in y_above:
        points = [
            (x_left, y0),
            (wing_center_x - 0.9, y0),
            (wing_center_x - 0.3, wing_center_y + 0.28),
            (wing_center_x, wing_center_y + 0.25),
            (wing_center_x + 0.3, wing_center_y + 0.28),
            (wing_center_x + 0.9, y0),
            (x_right, y0),
        ]
        lines.append(make_streamline(points, color=GREEN_C, stroke_width=1.1))
    # Below wing: start horizontal, bulge under wing (shorter path), exit horizontal
    y_below = np.linspace(wing_center_y - 0.35, wing_center_y - 1.0, n_below)
    for y0 in y_below:
        points = [
            (x_left, y0),
            (wing_center_x - 0.9, y0),
            (wing_center_x - 0.3, wing_center_y - 0.22),
            (wing_center_x, wing_center_y - 0.18),
            (wing_center_x + 0.3, wing_center_y - 0.22),
            (wing_center_x + 0.9, y0),
            (x_right, y0),
        ]
        lines.append(make_streamline(points, color=BLUE_C, stroke_width=1.1))
    # Free stream: a few horizontal lines far from wing (red/orange)
    y_free = [wing_center_y + 1.35, wing_center_y - 1.25]
    for y0 in y_free:
        points = [
            (x_left, y0),
            (wing_center_x - 1.3, y0),
            (wing_center_x + 1.3, y0),
            (x_right, y0),
        ]
        lines.append(make_streamline(points, color=RED_E, stroke_width=1.0))
    return lines


def label_with_arrow(
    scene, label_text, point_in_diagram, direction_from_label, color, font_size=20
):
    """Place label outside figure and add arrow pointing to a point in the diagram."""
    label = Text(
        label_text,
        font_size=font_size,
        font="Arial",
        color=color,
    )
    label.move_to(direction_from_label)
    arrow_end = point_in_diagram
    arrow_start = label.get_center() + 0.4 * normalize(arrow_end - label.get_center())
    arr = Arrow(
        arrow_start,
        arrow_end,
        thickness=2,
        color=color,
        buff=0.08,
    )
    return label, arr


def bullet_text_styled(lines_with_style, font_size=20, font="Arial"):
    """
    lines_with_style: list of (text_str, color_or_none, bold_or_false).
    color_or_none: color for the whole line, or None for default. Optional t2c dict for that line.
    """
    group = VGroup()
    for item in lines_with_style:
        if isinstance(item, tuple):
            if len(item) == 2:
                line_text, color = item[0], item[1]
                t2c = {}
                t2w = {}
            else:
                line_text, color, t2c = (
                    item[0],
                    item[1],
                    item[2] if len(item) > 2 else {},
                )
                t2w = item[3] if len(item) > 3 else {}
        else:
            line_text, color, t2c, t2w = item, None, {}, {}
        t = Text(
            line_text,
            font_size=font_size,
            font=font,
            color=color if color else WHITE,
            t2c=t2c,
            t2w=t2w,
        )
        if len(group) == 0:
            group.add(t)
        else:
            t.next_to(group[-1], DOWN, buff=0.12, aligned_edge=LEFT)
            group.add(t)
    return group


def text_panel_position():
    """Position for the text panel (below diagram, outside figure)."""
    return np.array([0, TEXT_PANEL_TOP, 0])


class LiftExplainer(Scene):
    def construct(self):
        # Title at top, always outside diagram
        title = Text(
            "How does a wing generate lift?",
            font_size=32,
            font="Arial",
            color=WHITE,
            t2c={"lift": GREEN_C},
        )
        title.to_edge(UP, buff=0.28)
        self.add(title)
        self.wait(0.5)

        # -------------------------------------------------------------------------
        # STEP 1: Big picture
        # -------------------------------------------------------------------------
        step1 = bullet_text_styled(
            [
                ("Lift = upward force from the air on the wings.", GREEN_C),
                (
                    "Lift > Weight => plane climbs.  Lift = Weight => level flight.",
                    None,
                    {"Lift": GREEN_C, "Weight": RED_C},
                ),
            ],
            font_size=21,
        )
        step1.move_to(text_panel_position())
        self.play(Write(step1), run_time=1.2)
        self.wait(1.2)
        self.play(FadeOut(step1), run_time=0.35)

        # -------------------------------------------------------------------------
        # STEP 2: Wing shape — show wing first, text in panel only
        # -------------------------------------------------------------------------
        angle_of_attack = 10 * DEG
        wing = make_wing_polygon()
        wing.move_to(np.array([0, DIAGRAM_CENTER_Y, 0]))
        wing.rotate(angle_of_attack, about_point=wing.get_center())
        wing_center = wing.get_center()
        chord_left = wing_center[0] - CHORD * 0.5
        chord_right = wing_center[0] + CHORD * 0.5
        wing_center_y = wing_center[1]

        step2_title = Text(
            "The wing is a special shape: the airfoil",
            font_size=24,
            font="Arial",
            color=YELLOW,
            t2w={"airfoil": "bold"},
        )
        step2 = bullet_text_styled(
            [
                ("Curved on top, flatter on the bottom.", GREY_A),
                ("Rounded front (leading edge), thinner back (trailing edge).", GREY_A),
                ("Air has to flow around this shape.", None, {"Air": TEAL_C}),
            ],
            font_size=19,
        )
        step2_title.move_to(text_panel_position() + 0.6 * UP)
        step2.next_to(step2_title, DOWN, buff=0.2, aligned_edge=LEFT)
        step2.shift(LEFT * 0.5)

        self.play(FadeIn(wing), run_time=1)
        self.play(Write(step2_title), Write(step2), run_time=1)
        self.wait(1)
        self.play(FadeOut(step2_title), FadeOut(step2), run_time=0.35)

        # -------------------------------------------------------------------------
        # STEP 3: Streamlines — reference style (horizontal, color bands)
        # -------------------------------------------------------------------------
        step3_title = Text(
            "Air has to go somewhere: over or under the wing",
            font_size=22,
            font="Arial",
            color=YELLOW,
            t2c={"over": TEAL_C, "under": BLUE_C},
        )
        step3 = bullet_text_styled(
            [
                (
                    "Streamlines can't go through — they go OVER or UNDER.",
                    None,
                    {"OVER": TEAL_C, "UNDER": BLUE_C},
                ),
                (
                    "Over: follow the curved top.  Under: follow the flatter bottom.",
                    GREY_A,
                ),
            ],
            font_size=19,
        )
        step3_title.move_to(text_panel_position() + 0.55 * UP)
        step3.next_to(step3_title, DOWN, buff=0.18, aligned_edge=LEFT)
        step3.shift(LEFT * 0.4)

        self.play(Write(step3_title), Write(step3), run_time=0.9)
        self.wait(0.5)

        all_streamlines = streamlines_reference_style(
            wing_center[0], wing_center_y, CHORD * 0.5, n_above=6, n_below=6
        )
        self.play(
            *[ShowCreation(s) for s in all_streamlines],
            run_time=2,
        )
        self.wait(0.8)
        self.play(FadeOut(step3_title), FadeOut(step3), run_time=0.35)

        # -------------------------------------------------------------------------
        # STEP 4: Longer path => faster — labels OUTSIDE with arrows
        # -------------------------------------------------------------------------
        step4_title = Text(
            "The path over the top is longer",
            font_size=22,
            font="Arial",
            color=YELLOW,
            t2w={"longer": "bold"},
        )
        step4 = bullet_text_styled(
            [
                (
                    "Same time => air above travels farther => air above moves FASTER.",
                    None,
                    {"FASTER": TEAL_C},
                ),
                (
                    "Key: faster flow on top, slower flow on the bottom.",
                    None,
                    {"faster": TEAL_C, "slower": BLUE_C},
                ),
            ],
            font_size=19,
        )
        step4_title.move_to(text_panel_position() + 0.5 * UP)
        step4.next_to(step4_title, DOWN, buff=0.18, aligned_edge=LEFT)

        # Labels outside figure with arrows pointing in
        high_vel_label = Text(
            "High-velocity region", font_size=18, font="Arial", color=GREEN_C
        )
        high_vel_label.to_edge(RIGHT, buff=0.35).shift(0.5 * UP)
        high_arrow = Arrow(
            high_vel_label.get_left(),
            wing_center + 0.5 * UP,
            thickness=2,
            color=GREEN_C,
            buff=0.06,
        )
        low_vel_label = Text(
            "Low-velocity region", font_size=18, font="Arial", color=BLUE_C
        )
        low_vel_label.to_edge(RIGHT, buff=0.35).shift(0.1 * DOWN)
        low_arrow = Arrow(
            low_vel_label.get_left(),
            wing_center + 0.5 * DOWN,
            thickness=2,
            color=BLUE_C,
            buff=0.06,
        )

        self.play(Write(step4_title), Write(step4), run_time=0.9)
        self.play(
            Write(high_vel_label),
            GrowArrow(high_arrow),
            Write(low_vel_label),
            GrowArrow(low_arrow),
            run_time=0.8,
        )
        self.wait(1.2)
        self.play(
            FadeOut(step4_title),
            FadeOut(step4),
            FadeOut(high_vel_label),
            FadeOut(high_arrow),
            FadeOut(low_vel_label),
            FadeOut(low_arrow),
            run_time=0.35,
        )

        # -------------------------------------------------------------------------
        # STEP 5: Bernoulli — colored key terms
        # -------------------------------------------------------------------------
        step5_title = Text(
            "Bernoulli's principle: faster air = lower pressure",
            font_size=22,
            font="Arial",
            color=YELLOW,
            t2c={"faster": TEAL_C, "lower pressure": RED_C},
        )
        step5 = bullet_text_styled(
            [
                (
                    "Above the wing: air faster => pressure LOWER.",
                    None,
                    {"faster": TEAL_C, "LOWER": RED_C},
                ),
                (
                    "Below the wing: air slower => pressure HIGHER.",
                    None,
                    {"slower": BLUE_C, "HIGHER": GREEN_C},
                ),
            ],
            font_size=19,
        )
        formula_bernoulli = Text(
            "P  +  (1/2) rho v^2  =  constant   =>   higher v => lower P",
            font_size=17,
            font="Arial",
            t2c={"P": BLUE_C, "v": TEAL_C, "lower P": RED_C},
        )
        step5_title.move_to(text_panel_position() + 0.55 * UP)
        step5.next_to(step5_title, DOWN, buff=0.15, aligned_edge=LEFT)
        formula_bernoulli.next_to(step5, DOWN, buff=0.2)

        self.play(Write(step5_title), run_time=0.6)
        self.play(Write(step5), Write(formula_bernoulli), run_time=1)
        self.wait(1.2)
        self.play(
            FadeOut(step5_title),
            FadeOut(step5),
            FadeOut(formula_bernoulli),
            run_time=0.35,
        )

        # -------------------------------------------------------------------------
        # STEP 6: Pressure difference = lift — highlight LIFT
        # -------------------------------------------------------------------------
        step6_title = Text(
            "Pressure difference pushes the wing up",
            font_size=22,
            font="Arial",
            color=YELLOW,
            t2c={"Pressure difference": ORANGE, "up": GREEN_C},
        )
        step6 = bullet_text_styled(
            [
                (
                    "Push from below stronger than from above => net force UPWARD = LIFT.",
                    None,
                    {"LIFT": GREEN_C},
                ),
            ],
            font_size=19,
        )
        formula_lift = Text(
            "Lift  L  =  (P_below - P_above)  x  wing area",
            font_size=19,
            font="Arial",
            t2c={"Lift": GREEN_C, "L": GREEN_C, "P_below": BLUE_C, "P_above": RED_C},
        )
        step6_title.move_to(text_panel_position() + 0.5 * UP)
        step6.next_to(step6_title, DOWN, buff=0.15, aligned_edge=LEFT)
        formula_lift.next_to(step6, DOWN, buff=0.18)

        lift_start = wing_center + 0.3 * UP
        lift_end = lift_start + 1.1 * UP
        lift_arrow = Arrow(
            lift_start,
            lift_end,
            thickness=4,
            color=GREEN_C,
            buff=0.05,
        )
        lift_arrow_label = Text("Lift L", font_size=22, font="Arial", color=GREEN_C)
        lift_arrow_label.next_to(lift_end, UP, buff=0.08)

        self.play(Write(step6_title), Write(step6), Write(formula_lift), run_time=0.9)
        self.play(GrowArrow(lift_arrow), Write(lift_arrow_label), run_time=0.7)
        self.wait(1.2)
        self.play(
            FadeOut(step6_title),
            FadeOut(step6),
            FadeOut(formula_lift),
            run_time=0.35,
        )

        # -------------------------------------------------------------------------
        # STEP 7: Newton
        # -------------------------------------------------------------------------
        step7_title = Text(
            "Newton's third law: action and reaction",
            font_size=22,
            font="Arial",
            color=YELLOW,
            t2c={"Newton's third law": GOLD_C},
        )
        step7 = bullet_text_styled(
            [
                (
                    "Wing deflects the air downward => air pushes wing UPWARD (lift).",
                    None,
                    {"downward": BLUE_C, "UPWARD": GREEN_C, "lift": GREEN_C},
                ),
                ("Bernoulli and Newton: two ways to describe the same force.", GREY_A),
            ],
            font_size=19,
        )
        step7_title.move_to(text_panel_position() + 0.5 * UP)
        step7.next_to(step7_title, DOWN, buff=0.18, aligned_edge=LEFT)

        self.play(Write(step7_title), Write(step7), run_time=1)
        self.wait(1.2)
        self.play(FadeOut(step7_title), FadeOut(step7), run_time=0.35)

        # -------------------------------------------------------------------------
        # STEP 8: Why the plane flies
        # -------------------------------------------------------------------------
        step8_title = Text(
            "Why the plane takes off and stays in the air",
            font_size=22,
            font="Arial",
            color=YELLOW,
        )
        step8 = bullet_text_styled(
            [
                (
                    "As long as the plane moves, air flows over the wings => lift.",
                    None,
                    {"lift": GREEN_C},
                ),
                (
                    "Lift > Weight  =>  plane climbs.",
                    None,
                    {"Lift": GREEN_C, "Weight": RED_C},
                ),
                (
                    "Lift = Weight  =>  level flight.",
                    None,
                    {"Lift": GREEN_C, "Weight": RED_C},
                ),
            ],
            font_size=19,
        )
        step8_title.move_to(text_panel_position() + 0.5 * UP)
        step8.next_to(step8_title, DOWN, buff=0.18, aligned_edge=LEFT)

        self.play(Write(step8_title), Write(step8), run_time=1.1)
        self.wait(1.8)
        self.play(FadeOut(step8_title), FadeOut(step8), run_time=0.35)

        # -------------------------------------------------------------------------
        # Summary and end
        # -------------------------------------------------------------------------
        summary = Text(
            "Shape -> faster/slower flow -> pressure difference -> LIFT.",
            font_size=20,
            font="Arial",
            t2c={
                "faster": TEAL_C,
                "slower": BLUE_C,
                "pressure difference": ORANGE,
                "LIFT": GREEN_C,
            },
        )
        summary.move_to(text_panel_position())
        self.play(Write(summary), run_time=1)
        self.wait(1.8)

        self.play(
            FadeOut(wing),
            FadeOut(lift_arrow),
            FadeOut(lift_arrow_label),
            *[FadeOut(s) for s in all_streamlines],
            FadeOut(summary),
            FadeOut(title),
            run_time=1,
        )

        conclusion = Text(
            "Now you can explain lift to your mom.",
            font_size=26,
            font="Arial",
            color=WHITE,
            t2c={"lift": GREEN_C},
        )
        conclusion.move_to(ORIGIN)
        self.play(Write(conclusion), run_time=1)
        self.wait(2)
