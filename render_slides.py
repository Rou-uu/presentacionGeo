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


def graph_slide(scene, ctx):
    import numpy as np

    scene.play(
        FadeOut(ctx["title"]), FadeOut(ctx["subtitle"]),
        FadeOut(ctx["corner_left"]), FadeOut(ctx["corner_right"]),
    )

    heading = Text("Triangulación Hamiltoniana", font_size=28, color=WHITE)
    heading.to_corner(UP + LEFT, buff=0.4)

    description = Text(
        "Decimos que una triangulación es hamiltoniana\n"
        "si su gráfica dual contiene un camino hamiltoniano",
        font_size=20, color=WHITE, line_spacing=0.8,
    )
    description.next_to(heading, DOWN, buff=0.2, aligned_edge=LEFT)

    scale, ox, oy = 0.85, -4.675, -1.7
    def mp(x, y):
        return np.array([x * scale + ox, y * scale + oy, 0])

    pos = {
        "A": mp(0,    0),
        "B": mp(2,   -1),
        "C": mp(4,    0),
        "D": mp(1,    3),
        "E": mp(4.5,  2),
        "F": mp(8,    0),
        "G": mp(7,    2),
        "H": mp(11,   1),
        "I": mp(8,    4),
        "J": mp(11,   5),
    }

    edge_pairs = [
        ("F","H"), ("I","J"), ("J","H"),
        ("A","B"), ("B","C"), ("A","C"),
        ("A","D"), ("C","D"), ("F","C"),
        ("D","E"),
        ("E","C"), ("E","G"), ("E","F"),
        ("G","I"), ("I","H"), ("H","G"), ("F","G"),
    ]

    lines = VGroup(*[
        Line(pos[u], pos[v], color=WHITE, stroke_width=2)
        for u, v in edge_pairs
        if not np.allclose(pos[u], pos[v])
    ])

    v_dots = VGroup(*[
        Dot(point=p, radius=0.09, color=WHITE).set_z_index(1)
        for p in pos.values()
    ])

    scene.play(Write(heading), FadeIn(description))
    scene.play(Create(lines))
    scene.play(FadeIn(v_dots))
    scene.next_slide()

    ham_pos = {
        "K": mp(2,   1),
        "L": mp(2,   -0.3),
        "M": mp(3.5, 1.5),
        "N": mp(5,   1),
        "O": mp(7,   1),
        "P": mp(9,   1),
        "Q": mp(9,   2),
        "R": mp(10,  3),
    }

    ham_edges = [
        ("L", "K"), ("K", "M"), ("M", "N"), ("N", "O"),
        ("O", "P"), ("P", "Q"), ("Q", "R"),
    ]

    ham_dots = VGroup(*[
        Dot(point=p, radius=0.12, color=YELLOW).set_z_index(2)
        for p in ham_pos.values()
    ])

    ham_segs = [
        Line(ham_pos[u], ham_pos[v], color=YELLOW, stroke_width=4).set_z_index(1)
        for u, v in ham_edges
    ]

    scene.play(FadeIn(ham_dots))
    for seg in ham_segs:
        scene.play(Create(seg), run_time=0.6)

    scene.next_slide()

    heading2 = Text("Triangulación secuencial", font_size=28, color=WHITE)
    heading2.to_corner(UP + LEFT, buff=0.4)

    description2 = Text(
        "Decimos que una triangulación es secuencial si su gráfica dual\n"
        "contiene un ciclo (o camino) hamiltoniano tal que no haya tres\n"
        "aristas de la triangulación cruzadas consecutivamente por dicho\n"
        "camino que incidan sobre el mismo vértice de la triangulación",
        font_size=18, color=WHITE, line_spacing=0.8,
    )
    description2.next_to(heading2, DOWN, buff=0.2, aligned_edge=LEFT)

    s_pos = mp(12, 3)
    h_highlight = Dot(pos["H"], radius=0.13, color=RED).set_z_index(3)
    s_highlight = Dot(s_pos, radius=0.13, color=WHITE).set_z_index(3)
    red_lines = VGroup(*[
        Line(pos[u], pos[v], color=RED, stroke_width=4).set_z_index(2)
        for u, v in [("H", "G"), ("I", "H"), ("J", "H")]
    ])
    s_lines = VGroup(
        Line(s_pos, pos["J"], color=WHITE, stroke_width=4).set_z_index(2),
        Line(s_pos, pos["H"], color=WHITE, stroke_width=4).set_z_index(2),
    )

    scene.play(Transform(heading, heading2), Transform(description, description2))
    scene.play(FadeIn(h_highlight), Create(red_lines))
    scene.play(FadeIn(s_highlight), Create(s_lines))

    scene.next_slide()

    heading3 = Text("Orejas", font_size=28, color=WHITE)
    heading3.to_corner(UP + LEFT, buff=0.4)

    description3 = Text(
        "Las orejas de un polígono son triángulos que tienen dos\n"
        "de sus tres caras (lados) definidas por la frontera del polígono.",
        font_size=20, color=WHITE, line_spacing=0.8,
    )
    description3.next_to(heading3, DOWN, buff=0.2, aligned_edge=LEFT)

    scene.play(
        Transform(heading, heading3), Transform(description, description3),
        FadeOut(ham_dots), FadeOut(VGroup(*ham_segs)),
        FadeOut(h_highlight), FadeOut(s_highlight),
        FadeOut(red_lines), FadeOut(s_lines),
    )

    ear_IJH_dots = VGroup(*[
        Dot(pos[k], radius=0.13, color=BLUE).set_z_index(3)
        for k in ["I", "J", "H"]
    ])
    ear_IJH_lines = VGroup(*[
        Line(pos[u], pos[v], color=BLUE, stroke_width=4).set_z_index(2)
        for u, v in [("I", "J"), ("J", "H"), ("I", "H")]
    ])
    ear_ABC_dots = VGroup(*[
        Dot(pos[k], radius=0.13, color=BLUE).set_z_index(3)
        for k in ["A", "B", "C"]
    ])
    ear_ABC_lines = VGroup(*[
        Line(pos[u], pos[v], color=BLUE, stroke_width=4).set_z_index(2)
        for u, v in [("A", "B"), ("B", "C"), ("A", "C")]
    ])

    scene.play(FadeIn(ear_IJH_dots), Create(ear_IJH_lines))
    scene.play(FadeIn(ear_ABC_dots), Create(ear_ABC_lines))

    scene.next_slide()

    heading4 = Text("Polígono serpenteante", font_size=28, color=WHITE)
    heading4.to_corner(UP + LEFT, buff=0.4)

    description4 = Text(
        "Una triangulación de un polígono es Hamiltoniana si y solo si\n"
        "contiene exactamente dos orejas. Es decir, su gráfica dual es\n"
        "un camino hamiltoniano. A estos polígonos les llamamos\n"
        "polígonos serpenteantes.",
        font_size=20, color=WHITE, line_spacing=0.8,
    )
    description4.next_to(heading4, DOWN, buff=0.2, aligned_edge=LEFT)

    ham_dots2 = VGroup(*[
        Dot(point=p, radius=0.12, color=YELLOW).set_z_index(2)
        for p in ham_pos.values()
    ])
    ham_segs2 = VGroup(*[
        Line(ham_pos[u], ham_pos[v], color=YELLOW, stroke_width=4).set_z_index(1)
        for u, v in ham_edges
    ])

    scene.play(
        Transform(heading, heading4), Transform(description, description4),
    )
    scene.play(FadeIn(ham_dots2), Create(ham_segs2))

    return {
        "lines": lines, "dots": v_dots,
        "heading": heading, "description": description,
        "ham_dots2": ham_dots2, "ham_segs2": ham_segs2,
        "ear_IJH_dots": ear_IJH_dots, "ear_IJH_lines": ear_IJH_lines,
        "ear_ABC_dots": ear_ABC_dots, "ear_ABC_lines": ear_ABC_lines,
    }


def hershberger_slide(scene, ctx):
    import numpy as np

    scene.play(
        FadeOut(ctx["lines"]), FadeOut(ctx["dots"]),
        FadeOut(ctx["heading"]), FadeOut(ctx["description"]),
        FadeOut(ctx["ham_dots2"]), FadeOut(ctx["ham_segs2"]),
        FadeOut(ctx["ear_IJH_dots"]), FadeOut(ctx["ear_IJH_lines"]),
        FadeOut(ctx["ear_ABC_dots"]), FadeOut(ctx["ear_ABC_lines"]),
    )

    title = Text("Gráfica de visibilidad", font_size=64, color=WHITE)
    scene.play(Write(title))
    scene.next_slide()

    title_small = Text("Gráfica de visibilidad", font_size=22, color=WHITE)
    title_small.to_corner(UP + LEFT, buff=0.4)
    algo_text = Text("Algoritmo de Hershberger", font_size=22, color=WHITE)
    algo_text.next_to(title_small, RIGHT, buff=0.5)
    scene.play(Transform(title, title_small), Write(algo_text))
    scene.next_slide()

    # Hexágono no convexo tipo escalón (v3 es el vértice reflejo)
    P = [
        np.array([-3.5, -2.0, 0]),  # v0
        np.array([ 3.5, -2.0, 0]),  # v1
        np.array([ 3.5,  0.0, 0]),  # v2
        np.array([ 0.5,  0.0, 0]),  # v3 (reflejo)
        np.array([ 0.5,  1.0, 0]),  # v4
        np.array([-3.5,  1.0, 0]),  # v5
    ]
    label_offsets = [
        (DOWN + LEFT) * 0.3,
        (DOWN + RIGHT) * 0.3,
        RIGHT * 0.3,
        (DOWN + RIGHT) * 0.3,
        UP * 0.3,
        (UP + LEFT) * 0.3,
    ]

    polygon = Polygon(*P, color=WHITE, stroke_width=3)
    v_dots = VGroup(*[Dot(p, radius=0.1, color=WHITE).set_z_index(1) for p in P])
    v_labels = VGroup(*[
        Text(f"v{i}", font_size=22, color=WHITE).move_to(P[i] + label_offsets[i])
        for i in range(6)
    ])

    scene.play(Create(polygon))
    scene.play(FadeIn(v_dots), Write(v_labels))
    scene.next_slide()

    # Aristas de visibilidad no adyacentes por vértice fuente
    vis_by_vertex = [
        (0, [(0, 2), (0, 3), (0, 4)]),
        (1, [(1, 3), (1, 5)]),
        (3, [(3, 5)]),
    ]

    all_segs = []
    for vi, edges in vis_by_vertex:
        hl = v_dots[vi].copy().set_color(YELLOW).scale(2).set_z_index(2)
        scene.play(FadeIn(hl))
        for u, v in edges:
            seg = Line(P[u], P[v], color=YELLOW, stroke_width=2)
            scene.play(Create(seg), run_time=0.5)
            all_segs.append(seg)
        scene.play(FadeOut(hl))
        scene.next_slide()

    return {
        "title": title, "algo_text": algo_text,
        "polygon": polygon, "v_dots": v_dots, "v_labels": v_labels,
        "vis_segs": VGroup(*all_segs),
    }


def dp_slide(scene, ctx):
    import numpy as np

    scene.play(FadeOut(ctx["title"]), FadeOut(ctx["algo_text"]), FadeOut(ctx["vis_segs"]))

    polygon  = ctx["polygon"]
    v_dots   = ctx["v_dots"]
    v_labels = ctx["v_labels"]

    P = [
        np.array([-3.5, -2.0, 0]),
        np.array([ 3.5, -2.0, 0]),
        np.array([ 3.5,  0.0, 0]),
        np.array([ 0.5,  0.0, 0]),
        np.array([ 0.5,  1.0, 0]),
        np.array([-3.5,  1.0, 0]),
    ]

    def mid(i, j, off=None):
        m = (P[i] + P[j]) / 2
        return m if off is None else m + off

    # ── Fase 1: Preparación — colorear por bucket ───────────────────────────
    heading = Text("Preparación e Inicialización", font_size=24, color=WHITE)
    heading.to_corner(UP + LEFT, buff=0.4)

    desc = Text(
        "Vértices numerados en sentido horario.\n"
        "Aristas visibles organizadas por distancia k = j − i.",
        font_size=18, color=WHITE, line_spacing=0.8,
    )
    desc.next_to(heading, DOWN, buff=0.2, aligned_edge=LEFT)

    k2_pairs = [(0, 2), (1, 3), (2, 4), (3, 5)]
    k3_pairs = [(0, 3)]
    k4_pairs = [(0, 4), (1, 5)]

    k2_segs = VGroup(*[Line(P[i], P[j], color=BLUE,  stroke_width=3) for i, j in k2_pairs])
    k3_segs = VGroup(*[Line(P[i], P[j], color=GREEN, stroke_width=3) for i, j in k3_pairs])
    k4_segs = VGroup(*[Line(P[i], P[j], color=RED,   stroke_width=3) for i, j in k4_pairs])

    legend = VGroup(
        Text("k=2", font_size=18, color=BLUE),
        Text("k=3", font_size=18, color=GREEN),
        Text("k=4", font_size=18, color=RED),
    ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_corner(UP + RIGHT, buff=0.5)

    scene.play(Write(heading), FadeIn(desc))
    scene.play(Create(k2_segs), FadeIn(legend[0]))
    scene.play(Create(k3_segs), FadeIn(legend[1]))
    scene.play(Create(k4_segs), FadeIn(legend[2]))
    scene.next_slide()

    # ── Fase 2: Casos Base (k = 2) ──────────────────────────────────────────
    heading2 = Text("Casos Base  (k = 2)", font_size=24, color=WHITE)
    heading2.to_corner(UP + LEFT, buff=0.4)

    base_fml = MathTex(
        r"D[i,\,i{+}2] = \top \iff (i,\,i{+}2)\text{ es cuerda visible}",
        font_size=22, color=WHITE,
    )
    base_fml.next_to(heading2, DOWN, buff=0.2, aligned_edge=LEFT)

    d_k2 = VGroup(*[
        Text("T", font_size=16, color=BLUE).move_to(mid(i, j, np.array([0, 0.3, 0])))
        for i, j in k2_pairs
    ])

    scene.play(Transform(heading, heading2), Transform(desc, base_fml))
    scene.play(FadeIn(d_k2))
    scene.next_slide()

    # ── Fase 3: Recurrencia ──────────────────────────────────────────────────
    heading3 = Text("Recurrencia", font_size=24, color=WHITE)
    heading3.to_corner(UP + LEFT, buff=0.4)

    rec_fml = MathTex(
        r"D[i,j] = \bigl(D[i,j{-}1]\wedge(i,j{-}1)_{\text{vis}}\bigr)"
        r"\;\lor\;"
        r"\bigl(D[i{+}1,j]\wedge(i{+}1,j)_{\text{vis}}\bigr)",
        font_size=18, color=WHITE,
    )
    rec_fml.next_to(heading3, DOWN, buff=0.2, aligned_edge=LEFT)

    scene.play(Transform(heading, heading3), Transform(desc, rec_fml))

    # D[0,3]: D[0,2]=T ∧ (0,2) visible → T
    hl02 = Line(P[0], P[2], color=WHITE, stroke_width=7).set_z_index(3)
    d03  = Text("T", font_size=16, color=GREEN).move_to(mid(0, 3, np.array([-0.3, 0.15, 0])))
    scene.play(Create(hl02))
    scene.play(FadeOut(hl02), Write(d03))

    # D[0,4]: D[0,3]=T ∧ (0,3) visible → T
    hl03 = Line(P[0], P[3], color=WHITE, stroke_width=7).set_z_index(3)
    d04  = Text("T", font_size=16, color=RED).move_to(mid(0, 4, np.array([0, 0.3, 0])))
    scene.play(Create(hl03))
    scene.play(FadeOut(hl03), Write(d04))

    # D[1,5]: (1,4) no visible, (2,5) no visible → F
    d15 = Text("F", font_size=16, color=RED).move_to(mid(1, 5, np.array([0, 0.3, 0])))
    scene.play(Write(d15))
    scene.next_slide()

    # ── Fase 4: Condición de Éxito ───────────────────────────────────────────
    heading4 = Text("Condición de Éxito", font_size=24, color=WHITE)
    heading4.to_corner(UP + LEFT, buff=0.4)

    success = Text(
        "D[0,4] = V  ∧  D[4,0] = V",
        font_size=18, color=WHITE,
    )
    success.next_to(heading4, DOWN, buff=0.2, aligned_edge=LEFT)

    # Triangulación hamiltoniana: fan desde v0 + triángulo (4,5,0)
    tris = VGroup(*[
        Polygon(P[a], P[b], P[c], color=BLUE, stroke_width=1).set_fill(BLUE, opacity=0.25)
        for a, b, c in [(0,1,2), (0,2,3), (0,3,4), (4,5,0)]
    ])

    scene.play(Transform(heading, heading4), Transform(desc, success))
    for tri in tris:
        scene.play(FadeIn(tri), run_time=0.5)

    return {
        "polygon": polygon, "v_dots": v_dots, "v_labels": v_labels,
        "heading": heading, "success": desc,
        "k_segs": VGroup(k2_segs, k3_segs, k4_segs),
        "d_labels": VGroup(d_k2, d03, d04, d15),
        "tris": tris, "legend": legend,
    }


class SimpleSlides(Slide):
    def construct(self):
        self.camera.background_color = BLACK
        ctx = title_slide(self, {})
        self.next_slide()
        ctx = graph_slide(self, ctx)
        self.next_slide()
        ctx = hershberger_slide(self, ctx)
        self.next_slide()
        ctx = dp_slide(self, ctx)
        self.next_slide()
