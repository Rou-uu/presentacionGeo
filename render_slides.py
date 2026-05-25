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
        Text, Line, Dot, DashedLine, VGroup, Group,
        Write, FadeIn, FadeOut, Create,
        WHITE, YELLOW, GRAY_B, BLUE_C,
        UP, DOWN, LEFT, RIGHT, ORIGIN,
    )

    # ═══════════════════════════════════════════════════════
    # Mapeo GeoGebra → Manim
    # ═══════════════════════════════════════════════════════
    CX, CY = 10.4, 4.7
    SX, SY = 0.7, 1.0

    def gp(x, y):
        return np.array([(x - CX) * SX, (y - CY) * SY, 0.0])

    # --- Coordenadas del GeoGebra ---
    PA = gp(10.0000, 7.0000)
    PB = gp(10.0000, 6.0000)
    PC = gp(6.0695, 6.7973)
    PD = gp(7.4498, 5.1809)
    PE = gp(7.9402, 4.2546)
    PF = gp(12.6262, 4.5815)
    PG = gp(13.0802, 5.5441)
    PH = gp(5.6517, 6.0164)
    PI = gp(7.2863, 4.4544)
    PJ = gp(5.8878, 3.1285)
    PK = gp(3.1816, 3.4736)
    PL = gp(6.2692, 2.3293)
    PM = gp(3.1089, 2.7471)
    PN = gp(3.4904, 5.5804)
    PO = gp(3.4177, 6.3978)
    PP = gp(13.4072, 4.7631)
    PQ = gp(14.9510, 6.2706)
    PR = gp(16.5130, 5.9619)
    PS = gp(14.9691, 3.4917)
    PT = gp(17.5846, 3.5099)
    PU = gp(14.8057, 2.8742)
    PV = gp(17.6754, 2.8016)
    PW = gp(14.7149, 7.1243)
    PZ = gp(16.4766, 6.8882)

    # --- Gráfica cúbica original (inferida de node vertices) ---
    NODE_L = (PD + PE + PH) / 3
    NODE_R = (PF + PG + PP) / 3
    END_TL = (PO + PN) / 2
    END_BL = (PK + PM) / 2
    END_TR = (PR + PZ) / 2
    END_BR = (PT + PV) / 2

    # ═══════════════════════════════════════════════════════
    # Estilos
    # ═══════════════════════════════════════════════════════
    CLR_FORCED = YELLOW
    CLR_OTHER = GRAY_B
    CLR_LABEL = BLUE_C
    SW = 2.5
    SW_D = 2.0
    RN = 0.10
    RS = 0.07

    def mk_dot(pos, r=RS):
        return Dot(pos, radius=r, color=WHITE).set_z_index(2)

    def mk_line(a, b, sw=SW):
        return Line(a, b, color=WHITE, stroke_width=sw)

    def mk_label(txt, pos, off):
        return Text(txt, font_size=14, color=CLR_LABEL).move_to(pos + off)

    # ═══════════════════════════════════════════════════════
    # Fade out slide anterior
    # ═══════════════════════════════════════════════════════
    all_prev = [v for v in ctx.values() if v is not None]
    if all_prev:
        scene.play(*[FadeOut(obj) for obj in all_prev])

    heading = Text("Ejemplo de la reducción", font_size=30, color=WHITE)
    heading.to_corner(UP + LEFT, buff=0.4)
    scene.play(Write(heading))

    # ════════════════════════════════════════════════════════
    # SLIDE 1 — Gráfica cúbica original G
    # ════════════════════════════════════════════════════════
    sub1 = Text("Gráfica cúbica G", font_size=20, color=GRAY_B)
    sub1.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.12)
    scene.play(FadeIn(sub1), run_time=0.4)

    orig_edges = VGroup(
        mk_line(NODE_L, NODE_R, 3),
        mk_line(NODE_L, END_TL, 3),
        mk_line(NODE_L, END_BL, 3),
        mk_line(NODE_R, END_TR, 3),
        mk_line(NODE_R, END_BR, 3),
    )
    orig_dots = VGroup(
        mk_dot(NODE_L, RN), mk_dot(NODE_R, RN),
        mk_dot(END_TL), mk_dot(END_BL),
        mk_dot(END_TR), mk_dot(END_BR),
    )

    scene.play(
        *[Create(e) for e in orig_edges],
        *[FadeIn(d) for d in orig_dots],
        run_time=1.5,
    )
    scene.next_slide()

    # ════════════════════════════════════════════════════════
    # SLIDE 2 — Nodos explotan en node vertices
    # ════════════════════════════════════════════════════════
    scene.play(FadeOut(sub1), run_time=0.3)
    sub2 = Text("Nodos -> vertices", font_size=20, color=GRAY_B)
    sub2.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.12)
    scene.play(FadeIn(sub2), run_time=0.4)

    left_nvs = [PD, PE, PH]
    right_nvs = [PF, PG, PP]

    dLv = [mk_dot(NODE_L) for _ in range(3)]
    dRv = [mk_dot(NODE_R) for _ in range(3)]
    for d in dLv + dRv:
        scene.add(d)

    scene.play(
        FadeOut(orig_dots[0]), FadeOut(orig_dots[1]),
        *[dLv[i].animate.move_to(left_nvs[i]) for i in range(3)],
        *[dRv[i].animate.move_to(right_nvs[i]) for i in range(3)],
        run_time=1.5,
    )

    nv_labels = VGroup(
        mk_label("D", PD, UP * 0.18 + LEFT * 0.12),
        mk_label("E", PE, DOWN * 0.18 + LEFT * 0.12),
        mk_label("H", PH, LEFT * 0.2),
        mk_label("F", PF, DOWN * 0.18 + RIGHT * 0.12),
        mk_label("G", PG, UP * 0.18 + RIGHT * 0.12),
        mk_label("P", PP, RIGHT * 0.2),
    )
    scene.play(FadeIn(nv_labels), run_time=0.6)
    scene.next_slide()

    # ════════════════════════════════════════════════════════
    # SLIDE 3 — Aristas → paredes de túnel + arc vertices
    # ════════════════════════════════════════════════════════
    scene.play(FadeOut(sub2), run_time=0.3)
    sub3 = Text("Aristas -> túneles en V", font_size=20, color=GRAY_B)
    sub3.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.12)
    scene.play(FadeIn(sub3), run_time=0.4)

    scene.play(
        *[FadeOut(e) for e in orig_edges],
        *[FadeOut(orig_dots[i]) for i in range(2, 6)],
        run_time=0.8,
    )

    # --- Paredes por túnel ---
    w_central = VGroup(
        mk_line(PA, PD), mk_line(PE, PB),
        mk_line(PB, PF), mk_line(PA, PG),
    )
    w_tl = VGroup(
        mk_line(PD, PC), mk_line(PC, PO), mk_line(PH, PN),
    )
    w_bl = VGroup(
        mk_line(PH, PI), mk_line(PI, PJ), mk_line(PJ, PK),
        mk_line(PE, PL), mk_line(PL, PM),
    )
    w_tr = VGroup(
        mk_line(PG, PW), mk_line(PW, PZ),
        mk_line(PP, PQ), mk_line(PQ, PR),
    )
    w_br = VGroup(
        mk_line(PP, PS), mk_line(PS, PT),
        mk_line(PF, PU), mk_line(PU, PV),
    )

    # --- Arc vertices ---
    arc_info = [
        ("A", PA, UP * 0.18 + LEFT * 0.05),
        ("B", PB, DOWN * 0.18 + LEFT * 0.05),
        ("C", PC, UP * 0.15 + LEFT * 0.1),
        ("I", PI, DOWN * 0.18 + LEFT * 0.1),
        ("L", PL, DOWN * 0.18),
        ("W", PW, UP * 0.15 + LEFT * 0.1),
        ("Q", PQ, UP * 0.15 + RIGHT * 0.1),
        ("S", PS, DOWN * 0.15 + LEFT * 0.1),
        ("U", PU, DOWN * 0.18),
    ]
    arc_dots = VGroup(*[mk_dot(pos) for _, pos, _ in arc_info])
    arc_lbls = VGroup(*[mk_label(n, p, o) for n, p, o in arc_info])

    # --- Endpoints ---
    ep_info = [
        ("O", PO, UP * 0.15), ("N", PN, LEFT * 0.2),
        ("K", PK, LEFT * 0.2), ("M", PM, LEFT * 0.2),
        ("J", PJ, LEFT * 0.2), ("Z", PZ, UP * 0.15),
        ("R", PR, RIGHT * 0.2), ("T", PT, RIGHT * 0.2),
        ("V", PV, RIGHT * 0.2),
    ]
    ep_dots = VGroup(*[mk_dot(pos) for _, pos, _ in ep_info])
    ep_lbls = VGroup(*[mk_label(n, p, o) for n, p, o in ep_info])

    # Animar por grupo
    scene.play(Create(w_central), run_time=1.0)
    scene.play(FadeIn(arc_dots[0:2]), FadeIn(arc_lbls[0:2]), run_time=0.5)

    scene.play(Create(w_tl), run_time=0.8)
    scene.play(FadeIn(arc_dots[2]), FadeIn(arc_lbls[2]), run_time=0.4)

    scene.play(Create(w_bl), run_time=0.8)
    scene.play(FadeIn(arc_dots[3:5]), FadeIn(arc_lbls[3:5]), run_time=0.4)

    scene.play(Create(w_tr), run_time=0.8)
    scene.play(FadeIn(arc_dots[5:7]), FadeIn(arc_lbls[5:7]), run_time=0.4)

    scene.play(Create(w_br), run_time=0.8)
    scene.play(FadeIn(arc_dots[7:9]), FadeIn(arc_lbls[7:9]), run_time=0.4)

    scene.play(FadeIn(ep_dots), FadeIn(ep_lbls), run_time=0.6)
    scene.next_slide()

    # ════════════════════════════════════════════════════════
    # SLIDE 4 — Diagonales forzadas (sólidas, amarillas)
    # ════════════════════════════════════════════════════════
    scene.play(FadeOut(sub3), run_time=0.3)
    sub4 = Text("Diagonales forzadas y otras diagonales", font_size=20, color=GRAY_B)
    sub4.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.12)
    scene.play(FadeIn(sub4), run_time=0.4)

    forced_diags = VGroup(
        Line(PA, PB, color=CLR_FORCED, stroke_width=SW_D).set_z_index(3),
        Line(PH, PC, color=CLR_FORCED, stroke_width=SW_D).set_z_index(3),
        Line(PJ, PL, color=CLR_FORCED, stroke_width=SW_D).set_z_index(3),
        Line(PW, PQ, color=CLR_FORCED, stroke_width=SW_D).set_z_index(3),
        Line(PS, PU, color=CLR_FORCED, stroke_width=SW_D).set_z_index(3),
    )
    scene.play(Create(forced_diags), run_time=1.5)
    scene.next_slide()

    # ════════════════════════════════════════════════════════
    # SLIDE 5 — Otras diagonales (punteadas)
    # ════════════════════════════════════════════════════════
    other_pairs = [
        (PA, PI), (PI, PB), (PA, PP), (PB, PP),
        (PI, PC), (PI, PL), (PI, PE), (PI, PD),
        (PF, PP), (PG, PP), (PW, PP), (PP, PU),
    ]
    other_diags = VGroup(*[
        DashedLine(s, e, color=CLR_OTHER, stroke_width=SW_D,
                   dash_length=0.10).set_z_index(2)
        for s, e in other_pairs
    ])
    scene.play(Create(other_diags), run_time=1.5)

    # Leyenda
    leg_f = VGroup(
        Line(ORIGIN, RIGHT * 0.5, color=CLR_FORCED, stroke_width=3),
        Text("── diagonales forzadas", font_size=14, color=CLR_FORCED),
    ).arrange(RIGHT, buff=0.12)
    leg_o = VGroup(
        DashedLine(ORIGIN, RIGHT * 0.5, color=CLR_OTHER,
                   stroke_width=2, dash_length=0.08),
        Text("╌╌ otras diagonales", font_size=14, color=CLR_OTHER),
    ).arrange(RIGHT, buff=0.12)
    legend = VGroup(leg_f, leg_o).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    legend.to_corner(DOWN + RIGHT, buff=0.35)
    scene.play(FadeIn(legend), run_time=0.6)
    scene.next_slide()

    # ═══════════════════════════════════════════════════════
    # Retornar contexto para el siguiente slide
    # ═══════════════════════════════════════════════════════
    return {
        "heading": heading,
        "all_objs": None,
    }


def example_paper(scene, ctx):
    import numpy as np
    from manim import (
        Text, Line, Dot, DashedLine, VGroup,
        Write, FadeIn, FadeOut, Create,
        WHITE, YELLOW, GRAY_B, BLUE_C, RED,
        UP, DOWN, LEFT, RIGHT, ORIGIN,
    )

    TEAL = '#006758'
    FORCED_CLR = YELLOW
    OTHER_CLR = GRAY_B

    def mk_dot(pos, r=0.04):
        return Dot(pos, radius=r, color=WHITE).set_z_index(2)

    def mk_line(a, b, sw=1.8, color=WHITE):
        return Line(a, b, color=color, stroke_width=sw)

    def gp3(x, y):
        return np.array([(x - 7.5) * 0.55, (y - 5.5) * 0.55 - 0.3, 0.0])

    def gp(x, y):
        return np.array([(x - 26.0) * 0.214, (y - 15.5) * 0.214 - 0.3, 0.0])

    # ═══ Puntos Q₃ ═══
    ORIG_A = gp3(6.0, 7.0)
    ORIG_B = gp3(6.0, 4.0)
    ORIG_C = gp3(9.0, 4.0)
    ORIG_D = gp3(9.0, 7.0)
    ORIG_E = gp3(2.0, 11.0)
    ORIG_F = gp3(13.0, 11.0)
    ORIG_G = gp3(13.0, 0.0)
    ORIG_H = gp3(2.0, 0.0)

    # ═══ Puntos reducción ═══
    PA1 = gp(29.4943, 11.6206)
    PA2 = gp(30.1718, 22.2688)
    PB1 = gp(31.0032, 13.1295)
    PB2 = gp(30.8275, 21.2678)
    PC1 = gp(24.6332, 17.8934)
    PC2 = gp(34.0, 16.0)
    PD1 = gp(23.5544, 17.1011)
    PD2 = gp(31.6077, 15.943)
    PE1 = gp(24.3679, 16.4109)
    PE2 = gp(34.4746, 11.604)
    PF1 = gp(28.8523, 19.5134)
    PF2 = gp(33.5037, 10.8878)
    PG1 = gp(28.8135, 17.4565)
    PG2 = gp(26.685, 7.3888)
    PH1 = gp(30.5211, 18.4267)
    PH2 = gp(26.6921, 9.1202)
    PI = gp(33.8054, 6.8569)
    PI1 = gp(40.0, 16.0)
    PJ = gp(34.4737, 5.9515)
    PJ1 = gp(38.3941, 15.9672)
    PK = gp(35.0341, 8.4304)
    PK1 = gp(26.6123, 2.6169)
    PL = gp(35.1005, 23.2002)
    PL1 = gp(26.4938, 3.5416)
    PM = gp(36.3393, 25.3637)
    PM1 = gp(12.0, 16.0)
    PN = gp(33.8975, 24.8302)
    PN1 = gp(14.0, 16.0)
    PO = gp(21.0043, 23.2723)
    PO1 = gp(27.035, 28.2966)
    PP = gp(19.068, 22.5982)
    PP1 = gp(27.035, 26.4762)
    PQ = gp(18.4517, 23.954)
    PQ1 = gp(19.3638, 12.4175)
    PR = gp(18.7395, 7.6245)
    PR1 = gp(20.3005, 11.5794)
    PS = gp(19.9452, 6.6629)
    PS1 = gp(24.1701, 20.9219)
    PT = gp(19.0998, 5.6427)
    PT1 = gp(23.3165, 19.9023)
    PU = gp(23.3079, 13.1942)
    PU1 = gp(19.0011, 16.0611)
    PV = gp(24.0, 12.0)
    PV1 = gp(21.2536, 15.658)
    PW = gp(25.3341, 13.0864)
    PW1 = gp(27.1835, 22.23)
    PZ = gp(28.8692, 12.6769)
    PZ1 = gp(27.0671, 20.2895)

    # ═══ Puntos dual ═══
    D_PA = gp(18.1617, 22.9073)
    D_PA3 = gp(20.596, 24.5953)
    D_PA4 = gp(25.1322, 12.1194)
    D_PB = gp(13.6198, 16.7384)
    D_PB3 = gp(20.4183, 23.4581)
    D_PB4 = gp(24.2093, 12.5018)
    D_PC = gp(13.2751, 15.5465)
    D_PC3 = gp(23.0, 21.0)
    D_PC4 = gp(20.2557, 12.1842)
    D_PD = gp(18.2861, 7.342)
    D_PD3 = gp(19.5299, 22.7118)
    D_PD4 = gp(23.6701, 13.7456)
    D_PE = gp(19.6246, 6.772)
    D_PE3 = gp(23.8287, 19.6616)
    D_PE4 = gp(23.2463, 13.0828)
    D_PF = gp(19.7609, 11.2511)
    D_PF3 = gp(23.7406, 17.6498)
    D_PF4 = gp(20.8451, 15.3102)
    D_PG = gp(18.8225, 7.9352)
    D_PG3 = gp(24.4861, 18.2631)
    D_PG4 = gp(21.0624, 16.2663)
    D_PH = gp(19.7076, 5.725)
    D_PH3 = gp(24.9154, 17.6351)
    D_PH4 = gp(23.6848, 16.4653)
    D_PI2 = gp(26.0576, 3.3263)
    D_PI3 = gp(26.7142, 20.9526)
    D_PJ2 = gp(27.0502, 3.3072)
    D_PJ3 = gp(27.4393, 20.913)
    D_PK2 = gp(33.727, 5.9027)
    D_PK3 = gp(28.3094, 19.0146)
    D_PL2 = gp(33.8691, 7.2353)
    D_PL3 = gp(29.0734, 19.2447)
    D_PM2 = gp(34.0, 10.0)
    D_PM3 = gp(30.1552, 20.9394)
    D_PN2 = gp(34.7043, 8.337)
    D_PN3 = gp(30.0629, 18.8168)
    D_PO2 = gp(35.1819, 7.7913)
    D_PO3 = gp(30.0233, 17.5248)
    D_PP2 = gp(38.8453, 15.3686)
    D_PP3 = gp(32.4755, 16.4569)
    D_PQ2 = gp(39.0, 17.0)
    D_PQ3 = gp(32.2118, 15.4286)
    D_PR2 = gp(36.0, 23.0)
    D_PR3 = gp(30.4057, 13.5696)
    D_PS2 = gp(34.8287, 23.6891)
    D_PS3 = gp(30.7347, 12.706)
    D_PT2 = gp(31.3638, 22.2143)
    D_PT3 = gp(33.5302, 11.5262)
    D_PU2 = gp(33.9402, 24.4531)
    D_PU3 = gp(30.2475, 11.8294)
    D_PV2 = gp(34.7753, 25.4304)
    D_PV3 = gp(28.6918, 11.6184)
    D_PW2 = gp(28.0, 27.0)
    D_PW3 = gp(26.9779, 8.5071)
    D_PZ2 = gp(26.2286, 27.0118)
    D_PZ3 = gp(26.1737, 8.9817)

    all_prev = [m for m in scene.mobjects]
    if all_prev:
        scene.play(*[FadeOut(m) for m in all_prev], run_time=0.8)

    heading = Text('Ejemplo: reducción sobre Q₃', font_size=28, color=WHITE)
    heading.to_corner(UP + LEFT, buff=0.35)
    scene.play(Write(heading))

    # ════ SLIDE 1: Q₃ ════
    sub = Text('Grafo cúbico Q₃', font_size=18, color=GRAY_B)
    sub.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.1)
    scene.play(FadeIn(sub), run_time=0.4)

    orig_edges = VGroup(
        mk_line(ORIG_A, ORIG_B, sw=2.5),
        mk_line(ORIG_B, ORIG_C, sw=2.5),
        mk_line(ORIG_C, ORIG_D, sw=2.5),
        mk_line(ORIG_D, ORIG_A, sw=2.5),
        mk_line(ORIG_E, ORIG_F, sw=2.5),
        mk_line(ORIG_F, ORIG_G, sw=2.5),
        mk_line(ORIG_G, ORIG_H, sw=2.5),
        mk_line(ORIG_H, ORIG_E, sw=2.5),
        mk_line(ORIG_A, ORIG_E, sw=2.5),
        mk_line(ORIG_D, ORIG_F, sw=2.5),
        mk_line(ORIG_C, ORIG_G, sw=2.5),
        mk_line(ORIG_B, ORIG_H, sw=2.5),
    )
    orig_dots = VGroup(
        mk_dot(ORIG_A, r=0.07),
        mk_dot(ORIG_B, r=0.07),
        mk_dot(ORIG_C, r=0.07),
        mk_dot(ORIG_D, r=0.07),
        mk_dot(ORIG_E, r=0.07),
        mk_dot(ORIG_F, r=0.07),
        mk_dot(ORIG_G, r=0.07),
        mk_dot(ORIG_H, r=0.07),
    )
    orig_labels = VGroup(
        Text('A', font_size=13, color=BLUE_C).next_to(ORIG_A, UP, buff=0.06),
        Text('B', font_size=13, color=BLUE_C).next_to(ORIG_B, UP, buff=0.06),
        Text('C', font_size=13, color=BLUE_C).next_to(ORIG_C, UP, buff=0.06),
        Text('D', font_size=13, color=BLUE_C).next_to(ORIG_D, UP, buff=0.06),
        Text('E', font_size=13, color=BLUE_C).next_to(ORIG_E, UP, buff=0.06),
        Text('F', font_size=13, color=BLUE_C).next_to(ORIG_F, UP, buff=0.06),
        Text('G', font_size=13, color=BLUE_C).next_to(ORIG_G, UP, buff=0.06),
        Text('H', font_size=13, color=BLUE_C).next_to(ORIG_H, UP, buff=0.06),
    )
    scene.play(*[Create(e) for e in orig_edges], *[FadeIn(d) for d in orig_dots], run_time=1.5)
    scene.play(FadeIn(orig_labels), run_time=0.5)
    scene.next_slide()

    # ════ SLIDE 2: Polígono reducido ════
    scene.play(FadeOut(sub), run_time=0.3)
    sub2 = Text('Polígono con hoyos (paredes de túnel)', font_size=18, color=GRAY_B)
    sub2.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.1)
    scene.play(FadeIn(sub2), run_time=0.4)
    scene.play(FadeOut(orig_edges), FadeOut(orig_dots), FadeOut(orig_labels), run_time=0.8)

    tunnel_walls = VGroup(
        mk_line(PM, PI1),
        mk_line(PI1, PJ),
        mk_line(PK, PJ1),
        mk_line(PL, PJ1),
        mk_line(PK1, PJ),
        mk_line(PL1, PI),
        mk_line(PK1, PT),
        mk_line(PL1, PS),
        mk_line(PT, PM1),
        mk_line(PR, PN1),
        mk_line(PM1, PQ),
        mk_line(PN1, PP),
        mk_line(PQ, PO1),
        mk_line(PO1, PM),
        mk_line(PO, PP1),
        mk_line(PP1, PN),
        mk_line(PR, PQ1),
        mk_line(PQ1, PU),
        mk_line(PS, PR1),
        mk_line(PR1, PV),
        mk_line(PO, PS1),
        mk_line(PS1, PC1),
        mk_line(PP, PT1),
        mk_line(PT1, PD1),
        mk_line(PD1, PU1),
        mk_line(PU1, PU),
        mk_line(PE1, PV1),
        mk_line(PV1, PW),
        mk_line(PC1, PW1),
        mk_line(PW1, PF1),
        mk_line(PE1, PZ1),
        mk_line(PZ1, PG1),
        mk_line(PF1, PA2),
        mk_line(PA2, PN),
        mk_line(PH1, PB2),
        mk_line(PB2, PL),
        mk_line(PH1, PC2),
        mk_line(PC2, PB1),
        mk_line(PG1, PD2),
        mk_line(PD2, PZ),
        mk_line(PB1, PE2),
        mk_line(PE2, PK),
        mk_line(PA1, PF2),
        mk_line(PF2, PI),
        mk_line(PV, PG2),
        mk_line(PG2, PA1),
        mk_line(PW, PH2),
        mk_line(PH2, PZ),
    )
    red_pts = VGroup(
        mk_dot(PA1),
        mk_dot(PA2),
        mk_dot(PB1),
        mk_dot(PB2),
        mk_dot(PC1),
        mk_dot(PC2),
        mk_dot(PD1),
        mk_dot(PD2),
        mk_dot(PE1),
        mk_dot(PE2),
        mk_dot(PF1),
        mk_dot(PF2),
        mk_dot(PG1),
        mk_dot(PG2),
        mk_dot(PH1),
        mk_dot(PH2),
        mk_dot(PI),
        mk_dot(PI1),
        mk_dot(PJ),
        mk_dot(PJ1),
        mk_dot(PK),
        mk_dot(PK1),
        mk_dot(PL),
        mk_dot(PL1),
        mk_dot(PM),
        mk_dot(PM1),
        mk_dot(PN),
        mk_dot(PN1),
        mk_dot(PO),
        mk_dot(PO1),
        mk_dot(PP),
        mk_dot(PP1),
        mk_dot(PQ),
        mk_dot(PQ1),
        mk_dot(PR),
        mk_dot(PR1),
        mk_dot(PS),
        mk_dot(PS1),
        mk_dot(PT),
        mk_dot(PT1),
        mk_dot(PU),
        mk_dot(PU1),
        mk_dot(PV),
        mk_dot(PV1),
        mk_dot(PW),
        mk_dot(PW1),
        mk_dot(PZ),
        mk_dot(PZ1),
    )
    scene.play(Create(tunnel_walls), run_time=2.5)
    scene.play(FadeIn(red_pts), run_time=0.8)
    scene.next_slide()

    # ════ SLIDE 3: Diagonales forzadas ════
    scene.play(FadeOut(sub2), run_time=0.3)
    sub3 = Text('Diagonales forzadas', font_size=18, color=GRAY_B)
    sub3.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.1)
    scene.play(FadeIn(sub3), run_time=0.4)

    forced_diags = VGroup(
        mk_line(PT1, PS1, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PO1, PP1, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PJ1, PI1, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PL1, PK1, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PN1, PM1, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PV1, PU1, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PR1, PQ1, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PH2, PG2, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PF2, PE2, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PD2, PC2, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PZ1, PW1, sw=2.2, color=FORCED_CLR).set_z_index(3),
        mk_line(PB2, PA2, sw=2.2, color=FORCED_CLR).set_z_index(3),
    )
    scene.play(Create(forced_diags), run_time=1.5)
    scene.next_slide()

    # ════ SLIDE 4: Otras diagonales ════
    scene.play(FadeOut(sub3), run_time=0.3)
    sub4 = Text('Otras diagonales', font_size=18, color=GRAY_B)
    sub4.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.1)
    scene.play(FadeIn(sub4), run_time=0.4)

    other_diags = VGroup(
        DashedLine(PT1, PQ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PS1, PQ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PP, PQ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PQ, PO, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PM1, PP, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PM1, PR, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PT, PQ1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PR1, PT, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PR, PT, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PT, PS, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PS1, PE1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PT1, PE1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PC1, PE1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PD1, PE1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PA2, PM, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PB2, PM, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PL, PM, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PN, PM, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PM, PJ1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PK, PI1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PF2, PJ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PE2, PJ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PK, PJ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PI, PJ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PS, PK1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PK1, PI, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PQ1, PW, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PR1, PW, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PV, PW, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PU, PW, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PV, PH2, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PH2, PA1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PZ, PE2, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PF2, PZ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PA1, PZ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PB1, PZ, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PV1, PU, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PD1, PV1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PC1, PZ1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PZ1, PF1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PF1, PG1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PG1, PA2, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PG1, PB2, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PH1, PG1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PH1, PD2, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PD2, PB1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PO, PO1, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
        DashedLine(PO1, PN, color=OTHER_CLR, stroke_width=1.2, dash_length=0.06).set_z_index(2),
    )
    scene.play(Create(other_diags), run_time=1.5)

    leg_f = VGroup(
        Line(ORIGIN, RIGHT*0.4, color=FORCED_CLR, stroke_width=3),
        Text('forzadas', font_size=12, color=FORCED_CLR),
    ).arrange(RIGHT, buff=0.1)
    leg_o = VGroup(
        DashedLine(ORIGIN, RIGHT*0.4, color=OTHER_CLR, stroke_width=2, dash_length=0.06),
        Text('otras', font_size=12, color=OTHER_CLR),
    ).arrange(RIGHT, buff=0.1)
    legend = VGroup(leg_f, leg_o).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    legend.to_corner(DOWN + RIGHT, buff=0.3)
    scene.play(FadeIn(legend), run_time=0.5)
    scene.next_slide()

    # ════ SLIDE 5: Dual + hamiltoniano ════
    scene.play(FadeOut(sub4), run_time=0.3)
    sub5 = Text('Camino hamiltoniano en la dual', font_size=18, color=GRAY_B)
    sub5.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.1)
    scene.play(FadeIn(sub5), run_time=0.4)

    dual_teal = VGroup(
        mk_line(D_PB, D_PA, sw=2.0, color=RED),
        mk_line(D_PA, D_PD3, sw=2.0, color=RED),
        mk_line(D_PC3, D_PB3, sw=2.0, color=RED),
        mk_line(D_PB3, D_PA3, sw=2.0, color=RED),
        mk_line(D_PA3, D_PZ2, sw=2.0, color=RED),
        mk_line(D_PZ2, D_PW2, sw=2.0, color=RED),
        mk_line(D_PW2, D_PV2, sw=2.0, color=RED),
        mk_line(D_PV2, D_PU2, sw=2.0, color=RED),
        mk_line(D_PU2, D_PT2, sw=2.0, color=RED),
        mk_line(D_PT2, D_PS2, sw=2.0, color=RED),
        mk_line(D_PS2, D_PR2, sw=2.0, color=RED),
        mk_line(D_PR2, D_PQ2, sw=2.0, color=RED),
        mk_line(D_PQ2, D_PP2, sw=2.0, color=RED),
        mk_line(D_PP2, D_PO2, sw=2.0, color=RED),
        mk_line(D_PO2, D_PN2, sw=2.0, color=RED),
        mk_line(D_PN2, D_PM2, sw=2.0, color=RED),
        mk_line(D_PM2, D_PL2, sw=2.0, color=RED),
        mk_line(D_PL2, D_PK2, sw=2.0, color=RED),
        mk_line(D_PK2, D_PJ2, sw=2.0, color=RED),
        mk_line(D_PJ2, D_PI2, sw=2.0, color=RED),
        mk_line(D_PI2, D_PH, sw=2.0, color=RED),
        mk_line(D_PH, D_PE, sw=2.0, color=RED),
        mk_line(D_PE, D_PF, sw=2.0, color=RED),
        mk_line(D_PF, D_PG, sw=2.0, color=RED),
        mk_line(D_PG, D_PD, sw=2.0, color=RED),
        mk_line(D_PD, D_PC, sw=2.0, color=RED),
        mk_line(D_PB, D_PC, sw=2.0, color=RED),
        mk_line(D_PC4, D_PE4, sw=2.0, color=RED),
        mk_line(D_PC4, D_PB4, sw=2.0, color=RED),
        mk_line(D_PE4, D_PD4, sw=2.0, color=RED),
        mk_line(D_PD4, D_PF4, sw=2.0, color=RED),
        mk_line(D_PF4, D_PG4, sw=2.0, color=RED),
        mk_line(D_PG4, D_PH4, sw=2.0, color=RED),
        mk_line(D_PH4, D_PF3, sw=2.0, color=RED),
        mk_line(D_PF3, D_PE3, sw=2.0, color=RED),
        mk_line(D_PE3, D_PC3, sw=2.0, color=RED),
        mk_line(D_PG3, D_PH3, sw=2.0, color=RED),
        mk_line(D_PH3, D_PI3, sw=2.0, color=RED),
        mk_line(D_PI3, D_PJ3, sw=2.0, color=RED),
        mk_line(D_PJ3, D_PK3, sw=2.0, color=RED),
        mk_line(D_PK3, D_PL3, sw=2.0, color=RED),
        mk_line(D_PL3, D_PM3, sw=2.0, color=RED),
        mk_line(D_PM3, D_PN3, sw=2.0, color=RED),
        mk_line(D_PN3, D_PO3, sw=2.0, color=RED),
        mk_line(D_PO3, D_PP3, sw=2.0, color=RED),
        mk_line(D_PP3, D_PQ3, sw=2.0, color=RED),
        mk_line(D_PQ3, D_PR3, sw=2.0, color=RED),
        mk_line(D_PR3, D_PS3, sw=2.0, color=RED),
        mk_line(D_PS3, D_PT3, sw=2.0, color=RED),
        mk_line(D_PT3, D_PU3, sw=2.0, color=RED),
        mk_line(D_PU3, D_PV3, sw=2.0, color=RED),
        mk_line(D_PV3, D_PW3, sw=2.0, color=RED),
        mk_line(D_PW3, D_PZ3, sw=2.0, color=RED),
        mk_line(D_PZ3, D_PA4, sw=2.0, color=RED),
        mk_line(D_PA4, D_PB4, sw=2.0, color=RED),
    )
    dual_red = VGroup(
        mk_line(D_PD3, D_PC3, sw=2.0, color=TEAL),
        mk_line(D_PF, D_PC4, sw=2.0, color=TEAL),
        mk_line(D_PE3, D_PG3, sw=2.0, color=TEAL),
        mk_line(D_PM3, D_PT2, sw=2.0, color=TEAL),
        mk_line(D_PT3, D_PM2, sw=2.0, color=TEAL),
    )
    dual_dots = VGroup(
        mk_dot(D_PA, r=0.035),
        mk_dot(D_PA3, r=0.035),
        mk_dot(D_PA4, r=0.035),
        mk_dot(D_PB, r=0.035),
        mk_dot(D_PB3, r=0.035),
        mk_dot(D_PB4, r=0.035),
        mk_dot(D_PC, r=0.035),
        mk_dot(D_PC3, r=0.035),
        mk_dot(D_PC4, r=0.035),
        mk_dot(D_PD, r=0.035),
        mk_dot(D_PD3, r=0.035),
        mk_dot(D_PD4, r=0.035),
        mk_dot(D_PE, r=0.035),
        mk_dot(D_PE3, r=0.035),
        mk_dot(D_PE4, r=0.035),
        mk_dot(D_PF, r=0.035),
        mk_dot(D_PF3, r=0.035),
        mk_dot(D_PF4, r=0.035),
        mk_dot(D_PG, r=0.035),
        mk_dot(D_PG3, r=0.035),
        mk_dot(D_PG4, r=0.035),
        mk_dot(D_PH, r=0.035),
        mk_dot(D_PH3, r=0.035),
        mk_dot(D_PH4, r=0.035),
        mk_dot(D_PI2, r=0.035),
        mk_dot(D_PI3, r=0.035),
        mk_dot(D_PJ2, r=0.035),
        mk_dot(D_PJ3, r=0.035),
        mk_dot(D_PK2, r=0.035),
        mk_dot(D_PK3, r=0.035),
        mk_dot(D_PL2, r=0.035),
        mk_dot(D_PL3, r=0.035),
        mk_dot(D_PM2, r=0.035),
        mk_dot(D_PM3, r=0.035),
        mk_dot(D_PN2, r=0.035),
        mk_dot(D_PN3, r=0.035),
        mk_dot(D_PO2, r=0.035),
        mk_dot(D_PO3, r=0.035),
        mk_dot(D_PP2, r=0.035),
        mk_dot(D_PP3, r=0.035),
        mk_dot(D_PQ2, r=0.035),
        mk_dot(D_PQ3, r=0.035),
        mk_dot(D_PR2, r=0.035),
        mk_dot(D_PR3, r=0.035),
        mk_dot(D_PS2, r=0.035),
        mk_dot(D_PS3, r=0.035),
        mk_dot(D_PT2, r=0.035),
        mk_dot(D_PT3, r=0.035),
        mk_dot(D_PU2, r=0.035),
        mk_dot(D_PU3, r=0.035),
        mk_dot(D_PV2, r=0.035),
        mk_dot(D_PV3, r=0.035),
        mk_dot(D_PW2, r=0.035),
        mk_dot(D_PW3, r=0.035),
        mk_dot(D_PZ2, r=0.035),
        mk_dot(D_PZ3, r=0.035),
    )

    scene.play(FadeIn(dual_dots), Create(dual_teal), Create(dual_red), run_time=2.0)

    leg_h = VGroup(
        Line(ORIGIN, RIGHT*0.4, color=RED, stroke_width=3),
        Text('camino hamiltoniano', font_size=12, color=TEAL),
    ).arrange(RIGHT, buff=0.1)
    leg_nh = VGroup(
        Line(ORIGIN, RIGHT*0.4, color=TEAL, stroke_width=2),
        Text('fuera del camino', font_size=12, color=RED),
    ).arrange(RIGHT, buff=0.1)
    legend2 = VGroup(leg_h, leg_nh).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    legend2.next_to(legend, UP, aligned_edge=RIGHT, buff=0.15)
    scene.play(FadeIn(legend2), run_time=0.5)
    scene.next_slide()

    return {
        'heading': heading,
        'all_objs': None,
    }


class SimpleSlides(Slide):
    def construct(self):
        self.camera.background_color = BLACK
        ctx = title_slide(self, {})
        self.next_slide()
        ctx = holes_slide(self, ctx)
        self.next_slide()
        ctx = paper_slide(self, ctx)
        self.next_slide()
        ctx = example_paper(self, ctx)
        self.next_slide()
