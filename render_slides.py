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
        Text, Line, Dot, VGroup, DashedLine,
        Write, FadeIn, FadeOut, Create, Transform,
        WHITE, YELLOW,
        UP, DOWN, LEFT, RIGHT,
    )

    def p(x, y):
        return np.array([x, y, 0])

    def unit(a, b):
        d = b - a
        return d / np.linalg.norm(d)

    def perp_left(u):
        return np.array([-u[1], u[0], 0])

    def line_intersect(p1, d1, p2, d2):
        A = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
        b = (p2 - p1)[:2]
        try:
            ts = np.linalg.solve(A, b)
            return p1 + ts[0] * d1
        except np.linalg.LinAlgError:
            return (p1 + p2) / 2

    def node_triangle(center, nbrs, gap):
        us = [unit(center, nb) for nb in nbrs]
        ns = [perp_left(u) for u in us]
        verts = []
        for i in range(len(nbrs)):
            j = (i + 1) % len(nbrs)
            v = line_intersect(
                center + ns[i] * gap, us[i],
                center - ns[j] * gap, us[j],
            )
            verts.append(v)
        return verts

    def mk_dot(pos, r=0.10):
        return Dot(pos, radius=r, color=WHITE).set_z_index(2)

    def mk_line(a, b, sw=2.5):
        return Line(a, b, color=WHITE, stroke_width=sw)

    # ── Fade out slide anterior ──────────────────────────────────────────
    all_prev = [v for v in ctx.values() if v is not None]
    if all_prev:
        scene.play(*[FadeOut(obj) for obj in all_prev])

    heading = Text("Ejemplo de la reducción", font_size=30, color=WHITE)
    heading.to_corner(UP + LEFT, buff=0.4)
    scene.play(Write(heading))

    # ════════════════════════════════════════════════════════════════════
    # Coordenadas de la gráfica cúbica
    # ════════════════════════════════════════════════════════════════════
    L     = p(-1.2,  0.0)
    R     = p( 1.2,  0.0)
    L_top = p(-3.8,  2.4)
    L_bot = p(-3.8, -2.4)
    R_top = p( 3.8,  2.4)
    R_bot = p( 3.8, -2.4)

    gap  = 0.28
    rise = 0.85

    # ── SLIDE 1: gráfica cúbica ──────────────────────────────────────────
    e_LR  = mk_line(L, R)
    e_LLt = mk_line(L, L_top)
    e_LLb = mk_line(L, L_bot)
    e_RRt = mk_line(R, R_top)
    e_RRb = mk_line(R, R_bot)

    d_L    = mk_dot(L,     r=0.13)
    d_R    = mk_dot(R,     r=0.13)
    d_Ltop = mk_dot(L_top, r=0.10)
    d_Lbot = mk_dot(L_bot, r=0.10)
    d_Rtop = mk_dot(R_top, r=0.10)
    d_Rbot = mk_dot(R_bot, r=0.10)

    scene.play(
        Create(e_LR), Create(e_LLt), Create(e_LLb),
        Create(e_RRt), Create(e_RRb),
        FadeIn(d_L), FadeIn(d_R),
        FadeIn(d_Ltop), FadeIn(d_Lbot),
        FadeIn(d_Rtop), FadeIn(d_Rbot),
    )
    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════
    # SLIDE 2: nodos explotan en triángulos
    # L vecinos CCW: [R, L_top, L_bot]
    # R vecinos CCW: [R_top, L, R_bot]
    # ════════════════════════════════════════════════════════════════════
    Lv = node_triangle(L, [R, L_top, L_bot], gap)
    # Lv[0]: entre L→R y L→Ltop  → boca superior túnel central (= vértice 'c')
    # Lv[1]: entre L→Ltop y L→Lbot → extremo externo (= vértice 'a')
    # Lv[2]: entre L→Lbot y L→R  → boca inferior túnel central (= vértice 'b')

    Rv = node_triangle(R, [R_top, L, R_bot], gap)
    # Rv[0]: entre R→Rtop y R→L  → boca superior túnel central (= vértice 'e')
    # Rv[1]: entre R→L y R→Rbot  → boca inferior túnel central (= vértice 'd')
    # Rv[2]: entre R→Rbot y R→Rtop → extremo externo (= vértice 'f')

    dLv = [Dot(L, radius=0.10, color=WHITE).set_z_index(2) for _ in range(3)]
    dRv = [Dot(R, radius=0.10, color=WHITE).set_z_index(2) for _ in range(3)]
    for d in dLv + dRv:
        scene.add(d)

    scene.play(
        FadeOut(d_L), FadeOut(d_R),
        *[dLv[i].animate.move_to(Lv[i]) for i in range(3)],
        *[dRv[i].animate.move_to(Rv[i]) for i in range(3)],
    )
    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════
    # Función para transformar una arista en túnel en V
    # Devuelve (vTM, vBM): las dos puntas del V (arc vertices)
    # ════════════════════════════════════════════════════════════════════
    def edge_to_V(edge_mob,
                  src_top, src_bot,
                  dst_top, dst_bot,
                  src_dot_top, src_dot_bot,
                  dst_dot_top, dst_dot_bot,
                  u_edge, rise_sign):
        n_rise = perp_left(u_edge) * rise_sign

        # Paso 1: paralelas
        top = mk_line(src_top, dst_top)
        bot = mk_line(src_bot, dst_bot)
        anims = [Transform(edge_mob, top), FadeIn(bot)]
        for sd, pos in [(src_dot_top, src_top), (src_dot_bot, src_bot)]:
            anims.append(sd.animate.move_to(pos))
        for sd, pos in [(dst_dot_top, dst_top), (dst_dot_bot, dst_bot)]:
            if sd is not None:
                anims.append(sd.animate.move_to(pos))
        scene.play(*anims)
        scene.next_slide()

        # Paso 2: vértice central
        TM = (src_top + dst_top) / 2
        BM = (src_bot + dst_bot) / 2
        tTL = mk_line(src_top, TM);  tTR = mk_line(TM, dst_top)
        tBL = mk_line(src_bot, BM);  tBR = mk_line(BM, dst_bot)
        dTM = mk_dot(TM, r=0.09);    dBM = mk_dot(BM, r=0.09)
        scene.play(
            Transform(edge_mob, tTL), FadeIn(tTR),
            Transform(bot, tBL),      FadeIn(tBR),
            FadeIn(dTM), FadeIn(dBM),
        )
        scene.next_slide()

        # Paso 3: centrales suben → V
        vTM = TM + n_rise * rise
        vBM = BM + n_rise * rise
        vTL = mk_line(src_top, vTM);  vTR = mk_line(vTM, dst_top)
        vBL = mk_line(src_bot, vBM);  vBR = mk_line(vBM, dst_bot)
        dvTM = mk_dot(vTM, r=0.09);   dvBM = mk_dot(vBM, r=0.09)
        scene.play(
            Transform(edge_mob, vTL), Transform(tTR, vTR),
            Transform(bot,      vBL), Transform(tBR, vBR),
            Transform(dTM, dvTM),     Transform(dBM, dvBM),
        )
        scene.next_slide()
        return vTM, vBM   # arc vertices: punta superior e inferior del V

    u_LR  = unit(L, R)
    u_LLt = unit(L, L_top)
    u_LLb = unit(L, L_bot)
    u_RRt = unit(R, R_top)
    u_RRb = unit(R, R_bot)

    # ── Arista central L↔R → h (superior) y g (inferior) ───────────────
    # top: Lv[0]=c → Rv[0]=e  (boca superior)
    # bot: Lv[2]=b → Rv[1]=d  (boca inferior)
    # rise hacia ARRIBA → h sube, g baja (rise_sign=+1 da arriba, -1 abajo)
    # Pero queremos DOS puntas: una sube y otra baja.
    # El paper muestra h ARRIBA y g ABAJO del túnel central.
    # En edge_to_V el vTM sube (n_rise*rise), vBM también sube (mismo n_rise).
    # Para que uno suba y otro baje, llamamos dos veces o usamos signo opuesto.
    # Solución: el vTM sube con +rise_sign y el vBM con -rise_sign.

    n_rise_LR = perp_left(u_LR)  # apunta hacia arriba

    # Paso 1: paralelas
    top_LR = mk_line(Lv[0], Rv[0])
    bot_LR = mk_line(Lv[2], Rv[1])
    scene.play(
        Transform(e_LR, top_LR),
        dLv[0].animate.move_to(Lv[0]),
        dLv[2].animate.move_to(Lv[2]),
        dRv[0].animate.move_to(Rv[0]),
        dRv[1].animate.move_to(Rv[1]),
        FadeIn(bot_LR),
    )
    scene.next_slide()

    # Paso 2: vértice central en cada paralela
    TM_LR = (Lv[0] + Rv[0]) / 2   # centro paralela superior → será h
    BM_LR = (Lv[2] + Rv[1]) / 2   # centro paralela inferior → será g

    tTL_LR = mk_line(Lv[0], TM_LR);  tTR_LR = mk_line(TM_LR, Rv[0])
    tBL_LR = mk_line(Lv[2], BM_LR);  tBR_LR = mk_line(BM_LR, Rv[1])
    dTM_LR = mk_dot(TM_LR, r=0.09)
    dBM_LR = mk_dot(BM_LR, r=0.09)
    scene.play(
        Transform(e_LR, tTL_LR), FadeIn(tTR_LR),
        Transform(bot_LR, tBL_LR), FadeIn(tBR_LR),
        FadeIn(dTM_LR), FadeIn(dBM_LR),
    )
    scene.next_slide()

    # Paso 3: ambos suben, h más arriba (punta del V superior),
    # g a media altura entre las bocas (punta del V inferior, pero también hacia arriba)
    vh = TM_LR + n_rise_LR * rise          # h = punta alta del V (paralela superior)
    vg = BM_LR + n_rise_LR * (rise * 0.45) # g = punta baja del V (paralela inferior, sube menos)

    vTL_LR = mk_line(Lv[0], vh);   vTR_LR = mk_line(vh, Rv[0])
    vBL_LR = mk_line(Lv[2], vg);   vBR_LR = mk_line(vg, Rv[1])
    dvh = mk_dot(vh, r=0.10)
    dvg = mk_dot(vg, r=0.10)

    scene.play(
        Transform(e_LR,    vTL_LR), Transform(tTR_LR, vTR_LR),
        Transform(bot_LR,  vBL_LR), Transform(tBR_LR, vBR_LR),
        Transform(dTM_LR,  dvh),    Transform(dBM_LR,  dvg),
    )
    scene.next_slide()

    # ── Ramas laterales (sin arc vertices, extremos libres) ──────────────
    n_LLt = perp_left(u_LLt)
    Ltop_top = L_top + n_LLt * gap
    Ltop_bot = L_top - n_LLt * gap
    cLLt, _ = edge_to_V(e_LLt,
        Lv[1], Lv[0], Ltop_top, Ltop_bot,
        dLv[1], dLv[0], None, None,
        u_LLt, rise_sign=-1)

    n_LLb = perp_left(u_LLb)
    Lbot_top = L_bot + n_LLb * gap
    Lbot_bot = L_bot - n_LLb * gap
    cLLb, _ = edge_to_V(e_LLb,
        Lv[2], Lv[1], Lbot_top, Lbot_bot,
        dLv[2], dLv[1], None, None,
        u_LLb, rise_sign=-1)

    n_RRt = perp_left(u_RRt)
    Rtop_top = R_top + n_RRt * gap
    Rtop_bot = R_top - n_RRt * gap
    cRRt, _ = edge_to_V(e_RRt,
        Rv[0], Rv[2], Rtop_top, Rtop_bot,
        dRv[0], dRv[2], None, None,
        u_RRt, rise_sign=-1)

    n_RRb = perp_left(u_RRb)
    Rbot_top = R_bot + n_RRb * gap
    Rbot_bot = R_bot - n_RRb * gap
    cRRb, _ = edge_to_V(e_RRb,
        Rv[2], Rv[1], Rbot_top, Rbot_bot,
        dRv[2], dRv[1], None, None,
        u_RRb, rise_sign=-1)

    # ════════════════════════════════════════════════════════════════════
    # SLIDE FINAL — diagonales
    # El interior del túnel es el hexágono: c-h-e-d-g-b
    # Diagonal FORZADA (paper): g-h (conecta los dos arc vertices)
    # Para triangular el hexágono con g-h como base se necesitan además:
    #   c-g y e-g  (triangularizan los cuadrantes con g)
    #   b-h y d-h  (triangularizan los cuadrantes con h)
    # Según Fig 4: sólidas = g-h, c-g, e-g (forzadas)
    #              punteadas = b-h, d-h (otras diagonales)
    # ════════════════════════════════════════════════════════════════════
    # Vértices del hexágono interior del túnel:
    va = Lv[1]   # a — externo L
    vb = Lv[2]   # b — boca inf L
    vc = Lv[0]   # c — boca sup L
    vd = Rv[1]   # d — boca inf R
    ve = Rv[0]   # e — boca sup R
    vf = Rv[2]   # f — externo R

    # Diagonales forzadas (sólidas, YELLOW): g-h, c-g, e-g
    forced = VGroup(
        Line(vg, vh, color=YELLOW, stroke_width=2.5).set_z_index(3),
        Line(vc, vg, color=YELLOW, stroke_width=2.5).set_z_index(3),
        Line(ve, vg, color=YELLOW, stroke_width=2.5).set_z_index(3),
    )

    # Otras diagonales (punteadas, WHITE): b-h, d-h
    other_diags = VGroup(
        DashedLine(vb, vh, color=WHITE, stroke_width=2,
                   dash_length=0.10).set_z_index(2),
        DashedLine(vd, vh, color=WHITE, stroke_width=2,
                   dash_length=0.10).set_z_index(2),
    )

    legend_forced = Text("── diagonales forzadas", font_size=16, color=YELLOW)
    legend_other  = Text("╌╌ otras diagonales",    font_size=16, color=WHITE)
    legend = VGroup(legend_forced, legend_other).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    legend.to_corner(DOWN + RIGHT, buff=0.4)

    scene.play(Create(forced))
    scene.play(Create(other_diags))
    scene.play(FadeIn(legend))
    scene.next_slide()

    return {
        "heading":  heading,
        "all_objs": None,
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
