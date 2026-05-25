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

    PA  = pt(25, 40)   # A
    PB  = pt(35, 40)   # B
    PC  = pt(55, 10)   # C
    PD  = pt(50,  5)   # D  (antes Four)
    PE  = pt(10,  5)   # E
    PF  = pt( 5, 10)   # F
    Pc  = pt(30, 25)   # c  (antes Three)
    Pa  = pt(25, 15)   # a  (antes One)
    Pb  = pt(35, 15)   # b  (antes Two)

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
        'Teorema 4.1 — Caso 1: D = 4',
        font_size=HEAD_SZ, color=WHITE,
    ).to_corner(UP + LEFT, buff=0.35)
    scene.play(Write(heading))

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 0 — Figura original con letras del paper
    # One→a, Two→b, Three→c; hull: A,B,C,D,E,F
    # ════════════════════════════════════════════════════════════════════════
    sub0 = Text('Figura original: 9 puntos', font_size=SUB_SZ, color=GRAY_B)
    sub0.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub0), run_time=0.3)

    hull  = build_hull()
    inner = build_inner()
    dots  = build_dots()

    # Labels individuales (figura original con letras del paper)
    lbl_A0 = mk_lbl('A', PA, direction=UP+LEFT,  buff=0.10)
    lbl_B0 = mk_lbl('B', PB, direction=UP+RIGHT, buff=0.10)
    lbl_C0 = mk_lbl('C', PC, direction=RIGHT,    buff=0.10)
    lbl_D0 = mk_lbl('D', PD, direction=DOWN,     buff=0.12)
    lbl_E0 = mk_lbl('E', PE, direction=DOWN,     buff=0.12)
    lbl_F0 = mk_lbl('F', PF, direction=LEFT,     buff=0.10)
    lbl_c0 = mk_lbl('c', Pc, direction=UP+LEFT,  buff=0.10)
    lbl_a0 = mk_lbl('a', Pa, direction=LEFT,     buff=0.10)
    lbl_b0 = mk_lbl('b', Pb, direction=RIGHT,    buff=0.10)
    all_labels0 = VGroup(lbl_A0, lbl_B0, lbl_C0, lbl_D0,
                         lbl_E0, lbl_F0, lbl_c0, lbl_a0, lbl_b0)

    scene.play(Create(hull), run_time=1.0)
    scene.play(Create(inner), run_time=0.8)
    scene.play(FadeIn(dots), run_time=0.4)
    scene.play(FadeIn(all_labels0), run_time=0.5)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 1 — Case1Start: numeración 1–4
    # Renombramos a→One, b→Two, c→Three para la narrativa del caso
    # Al poner el número desaparece el label de letra
    # ════════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(sub0), run_time=0.3)
    sub1 = Text('Asignación: a=1, b=2, c=3, D=4',
                font_size=SUB_SZ, color=GRAY_B)
    sub1.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub1), run_time=0.3)

    seg_l = mk_seg(PD, Pb)   # D–b
    seg_m = mk_seg(PD, Pc)   # D–c
    scene.play(Create(seg_l), Create(seg_m), run_time=0.6)

    num1 = mk_num('1', Pa, direction=DOWN+LEFT, buff=0.20, color=YELLOW)
    num2 = mk_num('2', Pb, direction=DOWN+RIGHT,buff=0.20, color=YELLOW)
    num3 = mk_num('3', Pc, direction=UP,        buff=0.20, color=YELLOW)
    num4 = mk_num('4', PD, direction=DOWN,      buff=0.22, color=ORANGE)

    scene.play(
        FadeIn(num1),  FadeOut(lbl_a0),
        FadeIn(num2),  FadeOut(lbl_b0),
        FadeIn(num3),  FadeOut(lbl_c0),
        FadeIn(num4),  FadeOut(lbl_D0), run_time=0.6)


    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 2 — ¿Por qué E no puede ser el punto 0?
    # ════════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(sub1), run_time=0.3)
    sub2 = Text('¿Por qué E no puede ser el punto 0?',
                font_size=SUB_SZ, color=GRAY_B)
    sub2.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub2), run_time=0.3)

    dash_n2 = mk_dash(PE, Pa)   # E–a
    dash_p2 = mk_dash(PE, Pb)   # E–b
    poly2   = mk_poly([Pb, PE, PD])
    seg2_blue = VGroup(
        mk_seg(Pb,  PE, color=BLUE_D, sw=2.5),
        mk_seg(PD,  Pb, color=BLUE_D, sw=2.5),
        mk_seg(PE,  PD, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(dash_n2), Create(dash_p2), run_time=0.7)
    scene.play(FadeIn(poly2), run_time=0.5)
    scene.play(Create(seg2_blue), run_time=0.6)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 3 — Candidatos para el punto 5
    # A, B, C se renombran → sus labels desaparecen
    # Dashed D–a se dibuja y permanece en slides siguientes
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub2),
        FadeOut(dash_n2), FadeOut(dash_p2),
        FadeOut(poly2),   FadeOut(seg2_blue), run_time=0.4)
    sub3 = Text('Candidatos para el punto 5',
                font_size=SUB_SZ, color=GRAY_B)
    sub3.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub3), run_time=0.3)

    dash_d_a = mk_dash(PD, Pa)   # D–a, permanece hasta el final
    scene.play(Create(dash_d_a), run_time=0.5)

    lbl_fc2 = mk_lbl('FiveCand₂', PA, direction=UP+LEFT,  buff=0.10, color=ORANGE)
    lbl_fc1 = mk_lbl('FiveCand₁', PB, direction=UP+RIGHT, buff=0.10, color=ORANGE)
    lbl_fc  = mk_lbl('FiveCand',  PC, direction=RIGHT,    buff=0.10, color=ORANGE)

    scene.play(
        FadeIn(lbl_fc2), FadeOut(lbl_A0),
        FadeIn(lbl_fc1), FadeOut(lbl_B0),
        FadeIn(lbl_fc),  FadeOut(lbl_C0), run_time=0.5)


    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 4 — FiveCand₁=B no puede ser 5
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub3), run_time=0.4)
    sub4 = Text('¿Por qué FiveCand₁=B no puede ser el punto 5?',
                font_size=SUB_SZ, color=GRAY_B)
    sub4.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub4), run_time=0.3)

    num5_b    = mk_num('5', PB, direction=UP+RIGHT, buff=0.20, color=GREEN)
    lbl_sc_a  = mk_lbl('SixCand',  PA, direction=UP+LEFT,  buff=0.10, color=ORANGE)
    lbl_sc1_c = mk_lbl('SixCand₁', PC, direction=RIGHT,    buff=0.10, color=ORANGE)

    scene.play(
        FadeIn(num5_b),    FadeOut(lbl_fc1),
        FadeIn(lbl_sc_a),  FadeOut(lbl_fc2),
        FadeIn(lbl_sc1_c), FadeOut(lbl_fc), run_time=0.5)

    seg_p4  = mk_seg(PD, PB,  color=WHITE, sw=2.5)   # D–B
    seg_q4  = mk_seg(Pc, PB,  color=WHITE, sw=2.5)   # c–B
    poly4   = mk_poly([PB, PD, PC])
    seg4_blue = VGroup(
        mk_seg(PB, PD, color=BLUE_D, sw=2.5),
        mk_seg(PD, PC, color=BLUE_D, sw=2.5),
        mk_seg(PC, PB, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(seg_p4), Create(seg_q4), run_time=0.6)
    scene.play(FadeIn(poly4), run_time=0.4)
    scene.play(Create(seg4_blue), run_time=0.6)


    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 5 — FiveCand₂=A no puede ser 5
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub4),
        FadeOut(seg_p4),  FadeOut(seg_q4),
        FadeOut(poly4),   FadeOut(seg4_blue), run_time=0.4)
    sub5 = Text('¿Por qué FiveCand₂=A no puede ser el punto 5?',
                font_size=SUB_SZ, color=GRAY_B)
    sub5.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub5), run_time=0.3)

    num5_a    = mk_num('5', PA, direction=UP+LEFT,  buff=0.20, color=GREEN)
    lbl_sc5_b = mk_lbl('SixCand',  PB, direction=UP+RIGHT, buff=0.10, color=ORANGE)
    lbl_sc5_c = mk_lbl('SixCand₁', PC, direction=RIGHT,    buff=0.10, color=ORANGE)

    scene.play(
        FadeIn(num5_a),    FadeOut(lbl_sc_a),
        FadeIn(lbl_sc5_b), FadeOut(num5_b),
        FadeIn(lbl_sc5_c), FadeOut(lbl_sc1_c), run_time=0.5)

    seg_p5  = mk_seg(PA, Pc,  color=WHITE, sw=2.5)   # A–c
    seg_q5  = mk_seg(PA, PD,  color=WHITE, sw=2.5)   # A–D
    poly5   = mk_poly([PD, PA, PB, PC])
    seg5_blue = VGroup(
        mk_seg(PD, PA, color=BLUE_D, sw=2.5),
        mk_seg(PA, PB, color=BLUE_D, sw=2.5),
        mk_seg(PB, PC, color=BLUE_D, sw=2.5),
        mk_seg(PC, PD, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(seg_p5), Create(seg_q5), run_time=0.6)
    scene.play(FadeIn(poly5), run_time=0.4)
    scene.play(Create(seg5_blue), run_time=0.6)


    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 6 — FiveCand=C no puede ser 5, conclusión
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub5),
        FadeOut(seg_p5),  FadeOut(seg_q5),
        FadeOut(poly5),   FadeOut(seg5_blue), run_time=0.4)
    sub6 = Text('Conclusión Caso 1: ningún candidato a 5 es válido',
                font_size=SUB_SZ, color=GRAY_B)
    sub6.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub6), run_time=0.3)

    num5_c    = mk_num('5', PC, direction=RIGHT,   buff=0.22, color=GREEN)
    lbl_sc6_a = mk_lbl('SixCand₁', PA, direction=UP+LEFT, buff=0.10, color=ORANGE)

    scene.play(
        FadeIn(num5_c),    FadeOut(lbl_sc5_c),
        FadeIn(lbl_sc6_a), FadeOut(num5_a), run_time=0.5)

    seg_p6   = mk_seg(PC, Pc, color=WHITE, sw=2.5)   # C–c
    poly6_t1 = mk_poly([PD, PC, PB], color=BLUE_D, opacity=0.18)
    poly6_t2 = mk_poly([PD, PC, PA], color=BLUE_D, opacity=0.18)
    seg6_blue = VGroup(
        mk_seg(PC, PB, color=BLUE_D, sw=2.5),
        mk_seg(PB, PD, color=BLUE_D, sw=2.5),
        mk_seg(PD, PC, color=BLUE_D, sw=2.5),
        mk_seg(PC, PA, color=BLUE_D, sw=2.5),
        mk_seg(PA, PD, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(seg_p6), run_time=0.5)
    scene.play(FadeIn(poly6_t1), FadeIn(poly6_t2), run_time=0.5)
    scene.play(Create(seg6_blue), run_time=0.6)

    conc1 = Text(
        'Los 3 candidatos a 5 (A, B, C) generan regiones imposibles.',
        font_size=NOTE_SZ, color=WHITE,
    ).to_corner(DOWN + LEFT, buff=0.65)
    conc2 = Text(
        '→ Si D=4, no existe triangulación secuencial.  ✗',
        font_size=NOTE_SZ, color=RED,
    ).next_to(conc1, DOWN, aligned_edge=LEFT, buff=0.08)
    scene.play(FadeIn(conc1), FadeIn(conc2), run_time=0.6)

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
