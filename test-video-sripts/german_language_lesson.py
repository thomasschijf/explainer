"""
German: A Language of Hidden Connections
Language Transfer – Complete German lesson explainer.
Covers etymology, sound shifts, word order, and the verb sandwich.
Run:  .venv/bin/python -m manimlib test-video-sripts/german_language_lesson.py GermanLanguageLesson -w
"""

from manimlib import *
import numpy as np

# ═══════════════════════════════════════════
#  Colors & constants
# ═══════════════════════════════════════════

DE_COLOR = TEAL_C
EN_COLOR = GOLD_C
TEACHER_COLOR = BLUE_C
STUDENT_COLOR = GREEN_C
RULE_COLOR = YELLOW
SHIFT_COLOR = RED_C
CENTER_PT = np.array([0, 0, 0])


# ═══════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════


def _txt(s, sz=20, col=WHITE, **kw):
    return Text(s, font_size=sz, font="Arial", color=col, **kw)


def _teacher(s, sz=19):
    label = _txt("Teacher: ", sz, TEACHER_COLOR)
    body = _txt(s, sz, WHITE)
    body.next_to(label, RIGHT, buff=0.08, aligned_edge=UP)
    return VGroup(label, body)


def _student(s, sz=19):
    label = _txt("Student: ", sz, STUDENT_COLOR)
    body = _txt(s, sz, WHITE)
    body.next_to(label, RIGHT, buff=0.08, aligned_edge=UP)
    return VGroup(label, body)


def _dialogue_pair(teacher_text, student_text, sz=19):
    t = _teacher(teacher_text, sz)
    s = _student(student_text, sz)
    s.next_to(t, DOWN, buff=0.25, aligned_edge=LEFT)
    return VGroup(t, s)


def _word_pair(en_word, de_word, arrow_color=SHIFT_COLOR, sz=30):
    en = _txt(en_word, sz, EN_COLOR)
    arr = Arrow(LEFT * 0.1, RIGHT * 0.1, color=arrow_color, thickness=0.04)
    de = _txt(de_word, sz, DE_COLOR)
    grp = VGroup(en, arr, de)
    grp.arrange(RIGHT, buff=0.35)
    return grp


def _shift_row(pairs, y_offset=0, sz=24):
    rows = VGroup()
    for i, (en, de) in enumerate(pairs):
        wp = _word_pair(en, de, sz=sz)
        wp.move_to(np.array([0, y_offset - i * 0.65, 0]))
        rows.add(wp)
    return rows


def _bracket_block(items, title_text, title_color=RULE_COLOR, sz=18):
    title = _txt(title_text, sz + 4, title_color)
    lines = VGroup()
    for item in items:
        t = _txt(item, sz)
        lines.add(t)
    lines.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    title.next_to(lines, UP, buff=0.25)
    return VGroup(title, lines)


def _sentence_build(parts, colors, sz=26):
    """Animate building a German sentence word by word."""
    words = []
    for part, col in zip(parts, colors):
        words.append(_txt(part, sz, col))
    grp = VGroup(*words)
    grp.arrange(RIGHT, buff=0.18)
    return grp


# ═══════════════════════════════════════════
#  Visual components
# ═══════════════════════════════════════════


def _etymology_tree(root_en, root_de, descendants, ctr=CENTER_PT):
    root_en_txt = _txt(root_en, 26, EN_COLOR)
    root_de_txt = _txt(root_de, 26, DE_COLOR)
    root_en_txt.move_to(ctr + UP * 1.8 + LEFT * 2)
    root_de_txt.move_to(ctr + UP * 1.8 + RIGHT * 2)

    conn = Line(
        root_en_txt.get_right() + RIGHT * 0.1,
        root_de_txt.get_left() + LEFT * 0.1,
        color=YELLOW,
        stroke_width=2,
    )

    desc_grp = VGroup()
    for i, (word, col) in enumerate(descendants):
        t = _txt(word, 18, col)
        t.move_to(ctr + np.array([-3 + 1.5 * i, 0.6, 0]))
        arr = Arrow(
            root_en_txt.get_bottom() + DOWN * 0.05,
            t.get_top() + UP * 0.05,
            color=GREY_A,
            thickness=0.02,
        )
        desc_grp.add(VGroup(arr, t))

    return VGroup(root_en_txt, root_de_txt, conn, desc_grp)


def _sound_shift_table(ctr=CENTER_PT):
    headers = VGroup(
        _txt("English", 22, EN_COLOR),
        _txt("German", 22, DE_COLOR),
        _txt("Example", 22, WHITE),
    )
    headers[0].move_to(ctr + np.array([-3, 1.5, 0]))
    headers[1].move_to(ctr + np.array([0, 1.5, 0]))
    headers[2].move_to(ctr + np.array([3, 1.5, 0]))

    rows_data = [
        ("W → V sound", "W = V", "will → [vill]"),
        ("S → Z sound", "S + vowel = Z", "sehen [zehen]"),
        ("T → S", "T → S", "eat → essen"),
        ("TH → D", "TH → D", "thank → danke"),
        ("P → F", "P → F", "hope → hoffen"),
    ]

    rows = VGroup()
    for i, (en, de, ex) in enumerate(rows_data):
        y = 0.9 - i * 0.55
        en_t = _txt(en, 18, EN_COLOR)
        de_t = _txt(de, 18, DE_COLOR)
        ex_t = _txt(ex, 18, GREY_A)
        en_t.move_to(ctr + np.array([-3, y, 0]))
        de_t.move_to(ctr + np.array([0, y, 0]))
        ex_t.move_to(ctr + np.array([3, y, 0]))
        rows.add(VGroup(en_t, de_t, ex_t))

    h_line = Line(
        ctr + np.array([-4.5, 1.2, 0]),
        ctr + np.array([4.5, 1.2, 0]),
        color=GREY_B,
        stroke_width=1,
    )

    return VGroup(headers, h_line, rows)


def _word_order_diagram(parts, labels, colors, ctr=CENTER_PT):
    boxes = VGroup()
    total_w = len(parts) * 1.8
    start_x = -total_w / 2 + 0.9

    for i, (part, label, col) in enumerate(zip(parts, labels, colors)):
        rect = Rectangle(width=1.6, height=0.7)
        rect.set_fill(col, opacity=0.15).set_stroke(col, width=2)
        rect.move_to(ctr + np.array([start_x + i * 1.8, 0, 0]))

        word_t = _txt(part, 20, col)
        word_t.move_to(rect.get_center())

        lbl_t = _txt(label, 14, GREY_A)
        lbl_t.next_to(rect, DOWN, buff=0.08)

        boxes.add(VGroup(rect, word_t, lbl_t))

    return boxes


def _verb_sandwich_diagram(v1, middle_parts, v2, ctr=CENTER_PT):
    bread_l = Rectangle(width=1.5, height=1.2)
    bread_l.set_fill(DE_COLOR, opacity=0.2).set_stroke(DE_COLOR, width=2)
    bread_r = Rectangle(width=1.5, height=1.2)
    bread_r.set_fill(DE_COLOR, opacity=0.2).set_stroke(DE_COLOR, width=2)

    fill_w = len(middle_parts) * 1.3
    filling = Rectangle(width=max(fill_w, 2.5), height=0.9)
    filling.set_fill(EN_COLOR, opacity=0.1).set_stroke(EN_COLOR, width=1.5)

    grp = VGroup(bread_l, filling, bread_r)
    grp.arrange(RIGHT, buff=0.15)
    grp.move_to(ctr)

    v1_txt = _txt(v1, 22, DE_COLOR)
    v1_txt.move_to(bread_l.get_center())
    v2_txt = _txt(v2, 22, DE_COLOR)
    v2_txt.move_to(bread_r.get_center())

    mid_txts = VGroup()
    for part in middle_parts:
        t = _txt(part, 18, WHITE)
        mid_txts.add(t)
    mid_txts.arrange(RIGHT, buff=0.15)
    mid_txts.move_to(filling.get_center())

    lbl_v1 = _txt("Verb 1", 14, DE_COLOR)
    lbl_v1.next_to(bread_l, DOWN, buff=0.08)
    lbl_v2 = _txt("Verb 2", 14, DE_COLOR)
    lbl_v2.next_to(bread_r, DOWN, buff=0.08)
    lbl_mid = _txt("everything else", 14, GREY_A)
    lbl_mid.next_to(filling, DOWN, buff=0.08)

    return VGroup(
        bread_l, filling, bread_r, v1_txt, v2_txt, mid_txts, lbl_v1, lbl_v2, lbl_mid
    )


# ═══════════════════════════════════════════
#  MAIN SCENE
# ═══════════════════════════════════════════


class GermanLanguageLesson(Scene):
    def construct(self):
        self._act_i_intro()
        self._act_ii_ich_will()
        self._act_iii_sound_shifts()
        self._act_iv_pronouns_and_basics()
        self._act_v_word_order()
        self._act_vi_verb_sandwich()
        self._act_vii_modal_verbs()
        self._act_viii_summary()

    def _bottom(self, t, wait=2.0, buff=0.4, rt=1.2):
        t.to_edge(DOWN, buff=buff)
        self.play(Write(t), run_time=rt)
        self.wait(wait)
        self.play(FadeOut(t), run_time=0.3)

    # ── ACT I: Title & Introduction ─────────

    def _act_i_intro(self):
        title = _txt("German: A Language of\nHidden Connections", 40)
        sub = _txt("Based on Language Transfer – Complete German", 20, GREY_A)
        sub.next_to(title, DOWN, buff=0.5)

        self.play(Write(title), run_time=1.5)
        self.play(Write(sub), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(sub), run_time=0.5)

        hook = _txt(
            "What if you already know more German\nthan you think?",
            28,
            RULE_COLOR,
        )
        self.play(Write(hook), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(hook), run_time=0.4)

    # ── ACT II: Ich will & Etymology ────────

    def _act_ii_ich_will(self):
        h = _txt("Ich will = I want", 32, RULE_COLOR)
        h.to_edge(UP, buff=0.35)
        self.play(Write(h), run_time=0.8)

        de_text = _txt("Ich will", 36, DE_COLOR)
        en_text = _txt("I want", 36, EN_COLOR)
        de_text.move_to(UP * 0.8)
        en_text.move_to(UP * 0.8)

        self.play(Write(de_text), run_time=0.8)
        self.wait(0.5)

        cross = _txt("≠  I will", 28, RED_C)
        cross.next_to(de_text, RIGHT, buff=0.5)
        self.play(Write(cross), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(cross), run_time=0.3)

        eq = _txt("=  I want", 28, GREEN_C)
        eq.next_to(de_text, RIGHT, buff=0.5)
        self.play(Write(eq), run_time=0.6)
        self.wait(1)

        self.play(FadeOut(de_text), FadeOut(eq), run_time=0.3)

        etym_title = _txt("The hidden connection", 24, GREY_A)
        etym_title.move_to(UP * 1.0)
        self.play(Write(etym_title), run_time=0.6)

        en_will = _txt("English: will", 22, EN_COLOR)
        en_will.move_to(UP * 0.3 + LEFT * 2.5)
        de_wollen = _txt("German: wollen", 22, DE_COLOR)
        de_wollen.move_to(UP * 0.3 + RIGHT * 2.5)
        conn = Arrow(
            en_will.get_right() + RIGHT * 0.1,
            de_wollen.get_left() + LEFT * 0.1,
            color=YELLOW,
            thickness=0.03,
        )

        self.play(Write(en_will), Write(de_wollen), GrowArrow(conn), run_time=1)

        examples = VGroup(
            _txt('"the will of the people" = the want of the people', 18, GREY_A),
            _txt('"I will go" originally meant "I want to go"', 18, GREY_A),
            _txt("\"I don't have the will\" = I don't have the want", 18, GREY_A),
        )
        examples.arrange(DOWN, buff=0.15)
        examples.move_to(DOWN * 0.8)
        for ex in examples:
            self.play(Write(ex), run_time=0.7)
        self.wait(2)

        self.play(
            FadeOut(h),
            FadeOut(etym_title),
            FadeOut(en_will),
            FadeOut(de_wollen),
            FadeOut(conn),
            FadeOut(examples),
            run_time=0.4,
        )

        morgen_h = _txt("Morgen = tomorrow / morning", 26, RULE_COLOR)
        morgen_h.to_edge(UP, buff=0.4)
        self.play(Write(morgen_h), run_time=0.7)

        comp = VGroup(
            _txt("German:  morgen  = tomorrow & morning", 22, DE_COLOR),
            _txt("Spanish: mañana = tomorrow & morning", 22, GOLD_C),
        )
        comp.arrange(DOWN, buff=0.25)
        comp.move_to(UP * 0.3)
        self.play(Write(comp), run_time=1)

        ex_sent = _txt(
            "Ich helfe morgen = I help tomorrow = I will help tomorrow", 20, GREY_A
        )
        ex_sent.move_to(DOWN * 0.6)
        self.play(Write(ex_sent), run_time=0.8)

        self._bottom(
            _txt(
                "In German, you don't need a word for 'will' to talk about the future.\n"
                "If the context shows the future (like 'morgen'), just use the present tense!",
                17,
            ),
            2.5,
        )

        self.play(FadeOut(morgen_h), FadeOut(comp), FadeOut(ex_sent), run_time=0.4)

    # ── ACT III: Sound Shifts ───────────────

    def _act_iii_sound_shifts(self):
        h = _txt("Sound Shifts: English → German", 28, RULE_COLOR)
        h.to_edge(UP, buff=0.35)
        self.play(Write(h), run_time=0.8)

        # W sounds like V
        w_title = _txt("W sounds like V", 24, DE_COLOR)
        w_title.move_to(UP * 1.0)
        self.play(Write(w_title), run_time=0.5)

        w_examples = _shift_row(
            [
                ("will → [vill]", "ich will = I want"),
                ("wir = we", "W-I-R [veer]"),
                ("waschen", "to wash"),
            ],
            y_offset=0.2,
            sz=20,
        )
        self.play(FadeIn(w_examples), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(w_title), FadeOut(w_examples), run_time=0.3)

        # S sounds like Z
        s_title = _txt("S + vowel sounds like Z", 24, DE_COLOR)
        s_title.move_to(UP * 1.0)
        self.play(Write(s_title), run_time=0.5)

        s_examples = _shift_row(
            [
                ("sehen = to see", "[zehen]"),
                ("Sie = they / you", "[zee]"),
                ("singen = to sing", "[zingen]"),
            ],
            y_offset=0.2,
            sz=20,
        )
        self.play(FadeIn(s_examples), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(s_title), FadeOut(s_examples), run_time=0.3)

        # Consonant shifts table
        self.play(FadeOut(h), run_time=0.2)
        h2 = _txt("Consonant Shifts", 28, RULE_COLOR)
        h2.to_edge(UP, buff=0.35)
        self.play(Write(h2), run_time=0.6)

        table = _sound_shift_table(DOWN * 0.2)
        self.play(FadeIn(table), run_time=1.5)
        self.wait(3)

        self._bottom(
            _txt(
                "These patterns let you guess German words from English!\n"
                "eat → essen, water → Wasser, better → besser, hate → hassen",
                17,
                GREEN_C,
            ),
            2.5,
        )

        self.play(FadeOut(h2), FadeOut(table), run_time=0.4)

    # ── ACT IV: Pronouns & Basic Verbs ──────

    def _act_iv_pronouns_and_basics(self):
        h = _txt("Building Blocks", 28, RULE_COLOR)
        h.to_edge(UP, buff=0.35)
        self.play(Write(h), run_time=0.6)

        pronouns = VGroup(
            _txt("ich = I", 24, DE_COLOR),
            _txt("mich = me", 24, DE_COLOR),
            _txt("wir = we", 24, DE_COLOR),
            _txt("Sie = they / you (formal)", 24, DE_COLOR),
            _txt("es = it", 24, DE_COLOR),
        )
        pronouns.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        pronouns.move_to(LEFT * 2.5 + DOWN * 0.1)

        verbs = VGroup(
            _txt("kommen = to come", 24, EN_COLOR),
            _txt("gehen = to go", 24, EN_COLOR),
            _txt("sehen = to see", 24, EN_COLOR),
            _txt("essen = to eat", 24, EN_COLOR),
            _txt("kaufen = to buy", 24, EN_COLOR),
        )
        verbs.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        verbs.move_to(RIGHT * 2.5 + DOWN * 0.1)

        p_label = _txt("Pronouns", 20, GREY_A)
        p_label.next_to(pronouns, UP, buff=0.2)
        v_label = _txt("Key Verbs", 20, GREY_A)
        v_label.next_to(verbs, UP, buff=0.2)

        self.play(Write(p_label), Write(v_label), run_time=0.5)
        for p, v in zip(pronouns, verbs):
            self.play(Write(p), Write(v), run_time=0.5)
        self.wait(2)

        self._bottom(
            _txt(
                "With 'wir' (we) and 'Sie' (they/formal you), use the base verb form.\n"
                "wir kommen = we come  •  Sie sehen = they see / you (formal) see",
                17,
            ),
            2.5,
        )

        self.play(
            FadeOut(h),
            FadeOut(pronouns),
            FadeOut(verbs),
            FadeOut(p_label),
            FadeOut(v_label),
            run_time=0.4,
        )

        # die Kinder
        h3 = _txt("die = the  (TH → D shift!)", 26, RULE_COLOR)
        h3.to_edge(UP, buff=0.4)
        self.play(Write(h3), run_time=0.6)

        kinder = _txt("die Kinder = the children", 28, DE_COLOR)
        kinder.move_to(UP * 0.5)
        self.play(Write(kinder), run_time=0.7)

        kg = _txt("Kindergarten = children's garden", 20, GREY_A)
        kg.next_to(kinder, DOWN, buff=0.35)
        self.play(Write(kg), run_time=0.6)
        self.wait(1.5)

        self.play(FadeOut(h3), FadeOut(kinder), FadeOut(kg), run_time=0.4)

    # ── ACT V: Word Order ───────────────────

    def _act_v_word_order(self):
        h = _txt("German Word Order", 28, RULE_COLOR)
        h.to_edge(UP, buff=0.35)
        self.play(Write(h), run_time=0.7)

        # Basic statement
        st_label = _txt("Statement:", 20, GREY_A)
        st_label.move_to(UP * 1.0 + LEFT * 4)

        st = _word_order_diagram(
            ["Die Kinder", "kommen", "morgen", "nicht"],
            ["subject", "verb", "when", "not"],
            [WHITE, DE_COLOR, BLUE_C, RED_C],
            ctr=UP * 0.2,
        )
        self.play(Write(st_label), run_time=0.4)
        for box in st:
            self.play(FadeIn(box), run_time=0.4)

        en_trans = _txt("= The children are not coming tomorrow", 18, GREY_A)
        en_trans.move_to(DOWN * 0.7)
        self.play(Write(en_trans), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(st), FadeOut(st_label), FadeOut(en_trans), run_time=0.3)

        # Question (inversion)
        q_label = _txt("Question (inversion — swap subject & verb):", 20, GREY_A)
        q_label.move_to(UP * 1.0 + LEFT * 2)

        q = _word_order_diagram(
            ["Kommen", "die Kinder", "morgen", "nicht?"],
            ["verb", "subject", "when", "not?"],
            [DE_COLOR, WHITE, BLUE_C, RED_C],
            ctr=UP * 0.2,
        )
        self.play(Write(q_label), run_time=0.5)
        for box in q:
            self.play(FadeIn(box), run_time=0.4)

        en_q = _txt("= Aren't the children coming tomorrow?", 18, GREY_A)
        en_q.move_to(DOWN * 0.7)
        self.play(Write(en_q), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(q), FadeOut(q_label), FadeOut(en_q), run_time=0.3)

        # Command = same order as question, different tone
        cmd_note = _txt(
            "Command = same word order as question, different tone!\n"
            "Kommen Sie morgen!  (Come tomorrow!)\n"
            "Kommen Sie morgen?  (Are you coming tomorrow?)",
            20,
        )
        self.play(Write(cmd_note), run_time=1)
        self.wait(2)
        self.play(FadeOut(cmd_note), run_time=0.3)

        # nicht placement rule
        rule = VGroup(
            _txt("The 'nicht' rule:", 22, RULE_COLOR),
            _txt("Time expression (morgen, jetzt, später)", 18, BLUE_C),
            _txt("comes BEFORE nicht", 18, RED_C),
            _txt("Sie kommen morgen nicht", 20, DE_COLOR),
            _txt("(They are not coming tomorrow)", 16, GREY_A),
        )
        rule.arrange(DOWN, buff=0.2)
        self.play(Write(rule), run_time=1.5)
        self.wait(2)

        self._bottom(
            _txt(
                "The time expression can move for emphasis:\n"
                "Sie kommen nicht morgen = They're coming, NOT tomorrow (stressed)",
                16,
                GREY_A,
            ),
            2,
        )

        self.play(FadeOut(h), FadeOut(rule), run_time=0.4)

    # ── ACT VI: The Verb Sandwich ───────────

    def _act_vi_verb_sandwich(self):
        h = _txt("The Verb Sandwich", 32, RULE_COLOR)
        h.to_edge(UP, buff=0.3)
        self.play(Write(h), run_time=0.8)

        explanation = _txt(
            "When you use two verbs, German wraps\n"
            "everything between them like a sandwich.",
            20,
        )
        explanation.move_to(UP * 0.9)
        self.play(Write(explanation), run_time=1)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=0.3)

        # Visual sandwich diagram
        sandwich = _verb_sandwich_diagram(
            "Ich will",
            ["es", "morgen"],
            "kaufen",
            ctr=UP * 0.5,
        )
        self.play(FadeIn(sandwich), run_time=1.2)

        en_below = _txt("= I want to buy it tomorrow", 20, GREY_A)
        en_below.move_to(DOWN * 0.7)
        self.play(Write(en_below), run_time=0.6)

        literal = _txt("Literally: I want it tomorrow to-buy", 18, EN_COLOR)
        literal.next_to(en_below, DOWN, buff=0.2)
        self.play(Write(literal), run_time=0.6)
        self.wait(2)

        self.play(FadeOut(sandwich), FadeOut(en_below), FadeOut(literal), run_time=0.3)

        # Why? The value system of German
        why_h = _txt("Why? The value system of German", 24, TEAL_C)
        why_h.move_to(UP * 1.0)
        self.play(Write(why_h), run_time=0.7)

        points = VGroup(
            _txt("German saves the key information for last.", 19, WHITE),
            _txt("The listener can't assume what you're saying.", 19, WHITE),
            _txt("This prevents interruption and presumption.", 19, WHITE),
            _txt(
                '"Ich will es morgen..." → you must wait for the last verb!',
                19,
                DE_COLOR,
            ),
        )
        points.arrange(DOWN, buff=0.2)
        points.move_to(DOWN * 0.1)

        for p in points:
            self.play(Write(p), run_time=0.7)
        self.wait(2)

        self.play(FadeOut(why_h), FadeOut(points), run_time=0.3)

        # More examples
        examples_h = _txt("Building the sandwich step by step", 22, RULE_COLOR)
        examples_h.to_edge(UP, buff=0.6)
        self.play(Write(examples_h), run_time=0.6)

        sents = [
            (
                "I can't send it tomorrow",
                ["Ich kann", "es", "morgen", "nicht", "senden"],
                [DE_COLOR, WHITE, BLUE_C, RED_C, DE_COLOR],
            ),
            (
                "I can't buy it later",
                ["Ich kann", "es", "später", "nicht", "kaufen"],
                [DE_COLOR, WHITE, BLUE_C, RED_C, DE_COLOR],
            ),
            (
                "I can't stay here now",
                ["Ich kann", "jetzt", "nicht", "hier", "bleiben"],
                [DE_COLOR, BLUE_C, RED_C, WHITE, DE_COLOR],
            ),
        ]

        for en_s, parts, colors in sents:
            en_line = _txt(en_s, 18, GREY_A)
            en_line.move_to(UP * 0.6)
            self.play(Write(en_line), run_time=0.5)

            built = _sentence_build(parts, colors, sz=22)
            built.move_to(DOWN * 0.2)

            for word in built:
                self.play(Write(word), run_time=0.3)

            self.wait(1.5)
            self.play(FadeOut(en_line), FadeOut(built), run_time=0.3)

        self.play(FadeOut(h), FadeOut(examples_h), run_time=0.3)

    # ── ACT VII: Modal Verbs ────────────────

    def _act_vii_modal_verbs(self):
        h = _txt("Modal Verbs & Irregulars", 28, RULE_COLOR)
        h.to_edge(UP, buff=0.35)
        self.play(Write(h), run_time=0.7)

        modals = VGroup(
            _txt("wollen (to want)  →  ich will (irregular!)", 22, DE_COLOR),
            _txt("können (to be able) →  ich kann (irregular!)", 22, DE_COLOR),
            _txt("müssen (to must)  →  ich muss (irregular!)", 22, DE_COLOR),
        )
        modals.arrange(DOWN, buff=0.3)
        modals.move_to(UP * 0.3)

        for m in modals:
            self.play(Write(m), run_time=0.7)
        self.wait(1.5)

        note = _txt(
            "müssen ≈ 'have to' (not as heavy as English 'must')\n"
            "ich muss nicht = I don't have to (NOT 'I must not'!)",
            18,
            GREY_A,
        )
        note.move_to(DOWN * 1.0)
        self.play(Write(note), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(modals), FadeOut(note), run_time=0.3)

        # Umlauts
        uml_h = _txt("Umlauts: the two dots", 24, RULE_COLOR)
        uml_h.move_to(UP * 1.0)
        self.play(Write(uml_h), run_time=0.6)

        umlauts = VGroup(
            _txt("ä  →  sounds like 'e'  (spät = late)", 22, DE_COLOR),
            _txt("ö  →  sounds like 'bird'  (können)", 22, DE_COLOR),
            _txt("ü  →  make 'u', keep lips, say 'e'  (über = over)", 22, DE_COLOR),
        )
        umlauts.arrange(DOWN, buff=0.25)
        umlauts.move_to(DOWN * 0.1)

        for u in umlauts:
            self.play(Write(u), run_time=0.6)
        self.wait(2)

        self.play(FadeOut(h), FadeOut(uml_h), FadeOut(umlauts), run_time=0.4)

        # -ieren verbs
        ieren_h = _txt("Latin-origin verbs: -ieren", 24, RULE_COLOR)
        ieren_h.to_edge(UP, buff=0.4)
        self.play(Write(ieren_h), run_time=0.6)

        ieren_examples = VGroup(
            _txt("organisieren, studieren, existieren", 22, DE_COLOR),
            _txt("adoptieren, aktivieren, funktionieren", 22, DE_COLOR),
            _txt("informieren, kopieren, definieren", 22, DE_COLOR),
        )
        ieren_examples.arrange(DOWN, buff=0.2)

        self.play(Write(ieren_examples), run_time=1.2)
        self.wait(1.5)

        self._bottom(
            _txt(
                "If a word ends in '-ate', '-ify', '-ize' in English,\n"
                "try adding '-ieren' in German. You'll often be right!",
                18,
                GREEN_C,
            ),
            2,
        )

        self.play(FadeOut(ieren_h), FadeOut(ieren_examples), run_time=0.4)

    # ── ACT VIII: Summary ───────────────────

    def _act_viii_summary(self):
        h = _txt("What You've Learned", 30, RULE_COLOR)
        h.to_edge(UP, buff=0.35)
        self.play(Write(h), run_time=0.7)

        items = [
            ("Ich will = I want", DE_COLOR),
            ("Sound shifts: W→V, S→Z, T→S, TH→D, P→F", SHIFT_COLOR),
            ("Morgen = tomorrow (no need for 'will')", DE_COLOR),
            ("Word order: time before nicht", BLUE_C),
            ("Questions & commands use inversion", WHITE),
            ("Verb sandwich: Verb 1 ... everything ... Verb 2", TEAL_C),
            ("Modal verbs: wollen, können, müssen", DE_COLOR),
            ("Umlauts: ä ö ü change the vowel sound", WHITE),
            ("-ieren: Latin verbs you already know", GREEN_C),
        ]

        summary = VGroup()
        for i, (text, col) in enumerate(items):
            t = _txt(text, 17, col)
            t.move_to(np.array([0, 0.8 - i * 0.38, 0]))
            summary.add(t)

        for s in summary:
            self.play(Write(s), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(h), FadeOut(summary), run_time=0.5)

        # End card
        e1 = _txt("Languages are not thought.", 28)
        e2 = _txt("They are tools we use in thought.", 24, GREY_A)
        e3 = _txt(
            "Learning a language that does this differently\n"
            "can be a life-changing experience.",
            22,
            RULE_COLOR,
        )
        e2.next_to(e1, DOWN, buff=0.3)
        e3.next_to(e2, DOWN, buff=0.4)

        self.play(Write(e1), run_time=1)
        self.play(Write(e2), run_time=0.8)
        self.play(Write(e3), run_time=1)
        self.wait(3)

        credit = _txt("Language Transfer — Complete German", 18, GREY_B)
        credit.to_edge(DOWN, buff=0.4)
        self.play(Write(credit), run_time=0.5)
        self.wait(2)
