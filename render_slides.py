# -*- coding: utf-8 -*-
from manim import (
    Text, Square, Line, Dot, RegularPolygon, Polygon, Circle, DashedLine,
    MathTex, VGroup,
    Write, FadeIn, FadeOut, Create, Transform,
    MoveAlongPath, LaggedStart,
    BLACK, WHITE, YELLOW, BLUE, RED, GREEN,
    UP, DOWN, LEFT, RIGHT, ORIGIN, smooth
)
from manim_slides import Slide


def title_slide(scene, ctx):
    title = Text("Triangulaciones Hamiltonianas \npara Renderizado Rápido", font_size=48, color=WHITE, line_spacing=0.75)
    title.move_to([0, 1, 0])
    subtitle = Text("Geometría Computacional 2026-2", font_size=24, color=WHITE)
    subtitle.next_to(title, DOWN, buff=0.5)

    corner_left = Text("Lara Guillén Gilabert", font_size=18, color=WHITE)
    corner_left.to_corner(DOWN + LEFT, buff=0.7)
    corner_right = Text("José Rubén Alfaro González", font_size=18, color=WHITE)
    corner_right.to_corner(DOWN + RIGHT, buff=0.7)

    scene.play(Write(title))
    scene.play(FadeIn(subtitle))
    scene.play(FadeIn(corner_left), FadeIn(corner_right))
    return {"title": title, "subtitle": subtitle, "corner_left": corner_left, "corner_right": corner_right}


def holes_slide(scene, ctx):
    import numpy as np
    from manim import (
        Text, Line, Dot, VGroup,
        Write, FadeIn, FadeOut, Create, Transform,
        WHITE,
        UP, DOWN, LEFT, RIGHT,
    )

    def p(x, y):
        return np.array([x, y, 0])

    # ── Fade out slide anterior ──────────────────────────────────────────
    all_prev = [v for v in ctx.values() if v is not None]
    if all_prev:
        scene.play(*[FadeOut(obj) for obj in all_prev])

    # ════════════════════════════════════════════════════════════════════
    # SLIDE 1 — Título + texto
    # ════════════════════════════════════════════════════════════════════
    heading = Text("Problema de los hoyos", font_size=36, color=WHITE)
    heading.to_corner(UP + LEFT, buff=0.4)

    intro = Text(
        "Ya vimos que es posible dar un camino hamiltoniano\n"
        "en un polígono sin hoyos. Sin embargo, cuando\n"
        "introducimos estos, el problema se complica:\n"
        "se vuelve un problema NP-completo.",
        font_size=22, color=WHITE, line_spacing=0.85,
    )
    intro.next_to(heading, DOWN, buff=0.35, aligned_edge=LEFT)

    idea_text = Text(
        "La idea de la demostración es la siguiente:",
        font_size=22, color=WHITE,
    )
    idea_text.next_to(intro, DOWN, buff=0.35, aligned_edge=LEFT)

    scene.play(Write(heading))
    scene.play(FadeIn(intro))
    scene.play(FadeIn(idea_text))
    scene.next_slide()
    scene.play(FadeOut(intro), FadeOut(idea_text))

    # ════════════════════════════════════════════════════════════════════
    # SLIDE 2 — Nodo: punto solo, centrado
    # ════════════════════════════════════════════════════════════════════
    cx, cy = 0.0, -0.2

    solo = Dot(p(cx, cy), radius=0.14, color=WHITE).set_z_index(2)
    scene.play(FadeIn(solo))
    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════
    # SLIDE 3 — Del punto salen 3 nuevos puntos (sin flechas)
    # Los tres puntos arrancan desde el centro y se dispersan
    # ════════════════════════════════════════════════════════════════════
    s = 0.9   # distancia desde el centro

    t1 = p(cx,       cy + s)            # arriba
    t2 = p(cx - s,   cy - s * 0.55)    # abajo-izq
    t3 = p(cx + s,   cy - s * 0.55)    # abajo-der

    # Los tres dots empiezan en el centro (encima del solo)
    dot1 = Dot(p(cx, cy), radius=0.13, color=WHITE).set_z_index(2)
    dot2 = Dot(p(cx, cy), radius=0.13, color=WHITE).set_z_index(2)
    dot3 = Dot(p(cx, cy), radius=0.13, color=WHITE).set_z_index(2)

    scene.add(dot1, dot2, dot3)

    # Se mueven a sus posiciones finales en triángulo
    scene.play(
        dot1.animate.move_to(t1),
        dot2.animate.move_to(t2),
        dot3.animate.move_to(t3),
        FadeOut(solo),
    )
    scene.next_slide()

    scene.play(FadeOut(dot1), FadeOut(dot2), FadeOut(dot3))

    # ════════════════════════════════════════════════════════════════════
    # SLIDE 4 — Arista simple centrada
    # ════════════════════════════════════════════════════════════════════
    half = 2.2
    eL = p(-half, 0.0)
    eR = p( half, 0.0)

    e_line = Line(eL, eR, color=WHITE, stroke_width=3)
    e_dotL = Dot(eL, radius=0.11, color=WHITE).set_z_index(2)
    e_dotR = Dot(eR, radius=0.11, color=WHITE).set_z_index(2)

    scene.play(Create(e_line), FadeIn(e_dotL), FadeIn(e_dotR))
    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════
    # SLIDE 5 — Transform → dos paralelas
    # ════════════════════════════════════════════════════════════════════
    gap = 0.5

    pTL = p(-half,  gap);  pTR = p( half,  gap)
    pBL = p(-half, -gap);  pBR = p( half, -gap)

    top_line = Line(pTL, pTR, color=WHITE, stroke_width=3)
    bot_line = Line(pBL, pBR, color=WHITE, stroke_width=3)
    dTL = Dot(pTL, radius=0.11, color=WHITE).set_z_index(2)
    dTR = Dot(pTR, radius=0.11, color=WHITE).set_z_index(2)
    dBL = Dot(pBL, radius=0.11, color=WHITE).set_z_index(2)
    dBR = Dot(pBR, radius=0.11, color=WHITE).set_z_index(2)

    scene.play(
        Transform(e_line,  top_line),
        Transform(e_dotL,  dTL),
        Transform(e_dotR,  dTR),
        FadeIn(bot_line), FadeIn(dBL), FadeIn(dBR),
    )
    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════
    # SLIDE 6 — Transform → vértice central en cada paralela
    # ════════════════════════════════════════════════════════════════════
    pTM = p(0.0,  gap)
    pBM = p(0.0, -gap)

    tTL = Line(pTL, pTM, color=WHITE, stroke_width=3)
    tTR = Line(pTM, pTR, color=WHITE, stroke_width=3)
    tBL = Line(pBL, pBM, color=WHITE, stroke_width=3)
    tBR = Line(pBM, pBR, color=WHITE, stroke_width=3)

    dTM = Dot(pTM, radius=0.11, color=WHITE).set_z_index(2)
    dBM = Dot(pBM, radius=0.11, color=WHITE).set_z_index(2)

    scene.play(
        Transform(e_line,   tTL),
        FadeIn(tTR),
        Transform(bot_line, tBL),
        FadeIn(tBR),
        FadeIn(dTM), FadeIn(dBM),
    )
    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════
    # SLIDE 7 — Los dos centrales suben → V hacia arriba
    # ════════════════════════════════════════════════════════════════════
    rise = 1.3

    vTM = p(0.0,  gap + rise)
    vBM = p(0.0, -gap + rise)

    vTL_line = Line(pTL, vTM, color=WHITE, stroke_width=3)
    vTR_line = Line(vTM, pTR, color=WHITE, stroke_width=3)
    vBL_line = Line(pBL, vBM, color=WHITE, stroke_width=3)
    vBR_line = Line(vBM, pBR, color=WHITE, stroke_width=3)

    dvTM = Dot(vTM, radius=0.11, color=WHITE).set_z_index(2)
    dvBM = Dot(vBM, radius=0.11, color=WHITE).set_z_index(2)

    scene.play(
        Transform(e_line,   vTL_line),
        Transform(tTR,      vTR_line),
        Transform(bot_line, vBL_line),
        Transform(tBR,      vBR_line),
        Transform(dTM,      dvTM),
        Transform(dBM,      dvBM),
    )
    scene.next_slide()

    all_objs = VGroup(
        e_line, e_dotL, e_dotR,
        bot_line, dBL, dBR,
        tTR, tBL, tBR,
        dTL, dTR, dTM, dBM,
        dvTM, dvBM,
    )

    return {
        "heading":  heading,
        "all_objs": all_objs,
    }


def paper_slide(scene, ctx):
    import numpy as np
    from manim import (
        Text, Line, Dot, Polygon, VGroup, DashedLine,
        Write, FadeIn, FadeOut, Create,
        WHITE, YELLOW, GRAY_B, BLUE_C, BLUE_D, RED, GREEN, ORANGE,
        UP, DOWN, LEFT, RIGHT,
    )

    LBL_SZ  = 16
    HEAD_SZ = 26
    SUB_SZ  = 18
    NOTE_SZ = 14

    def pt(gx, gy):
        return np.array([(gx - 30) * 0.17, (gy - 22) * 0.17, 0.0])

    PA = pt(25, 40)
    PB = pt(35, 40)
    PC = pt(55, 10)
    PD = pt(50,  5)
    PE = pt(10,  5)
    PF = pt( 5, 10)
    Pc = pt(30, 25)
    Pa = pt(25, 15)
    Pb = pt(35, 15)

    def mk_dot(pos, color=WHITE):
        return Dot(pos, radius=0.08, color=color).set_z_index(4)

    def mk_seg(a, b, color=WHITE, sw=2.5):
        return Line(a, b, color=color, stroke_width=sw)

    def mk_dash(a, b, color=GRAY_B, sw=2.0):
        return DashedLine(a, b, color=color, stroke_width=sw, dash_length=0.12)

    def mk_lbl(txt, pos, direction=UP, buff=0.13, color=BLUE_C, size=LBL_SZ):
        return Text(txt, font_size=size, color=color).next_to(pos, direction, buff=buff)

    def mk_num(txt, pos, direction=DOWN, buff=0.18, color=YELLOW, size=LBL_SZ):
        return Text(txt, font_size=size, color=color).next_to(pos, direction, buff=buff)

    def mk_poly(verts, color=BLUE_D, opacity=0.20):
        return Polygon(
            *verts, color=color, fill_color=color,
            fill_opacity=opacity, stroke_width=1.5,
        ).set_z_index(1)

    def build_hull():
        hull_pts = [PF, PA, PB, PC, PD, PE]
        return VGroup(*[
            mk_seg(hull_pts[i], hull_pts[(i+1) % len(hull_pts)])
            for i in range(len(hull_pts))
        ])

    def build_inner():
        return VGroup(
            mk_seg(Pc, Pa),
            mk_seg(Pa, Pb),
            mk_seg(Pb, Pc),
        )

    def build_dots():
        return VGroup(*[mk_dot(p) for p in
                        [PA, PB, PC, PD, PE, PF, Pc, Pa, Pb]])

    # ── Limpiar escena ────────────────────────────────────────────────────────
    prev = list(scene.mobjects)
    if prev:
        scene.play(*[FadeOut(m) for m in prev], run_time=0.6)

    heading = Text(
        'Teorema 4.1 — Caso 3: B = 4',
        font_size=HEAD_SZ, color=WHITE,
    ).to_corner(UP + LEFT, buff=0.35)
    scene.play(Write(heading))

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 0 — Figura original
    # ════════════════════════════════════════════════════════════════════════
    sub0 = Text('Figura original: 9 puntos', font_size=SUB_SZ, color=GRAY_B)
    sub0.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub0), run_time=0.3)

    hull  = build_hull()
    inner = build_inner()
    dots  = build_dots()

    lbl_A = mk_lbl('A', PA, direction=UP+LEFT,  buff=0.10)
    lbl_B = mk_lbl('B', PB, direction=UP+RIGHT, buff=0.10)
    lbl_C = mk_lbl('C', PC, direction=RIGHT,    buff=0.10)
    lbl_D = mk_lbl('D', PD, direction=DOWN,     buff=0.12)
    lbl_E = mk_lbl('E', PE, direction=DOWN,     buff=0.12)
    lbl_F = mk_lbl('F', PF, direction=LEFT,     buff=0.10)
    lbl_c = mk_lbl('c', Pc, direction=UP+LEFT,  buff=0.10)
    lbl_a = mk_lbl('a', Pa, direction=LEFT,     buff=0.10)
    lbl_b = mk_lbl('b', Pb, direction=RIGHT,    buff=0.10)
    all_labels = VGroup(lbl_A, lbl_B, lbl_C, lbl_D,
                        lbl_E, lbl_F, lbl_c, lbl_a, lbl_b)

    scene.play(Create(hull),       run_time=1.0)
    scene.play(Create(inner),      run_time=0.8)
    scene.play(FadeIn(dots),       run_time=0.4)
    scene.play(FadeIn(all_labels), run_time=0.5)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 1 — Asignación: a=1, b=2, c=3, B=4
    # ════════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(sub0), run_time=0.3)
    sub1 = Text('Asignación: a=1, b=2, c=3, B=4',
                font_size=SUB_SZ, color=GRAY_B)
    sub1.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub1), run_time=0.3)

    seg_l = mk_seg(PB, Pc)
    seg_m = mk_seg(PB, Pb)
    scene.play(Create(seg_l), Create(seg_m), run_time=0.6)

    num1 = mk_num('1', Pa, direction=DOWN+LEFT, buff=0.20, color=YELLOW)
    num2 = mk_num('2', Pb, direction=DOWN+RIGHT,buff=0.20, color=YELLOW)
    num3 = mk_num('3', Pc, direction=UP,        buff=0.20, color=YELLOW)
    num4 = mk_num('4', PB, direction=UP+RIGHT,  buff=0.20, color=ORANGE)

    scene.play(
        FadeIn(num1), FadeOut(lbl_a),
        FadeIn(num2), FadeOut(lbl_b),
        FadeIn(num3), FadeOut(lbl_c),
        FadeIn(num4), FadeOut(lbl_B),
        run_time=0.6,
    )

    note1 = Text(
        'B=4 es el primer punto del hull exterior en la secuencia.',
        font_size=NOTE_SZ, color=GRAY_B,
    ).to_corner(DOWN + LEFT, buff=0.35)
    scene.play(FadeIn(note1), run_time=0.4)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 2 — ¿Por qué F no puede ser el punto 0?
    # Segs: Four–F(n), F–Three(p)
    # Polígono: A–F–Four(B)
    # ════════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(sub1), FadeOut(note1), run_time=0.3)
    sub2 = Text('¿Por qué F no puede ser el punto 0?',
                font_size=SUB_SZ, color=GRAY_B)
    sub2.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub2), run_time=0.3)

    num0_f = mk_num('0', PF, direction=LEFT, buff=0.20, color=GREEN)
    scene.play(FadeIn(num0_f), FadeOut(lbl_F), run_time=0.5)

    seg_n2 = mk_seg(PB, PF, color=WHITE, sw=2.5)
    seg_p2 = mk_seg(PF, Pc, color=WHITE, sw=2.5)
    poly2  = mk_poly([PA, PF, PB])
    seg2_blue = VGroup(
        mk_seg(PA, PF, color=BLUE_D, sw=2.5),
        mk_seg(PF, PB, color=BLUE_D, sw=2.5),
        mk_seg(PB, PA, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(seg_n2), Create(seg_p2), run_time=0.6)
    note2a = Text(
        'Si F=0, debe formar triángulo (0,1,2) con a y b.',
        font_size=NOTE_SZ, color=GRAY_B,
    ).to_corner(DOWN + LEFT, buff=0.55)
    note2b = Text(
        '→ La región (A, F, B) no puede cubrirse.  ✗',
        font_size=NOTE_SZ, color=RED,
    ).next_to(note2a, DOWN, aligned_edge=LEFT, buff=0.08)
    scene.play(FadeIn(note2a), run_time=0.4)
    scene.play(FadeIn(poly2),  run_time=0.5)
    scene.play(Create(seg2_blue), run_time=0.6)
    scene.play(FadeIn(note2b), run_time=0.4)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 3 — ¿Por qué E no puede ser el punto 0?
    # Segs: Four–E(n), E–Three(p)
    # Polígono: Four(B)–A–F–E
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub2),
        FadeOut(num0_f),
        FadeOut(seg_n2), FadeOut(seg_p2),
        FadeOut(poly2),  FadeOut(seg2_blue),
        FadeOut(note2a), FadeOut(note2b),
        run_time=0.4,
    )
    sub3 = Text('¿Por qué E no puede ser el punto 0?',
                font_size=SUB_SZ, color=GRAY_B)
    sub3.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub3), run_time=0.3)

    num0_e = mk_num('0', PE, direction=DOWN, buff=0.20, color=GREEN)
    scene.play(FadeIn(num0_e), FadeOut(lbl_E), run_time=0.5)

    # F vuelve a su label original
    scene.play(FadeIn(lbl_F), run_time=0.3)

    seg_n3 = mk_seg(PB, PE, color=WHITE, sw=2.5)
    seg_p3 = mk_seg(PE, Pc, color=WHITE, sw=2.5)
    poly3  = mk_poly([PB, PA, PF, PE])
    seg3_blue = VGroup(
        mk_seg(PB, PA, color=BLUE_D, sw=2.5),
        mk_seg(PA, PF, color=BLUE_D, sw=2.5),
        mk_seg(PF, PE, color=BLUE_D, sw=2.5),
        mk_seg(PE, PB, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(seg_n3), Create(seg_p3), run_time=0.6)
    note3a = Text(
        'Si E=0, debe formar triángulo (0,1,2) con a y b.',
        font_size=NOTE_SZ, color=GRAY_B,
    ).to_corner(DOWN + LEFT, buff=0.55)
    note3b = Text(
        '→ La región (B, A, F, E) no puede cubrirse.  ✗',
        font_size=NOTE_SZ, color=RED,
    ).next_to(note3a, DOWN, aligned_edge=LEFT, buff=0.08)
    scene.play(FadeIn(note3a), run_time=0.4)
    scene.play(FadeIn(poly3),  run_time=0.5)
    scene.play(Create(seg3_blue), run_time=0.6)
    scene.play(FadeIn(note3b), run_time=0.4)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 4 — A=5 no puede ser el punto 5
    # Seg: A–Three(n)
    # Polígono t1: B–A–F,  Polígono t2: B–A–E
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub3),
        FadeOut(num0_e),
        FadeOut(seg_n3), FadeOut(seg_p3),
        FadeOut(poly3),  FadeOut(seg3_blue),
        FadeOut(note3a), FadeOut(note3b),
        run_time=0.4,
    )
    sub4 = Text('¿Por qué A no puede ser el punto 5?',
                font_size=SUB_SZ, color=GRAY_B)
    sub4.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub4), run_time=0.3)

    # E y F recuperan sus labels; A toma el número 5
    num5_a = mk_num('5', PA, direction=UP+LEFT, buff=0.20, color=GREEN)
    num0_d = mk_num('0', PD, direction=DOWN,    buff=0.20, color=GREEN)  # D es el candidato 0
    scene.play(
        FadeIn(num5_a), FadeOut(lbl_A),
        FadeIn(num0_d), FadeOut(lbl_D),
        FadeIn(lbl_E),
        run_time=0.5,
    )

    seg_n4 = mk_seg(PA, Pc, color=WHITE, sw=2.5)   # A–Three (n)

    poly4_t1 = mk_poly([PB, PA, PF], color=BLUE_D, opacity=0.18)
    seg4_t1  = VGroup(
        mk_seg(PB, PA, color=BLUE_D, sw=2.5),
        mk_seg(PA, PF, color=BLUE_D, sw=2.5),
        mk_seg(PF, PB, color=BLUE_D, sw=2.5),
    )
    poly4_t2 = mk_poly([PB, PA, PE], color=BLUE_D, opacity=0.18)
    seg4_t2  = VGroup(
        mk_seg(PB, PA, color=BLUE_D, sw=2.5),
        mk_seg(PA, PE, color=BLUE_D, sw=2.5),
        mk_seg(PE, PB, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(seg_n4), run_time=0.5)
    scene.play(FadeIn(poly4_t1), FadeIn(poly4_t2), run_time=0.5)
    scene.play(Create(seg4_t1), Create(seg4_t2),   run_time=0.6)

    note4a = Text(
        'Si A=5, las regiones (B,A,F) y (B,A,E) no pueden cubrirse.',
        font_size=NOTE_SZ, color=GRAY_B,
    ).to_corner(DOWN + LEFT, buff=0.55)
    note4b = Text(
        '→ Si B=4, no existe triangulación secuencial.  ✗',
        font_size=NOTE_SZ, color=RED,
    ).next_to(note4a, DOWN, aligned_edge=LEFT, buff=0.08)
    scene.play(FadeIn(note4a), FadeIn(note4b), run_time=0.5)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 5 — Step4: A=6, F=7, One=5
    # Segs nuevos: B–One(m), A–One(n), F–One(p)
    # Polígono: A–F–E
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub4),
        FadeOut(seg_n4),
        FadeOut(poly4_t1), FadeOut(poly4_t2),
        FadeOut(seg4_t1),  FadeOut(seg4_t2),
        FadeOut(note4a),   FadeOut(note4b),
        FadeOut(num0_d),
        run_time=0.4,
    )
    sub5 = Text('Continuación: A=6, F=7',
                font_size=SUB_SZ, color=GRAY_B)
    sub5.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub5), run_time=0.3)

    num6 = mk_num('6', PA, direction=UP+LEFT, buff=0.20, color=GREEN)
    num7 = mk_num('7', PF, direction=LEFT,    buff=0.20, color=GREEN)

    # num1 (=1 sobre a) sigue en escena; One toma también rol de 5
    num5_one = mk_num('5', Pa, direction=DOWN, buff=0.20, color=GREEN)

    scene.play(
        FadeIn(num6),     FadeOut(num5_a),
        FadeIn(num7),     FadeOut(lbl_F),
        FadeIn(num5_one),
        run_time=0.5,
    )

    seg_m5 = mk_seg(PB, Pa, color=WHITE, sw=2.5)   # B–One (m)
    seg_n5 = mk_seg(PA, Pa, color=WHITE, sw=2.5)   # A–One (n)
    seg_p5 = mk_seg(PF, Pa, color=WHITE, sw=2.5)   # F–One (p)
    scene.play(Create(seg_m5), Create(seg_n5), Create(seg_p5), run_time=0.7)

    poly5  = mk_poly([PA, PF, PE])
    seg5_blue = VGroup(
        mk_seg(PA, PF, color=BLUE_D, sw=2.5),
        mk_seg(PF, PE, color=BLUE_D, sw=2.5),
        mk_seg(PE, PA, color=BLUE_D, sw=2.5),
    )
    scene.play(FadeIn(poly5),     run_time=0.5)
    scene.play(Create(seg5_blue), run_time=0.6)

    note5a = Text(
        'La región (A, F, E) no puede cubrirse.',
        font_size=NOTE_SZ, color=GRAY_B,
    ).to_corner(DOWN + LEFT, buff=0.55)
    note5b = Text(
        '→ La secuencia no puede completarse.  ✗',
        font_size=NOTE_SZ, color=RED,
    ).next_to(note5a, DOWN, aligned_edge=LEFT, buff=0.08)
    scene.play(FadeIn(note5a), FadeIn(note5b), run_time=0.5)

    scene.next_slide()

    return {'heading': heading}


class SimpleSlides(Slide):
    def construct(self):
        self.camera.background_color = BLACK
        ctx = title_slide(self, {})
        self.next_slide()
        ctx = holes_slide(self, ctx)
        self.next_slide()
        ctx = paper_slide(self, ctx)
        self.next_slide()
