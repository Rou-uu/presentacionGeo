# /// script
# requires-python = "==3.12"
# dependencies = [
#     "manim==0.19.1",
#     "manim-slides==5.5.2",
#     "marimo",
#     "mohtml==0.1.11",
#     "moterm==0.1.0",
#     "numpy==2.4.4",
# ]
# ///

import marimo

__generated_with = "0.23.8"
app = marimo.App(sql_output="polars")

with app.setup:
    from manim import (
        Text, Square, Line, Dot, RegularPolygon, Polygon, Circle, DashedLine, RoundedRectangle,
        MathTex, VGroup,
        Write, FadeIn, FadeOut, Create, Transform,
        MoveAlongPath, LaggedStart,
        ImageMobject,
        BLACK, WHITE, YELLOW, BLUE, RED, GREEN, GOLD, TEAL,
        UP, DOWN, LEFT, RIGHT, ORIGIN,
        smooth,
    )
    from manim_slides import Slide


@app.cell
def _():
    import marimo as mo
    from pathlib import Path

    return Path, mo


@app.function
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


@app.function
def hexagon_slide(scene, ctx):
    scene.play(FadeOut(ctx["title"]), FadeOut(ctx["subtitle"]), FadeOut(ctx["corner_left"]), FadeOut(ctx["corner_right"]))

    hexagon = RegularPolygon(n=6, color=WHITE, stroke_width=3).scale(3)
    scene.play(Create(hexagon))
    scene.next_slide()

    verts = hexagon.get_vertices()
    diagonals = [
        Line(verts[0], verts[2], color=BLUE, stroke_width=2),
        Line(verts[0], verts[3], color=BLUE, stroke_width=2),
        Line(verts[0], verts[4], color=BLUE, stroke_width=2),
    ]
    scene.play(*[Create(d) for d in diagonals])

    return {"hexagon": hexagon, "diagonals": diagonals}


@app.function
def vertex_slide(scene, ctx):
    scene.play(*[FadeOut(m) for m in scene.mobjects])

    # Vértices del triángulo inicial (centrado)
    A = LEFT * 1.5 + DOWN * 1.2
    B = RIGHT * 1.5 + DOWN * 1.2
    C = UP * 1.5

    triangle = Polygon(A, B, C, color=WHITE, stroke_width=3)
    v_dots = [Dot(point=p, radius=0.15, color=BLUE).set_z_index(1) for p in [A, B, C]]
    v_labels = [
        MathTex(r"v_0", font_size=36).next_to(A, DOWN + LEFT, buff=0.15),
        MathTex(r"v_1", font_size=36).next_to(B, DOWN + RIGHT, buff=0.15),
        MathTex(r"v_2", font_size=36).next_to(C, UP, buff=0.15),
    ]
    tri_group = VGroup(triangle, *v_dots, *v_labels)

    scene.play(Create(triangle))
    scene.play(*[FadeIn(d) for d in v_dots], *[Write(l) for l in v_labels])
    scene.next_slide()

    # Mover triángulo a la izquierda y mostrar arreglos de coordenadas
    scene.play(tri_group.animate.shift(LEFT * 3))

    arr0 = MathTex(r"v_0 = \begin{bmatrix} x_0 \\ y_0 \\ z_0 \end{bmatrix}", font_size=30)
    arr1 = MathTex(r"v_1 = \begin{bmatrix} x_1 \\ y_1 \\ z_1 \end{bmatrix}", font_size=30)
    arr2 = MathTex(r"v_2 = \begin{bmatrix} x_2 \\ y_2 \\ z_2 \end{bmatrix}", font_size=30)
    arr_group = VGroup(arr0, arr1, arr2).arrange(DOWN, buff=0.5).move_to(RIGHT * 3.8)
    scene.play(FadeIn(arr0), FadeIn(arr1), FadeIn(arr2))
    scene.next_slide()

    # Nuevo vértice v3 unido a v1 y v2 (los dos vértices "visibles"/frontera)
    # Posiciones tras el shift LEFT*3:
    B_shifted = B + LEFT * 3   # (-1.5, -1.2, 0)
    C_shifted = C + LEFT * 3   # (-3.0,  1.5, 0)
    D = RIGHT * 0.8 + DOWN * 0.2

    edge_v1v3 = Line(B_shifted, D, color=WHITE, stroke_width=3)
    edge_v2v3 = Line(C_shifted, D, color=WHITE, stroke_width=3)
    dot_v3 = Dot(point=D, radius=0.15, color=BLUE).set_z_index(1)
    label_v3 = MathTex(r"v_3", font_size=36).next_to(D, RIGHT, buff=0.15)

    scene.play(arr_group.animate.shift(UP * 0.6), rate_func=smooth)

    arr3 = MathTex(r"v_3 = \begin{bmatrix} x_3 \\ y_3 \\ z_3 \end{bmatrix}", font_size=30)
    arr3.next_to(arr_group, DOWN, buff=0.5)



    scene.play(Create(edge_v1v3), Create(edge_v2v3))
    scene.play(FadeIn(dot_v3), Write(label_v3))
    scene.play(FadeIn(arr3))

    return {
        **ctx,
        "objects": [tri_group, arr_group, arr3, VGroup(edge_v1v3, edge_v2v3), dot_v3, label_v3]
    }


@app.function
def slide_90s(scene, ctx):
    scene.play(FadeOut(ctx["hexagon"]), *[FadeOut(d) for d in ctx["diagonals"]])

    # --- SGI workstation ---
    img_sgi = ImageMobject("sgi").set_height(5.5).move_to(DOWN * 0.3)
    text_top = Text("Estación de trabajo de Silicon Graphics (1994)", font_size=28, color=WHITE)
    text_top.to_edge(UP, buff=0.2)
    scene.play(FadeIn(img_sgi), FadeIn(text_top))
    scene.next_slide()

    # --- Toy Story ---
    img_ts1 = ImageMobject("toy_story_1").set_height(4.5).shift(LEFT * 3.2)
    img_ts2 = ImageMobject("toy_story_2").set_height(4.5).shift(RIGHT * 3.2)
    text_ts = Text("Detrás de escenas para Toy Story (1995)", font_size=28, color=WHITE)
    text_ts.to_edge(UP, buff=0.2)
    scene.play(FadeOut(img_sgi), Transform(text_top, text_ts), FadeIn(img_ts1), FadeIn(img_ts2))
    scene.next_slide()

    # --- Videojuegos grupo 1 ---
    xs = [-4.5, 0, 4.5]
    g1_imgs = [
        ImageMobject("doom").set_height(3).move_to([xs[0], -0.5, 0]),
        ImageMobject("re").set_height(3).move_to([xs[1], -0.5, 0]),
        ImageMobject("mario64").set_height(3).move_to([xs[2], -0.5, 0]),
    ]
    g1_caps = [
        Text("Doom (1993)", font_size=20, color=WHITE).next_to(g1_imgs[0], DOWN, buff=0.2),
        Text("Resident Evil (1996)", font_size=20, color=WHITE).next_to(g1_imgs[1], DOWN, buff=0.2),
        Text("Super Mario 64 (1996)", font_size=20, color=WHITE).next_to(g1_imgs[2], DOWN, buff=0.2),
    ]
    text_games = Text("Videojuegos en los 90's", font_size=28, color=WHITE).to_edge(UP, buff=0.2)
    scene.play(
        FadeOut(img_ts1), FadeOut(img_ts2),
        Transform(text_top, text_games),
        *[FadeIn(img) for img in g1_imgs],
        *[FadeIn(cap) for cap in g1_caps],
    )
    scene.next_slide()

    # --- Videojuegos grupo 2 ---
    g2_imgs = [
        ImageMobject("goldeneye").set_height(3).move_to([xs[0], -0.5, 0]),
        ImageMobject("halflife").set_height(3).move_to([xs[1], -0.5, 0]),
        ImageMobject("silenthill").set_height(3).move_to([xs[2], -0.5, 0]),
    ]
    g2_caps = [
        Text("Goldeneye 007 (1997)", font_size=20, color=WHITE).next_to(g2_imgs[0], DOWN, buff=0.2),
        Text("Half Life (1998)", font_size=20, color=WHITE).next_to(g2_imgs[1], DOWN, buff=0.2),
        Text("Silent Hill (1999)", font_size=20, color=WHITE).next_to(g2_imgs[2], DOWN, buff=0.2),
    ]
    scene.play(
        *[FadeOut(img) for img in g1_imgs],
        *[FadeOut(cap) for cap in g1_caps],
        *[FadeIn(img) for img in g2_imgs],
        *[FadeIn(cap) for cap in g2_caps],
    )

    return {
    **ctx,
    "objects": [text_top, *g2_imgs, *g2_caps]
}


@app.function
def motivation_slide(scene, ctx):
    scene.play(*[FadeOut(obj) for obj in ctx["objects"]])

    heading = Text("Motivación", font_size=72, color=WHITE)
    heading.move_to(ORIGIN)
    scene.play(Write(heading))
    scene.next_slide()

    scene.play(heading.animate.scale(0.4).to_corner(UP + LEFT, buff=0.4))

    cpu_sq = Square(side_length=2.5, color=WHITE).shift(LEFT * 3.5)
    cpu_lbl = Text("CPU", font_size=36, color=WHITE).move_to(cpu_sq)
    gpu_sq = Square(side_length=2.5, color=WHITE).shift(RIGHT * 3.5)
    gpu_lbl = Text("GPU", font_size=36, color=WHITE).move_to(gpu_sq)
    cable = Line(cpu_sq.get_right(), gpu_sq.get_left(), stroke_width=8, color=WHITE)
    pci_lbl = Text("PCI", font_size=24, color=WHITE).next_to(cable, UP, buff=0.2)

    scene.play(FadeIn(cpu_sq), FadeIn(cpu_lbl), FadeIn(gpu_sq), FadeIn(gpu_lbl))
    scene.play(Create(cable), FadeIn(pci_lbl))

    scene.next_slide(loop=True)

    dots_lr = [Dot(color=YELLOW, radius=0.08).move_to(cable.get_start()) for _ in range(3)]
    scene.play(
        LaggedStart(*[MoveAlongPath(d, Line(cable.get_start(), cable.get_end())) for d in dots_lr], lag_ratio=0.3),
        run_time=2.5,
    )
    scene.remove(*dots_lr)
    dots_rl = [Dot(color=YELLOW, radius=0.08).move_to(cable.get_end()) for _ in range(3)]
    scene.play(
        LaggedStart(*[MoveAlongPath(d, Line(cable.get_end(), cable.get_start())) for d in dots_rl], lag_ratio=0.3),
        run_time=2.5,
    )
    scene.remove(*dots_rl)

    return {"heading": heading, "cpu_sq": cpu_sq, "cpu_lbl": cpu_lbl, "gpu_sq": gpu_sq, "gpu_lbl": gpu_lbl, "cable": cable, "pci_lbl": pci_lbl}


@app.function
def primitives_slide(scene, ctx):
    scene.play(
        FadeOut(ctx["cpu_sq"]), FadeOut(ctx["cpu_lbl"]),
        FadeOut(ctx["gpu_sq"]), FadeOut(ctx["gpu_lbl"]),
        FadeOut(ctx["cable"]), FadeOut(ctx["pci_lbl"]),
    )

    heading = ctx["heading"]
    prim_title = Text("- Primitivas de OpenGL", font_size=29, color=WHITE)
    prim_title.next_to(heading, RIGHT, buff=0.4)
    scene.play(FadeIn(prim_title))
    scene.next_slide()

    # --- GL_POINTS ---
    cloud_center = LEFT * 4.2 + UP * 0.3
    cloud_offsets = [
        UP*0.8 + LEFT*0.5, UP*0.9, UP*0.6 + RIGHT*0.6,
        LEFT*0.9 + UP*0.1, RIGHT*0.4 + UP*0.2,
        DOWN*0.4 + LEFT*0.3, RIGHT*0.8 + DOWN*0.2,
        DOWN*0.8 + LEFT*0.7, DOWN*0.9 + RIGHT*0.1,
    ]
    pt_dots = VGroup(*[
        Dot(point=cloud_center + off, radius=0.08, color=WHITE)
        for off in cloud_offsets
    ])
    lbl_points = Text("GL_POINTS", font="Consolas", font_size=22, color=WHITE).next_to(pt_dots, DOWN, buff=0.35)

    # --- GL_LINES ---
    lc = ORIGIN
    gl_lines = VGroup(
        Line(lc + LEFT*0.7 + UP*0.9,   lc + RIGHT*0.6 + DOWN*0.7, color=WHITE, stroke_width=3),
        Line(lc + LEFT*0.9 + DOWN*0.2, lc + RIGHT*0.8 + UP*0.5,   color=WHITE, stroke_width=3),
        Line(lc + LEFT*0.2 + UP*0.6,   lc + RIGHT*0.5 + DOWN*0.7, color=WHITE, stroke_width=3),
    )
    lbl_lines = Text("GL_LINES", font="Consolas", font_size=22, color=WHITE).next_to(gl_lines, DOWN, buff=0.35)

    # --- GL_TRIANGLES ---
    tc = RIGHT * 4.2
    tri = Polygon(
        tc + UP * 1.0,
        tc + LEFT * 0.9 + DOWN * 0.7,
        tc + RIGHT * 0.9 + DOWN * 0.7,
        color=WHITE, stroke_width=3,
    )
    lbl_tri = Text("GL_TRIANGLES", font="Consolas", font_size=22, color=WHITE).next_to(tri, DOWN, buff=0.35)

    scene.play(LaggedStart(*[FadeIn(d) for d in pt_dots], lag_ratio=0.12), FadeIn(lbl_points))
    scene.play(Create(gl_lines), FadeIn(lbl_lines))
    scene.play(Create(tri), FadeIn(lbl_tri))
    scene.next_slide()

    scene.play(
        FadeOut(pt_dots), FadeOut(lbl_points),
        FadeOut(gl_lines), FadeOut(lbl_lines),
        FadeOut(tri), FadeOut(lbl_tri),
    )

    # --- GL_TRIANGLE_STRIP ---
    import numpy as np
    sc = LEFT * 2.5
    sv = [
        sc + LEFT*1.7 + UP*0.8,
        sc + LEFT*0.9 + DOWN*0.8,
        sc + LEFT*0.1 + UP*0.8,
        sc + RIGHT*0.7 + DOWN*0.8,
        sc + RIGHT*1.5 + UP*0.8,
        sc + RIGHT*2.3 + DOWN*0.8,
    ]
    strip_tris = VGroup(
        Polygon(sv[0], sv[1], sv[2], color=WHITE, stroke_width=3),
        Polygon(sv[1], sv[2], sv[3], color=WHITE, stroke_width=3),
        Polygon(sv[2], sv[3], sv[4], color=WHITE, stroke_width=3),
        Polygon(sv[3], sv[4], sv[5], color=WHITE, stroke_width=3),
    )
    lbl_strip = Text("GL_TRIANGLE_STRIP", font="Consolas", font_size=22, color=WHITE).next_to(strip_tris, DOWN, buff=0.35)

    # --- GL_TRIANGLE_FAN ---
    fc = RIGHT * 2.5
    r = 1.1
    fan_pts = [
        fc + np.array([r * np.cos(i * 2 * np.pi / 5), r * np.sin(i * 2 * np.pi / 5), 0])
        for i in range(6)
    ]
    fan_tris = VGroup(*[
        Polygon(fc, fan_pts[i], fan_pts[i + 1], color=WHITE, stroke_width=3)
        for i in range(5)
    ])
    lbl_fan = Text("GL_TRIANGLE_FAN", font="Consolas", font_size=22, color=WHITE).next_to(fan_tris, DOWN, buff=0.35)

    scene.play(Create(strip_tris), FadeIn(lbl_strip))
    scene.play(Create(fan_tris), FadeIn(lbl_fan))
    scene.next_slide()

    # Traer strip al centro, quitar fan y etiquetas
    scene.play(
        FadeOut(fan_tris), FadeOut(lbl_fan), FadeOut(lbl_strip),
        strip_tris.animate.move_to(ORIGIN),
    )
    scene.next_slide()

    # Mostrar giros alternados
    winding_colors  = [BLUE, RED, BLUE, RED]
    winding_symbols = ["↺", "↻", "↺", "↻"]

    fills = []
    syms  = []
    for i in range(4):
        color = winding_colors[i]
        fill = strip_tris[i].copy().set_fill(color, opacity=0.35).set_stroke(color, width=2)
        sym  = Text(winding_symbols[i], font_size=36, color=color).move_to(strip_tris[i].get_center())
        scene.play(FadeIn(fill), Write(sym))
        fills.append(fill)
        syms.append(sym)
        scene.next_slide()

    # Romper el orden: triángulo 3 (índice 2) debería ser ↺ pero lo ponemos ↻
    broken_fill = strip_tris[2].copy().set_fill(YELLOW, opacity=0.5).set_stroke(YELLOW, width=2)
    broken_sym  = Text("↻", font_size=36, color=YELLOW).move_to(strip_tris[2].get_center())
    scene.play(Transform(fills[2], broken_fill), Transform(syms[2], broken_sym))

    return {
        "objects": [heading, prim_title, strip_tris, *fills, *syms]
    }


@app.function
def igl_slide(scene, ctx):
    import numpy as np
    scene.play(*[FadeOut(obj) for obj in ctx["objects"]])

    heading = Text("IGL — Triángulo Degenerado", font_size=34, color=WHITE)
    heading.to_edge(UP, buff=0.4)
    scene.play(Write(heading))
    scene.next_slide()

    y_top, y_bot = 0.8, -0.8
    pos = {
        "A": np.array([-3.5,  y_top, 0]),
        "B": np.array([-1.75, y_bot, 0]),
        "C": np.array([ 0.0,  y_top, 0]),
        "D": np.array([ 1.75, y_bot, 0]),
        "E": np.array([ 3.5,  y_top, 0]),
    }

    v_dots = {k: Dot(point=v, radius=0.12, color=WHITE) for k, v in pos.items()}
    v_lbls = {}
    for k, v in pos.items():
        side = UP if v[1] > 0 else DOWN
        v_lbls[k] = Text(k, font_size=24, color=WHITE).next_to(v_dots[k], side, buff=0.15)

    seq = Text("Secuencia:  A  B  C  C  D  E", font="Consolas", font_size=22, color=WHITE)
    seq.to_edge(DOWN, buff=0.5)

    scene.play(*[FadeIn(d) for d in v_dots.values()], *[Write(l) for l in v_lbls.values()])
    scene.play(Write(seq))

    dup_ring = Circle(radius=0.22, color=YELLOW, stroke_width=3).move_to(pos["C"])
    scene.play(Create(dup_ring))
    scene.next_slide()

    # T1: (A, B, C) → real, CCW ↺
    t1 = Polygon(pos["A"], pos["B"], pos["C"], color=BLUE, stroke_width=3).set_fill(BLUE, opacity=0.3)
    t1_lbl = Text("↺", font_size=32, color=BLUE).move_to(t1.get_center())
    scene.play(Create(t1), Write(t1_lbl))
    scene.next_slide()

    # T2: (B, C, C) → degenerado, colapsa a la arista B-C
    t2 = DashedLine(pos["B"], pos["C"], color=RED, stroke_width=4).set_z_index(2)
    scene.play(Create(t2))
    scene.next_slide()

    # T3: (C, C, D) → degenerado, colapsa a la arista C-D
    t3 = DashedLine(pos["C"], pos["D"], color=RED, stroke_width=4).set_z_index(2)
    deg_lbl = Text("Área = 0", font_size=20, color=RED).next_to(v_dots["C"], DOWN, buff=0.55)
    scene.play(Create(t3), Write(deg_lbl))
    scene.next_slide()

    # Arista B-D: cierra la zona degenerada
    t_bd = DashedLine(pos["B"], pos["D"], color=RED, stroke_width=4).set_z_index(2)
    scene.play(Create(t_bd))
    scene.next_slide()

    # T4: (C, D, E) → real, CCW ↺ — mismo giro que T1
    t4 = Polygon(pos["C"], pos["D"], pos["E"], color=BLUE, stroke_width=3).set_fill(BLUE, opacity=0.3)
    t4_lbl = Text("↺", font_size=32, color=BLUE).move_to(t4.get_center())
    scene.play(Create(t4), Write(t4_lbl))

    return {
        "objects": [
            heading, dup_ring,
            t1, t1_lbl, t2, t3, t_bd, deg_lbl, t4, t4_lbl, seq,
            *v_dots.values(), *v_lbls.values(),
        ]
    }


@app.function
def graph_slide(scene, ctx):
    import numpy as np

    scene.play(*[FadeOut(m) for m in scene.mobjects])

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


@app.function
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


@app.function
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

    scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=0.8)
    return {}


@app.function
# -*- coding: utf-8 -*-
# holes_slide — nodo se expande en 3 puntos (sin flechas), aristas con Transform

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


@app.function
# -*- coding: utf-8 -*-
# paper_slide — fiel al paper (Fig 3 y 4)
#
# Gráfica cúbica: nodo L y nodo R conectados por arista central,
# cada uno con 2 ramas externas (grado 3).
#
# Transformación de la arista central L-R:
#   - g = arc vertex inferior (punta del V de abajo)
#   - h = arc vertex superior (punta del V de arriba)
#   - b,c = node vertices del nodo L en las bocas del túnel
#   - d,e = node vertices del nodo R en las bocas del túnel
#   - a = node vertex de L hacia sus ramas externas
#   - f = node vertex de R hacia sus ramas externas
#
# Diagonal forzada: g-h (conecta las dos puntas del V)
# Otras diagonales (punteadas): triangularizan el interior

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


@app.function
# -*- coding: utf-8 -*-
# example_paper — Ejemplo de la reducción sobre Q₃


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

    scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=0.8)

    return {
        'heading': None,
        'all_objs': [],
    }


@app.function
def steiner_slide(scene, ctx):
    import numpy as np


    heading = Text("Puntos Steiner", font_size=72, color=WHITE)
    heading.move_to(ORIGIN)
    scene.play(Write(heading))
    scene.next_slide()

    heading_small = Text("Puntos Steiner", font_size=28, color=WHITE)
    heading_small.to_corner(UP + LEFT, buff=0.4)
    scene.play(Transform(heading, heading_small))

    points = [
        np.array([0, 3, 0]),    # A  0
        np.array([0, 1, 0]),    # B  1
        np.array([1, 0, 0]),    # C  2
        np.array([3, 0, 0]),    # D  3
        np.array([4, 1, 0]),    # E  4
        np.array([5, 0, 0]),    # F  5
        np.array([7, 0, 0]),    # G  6
        np.array([8, 1, 0]),    # H  7
        np.array([9, 0, 0]),    # I  8
        np.array([11, 0, 0]),   # J  9
        np.array([12, 1, 0]),   # K  10
        np.array([12, 3, 0]),   # L  11
        np.array([11, 4, 0]),   # M  12
        np.array([9, 4, 0]),    # N  13
        np.array([8, 3, 0]),    # O  14
        np.array([7, 4, 0]),    # P  15
        np.array([5, 4, 0]),    # Q  16
        np.array([4, 3, 0]),    # R  17
        np.array([3, 4, 0]),    # S  18
        np.array([1, 4, 0]),    # T  19
    ]

    polygon = Polygon(*points, color=WHITE, stroke_width=3)
    polygon.move_to(ORIGIN)
    scene.play(Create(polygon))
    scene.next_slide()

    verts = polygon.get_vertices()

    red_region = Polygon(
        verts[0], verts[1], verts[2], verts[3], verts[4], verts[17], verts[18], verts[19],
        color=RED, stroke_width=2
    ).set_fill(RED, opacity=0.5)

    blue_region = Polygon(
        verts[4], verts[5], verts[6], verts[7], verts[14], verts[15], verts[16], verts[17],
        color=BLUE, stroke_width=2
    ).set_fill(BLUE, opacity=0.5)

    yellow_region = Polygon(
        verts[7], verts[8], verts[9], verts[10], verts[11], verts[12], verts[13], verts[14],
        color=YELLOW, stroke_width=2
    ).set_fill(YELLOW, opacity=0.5)

    label = Text("Regiones convexas: k = 3", font_size=24, color=WHITE)
    label.to_corner(DOWN + LEFT, buff=0.5)

    scene.play(FadeIn(red_region), FadeIn(blue_region), FadeIn(yellow_region))
    scene.play(FadeIn(label))
    scene.next_slide()

    # W X Y — puntos intermedios (bbox centro (6,2), sin escala adicional)
    bbox_center = np.array([6.0, 2.0, 0.0])
    w_pos = np.array([2.0,  2.0,  0.0]) - bbox_center   # (-4,  0,   0)
    wx_pos = np.array([6.0,  1.5,  0.0]) - bbox_center  # ( 0, -0.5, 0)
    wy_pos = np.array([10.0, 2.0,  0.0]) - bbox_center  # ( 4,  0,   0)

    w_dot  = Dot(w_pos,  radius=0.13, color=RED).set_z_index(3)
    wx_dot = Dot(wx_pos, radius=0.13, color=WHITE).set_z_index(3)
    wy_dot = Dot(wy_pos, radius=0.13, color=WHITE).set_z_index(3)
    wx_edge = DashedLine(w_pos,  wx_pos, color=WHITE, stroke_width=2, dash_length=0.1)
    wy_edge = DashedLine(wx_pos, wy_pos, color=WHITE, stroke_width=2, dash_length=0.1)

    scene.play(FadeIn(w_dot), FadeIn(wx_dot), FadeIn(wy_dot), Create(wx_edge), Create(wy_edge))
    scene.next_slide()

    scene.play(FadeOut(w_dot), FadeOut(wx_dot), FadeOut(wy_dot), FadeOut(wx_edge), FadeOut(wy_edge))
    scene.next_slide()

    # U y V están en coordenadas del polígono original; el bbox era (0..12, 0..4),
    # centro (6, 2), que move_to(ORIGIN) desplazó a (0,0).
    u_pos = np.array([4.0, 2.0, 0.0]) - bbox_center   # (-2, 0, 0)
    v_pos = np.array([8.0, 2.0, 0.0]) - bbox_center   # ( 2, 0, 0)

    u_dot = Dot(u_pos, radius=0.13, color=WHITE).set_z_index(3)
    v_dot = Dot(v_pos, radius=0.13, color=WHITE).set_z_index(3)
    u_label = Text("", font_size=22, color=WHITE).next_to(u_dot, DOWN, buff=0.15)
    v_label = Text("", font_size=22, color=WHITE).next_to(v_dot, DOWN, buff=0.15)

    uv_rect = RoundedRectangle(corner_radius=0.6, width=5.2, height=1.4, color=WHITE, stroke_width=2)
    uv_rect.move_to(ORIGIN)

    scene.play(FadeIn(u_dot), FadeIn(v_dot), Write(u_label), Write(v_label))
    scene.next_slide()

    # Aristas desde U → S T A B C D
    edges_u_left = [
        DashedLine(u_pos, verts[i], color=WHITE, stroke_width=1.5, dash_length=0.1)
        for i in [18, 19, 0, 1, 2, 3]
    ]
    scene.play(LaggedStart(*[Create(e) for e in edges_u_left], lag_ratio=0.25))
    scene.next_slide()

    # Aristas desde U → F G H V O P Q
    edges_u_mid = [
        DashedLine(u_pos, target, color=WHITE, stroke_width=1.5, dash_length=0.1)
        for target in [verts[5], verts[6], verts[7], v_pos, verts[14], verts[15], verts[16]]
    ]
    scene.play(LaggedStart(*[Create(e) for e in edges_u_mid], lag_ratio=0.25))
    scene.next_slide()

    # Aristas desde V → I J K L M N
    edges_v_right = [
        DashedLine(v_pos, verts[i], color=WHITE, stroke_width=1.5, dash_length=0.1)
        for i in [8, 9, 10, 11, 12, 13]
    ]
    scene.play(LaggedStart(*[Create(e) for e in edges_v_right], lag_ratio=0.25))

    steiner_label = Text("Puntos Steiner: k-1=2", font_size=24, color=WHITE)
    steiner_label.to_corner(DOWN + RIGHT, buff=0.5)
    scene.play(FadeIn(steiner_label), Create(uv_rect))
    scene.next_slide()

    scene.play(FadeOut(uv_rect))

    new_u_pos = verts[17]
    new_edges_u_left = [
        DashedLine(new_u_pos, verts[i], color=WHITE, stroke_width=1.5, dash_length=0.1)
        for i in [18, 19, 0, 1, 2, 3]
    ]
    new_edges_u_mid = [
        DashedLine(new_u_pos, target, color=WHITE, stroke_width=1.5, dash_length=0.1)
        for target in [verts[5], verts[6], verts[7], v_pos, verts[14], verts[15], verts[16]]
    ]

    new_steiner = Text("Puntos Steiner: k-2=1", font_size=24, color=WHITE)
    new_steiner.to_corner(DOWN + RIGHT, buff=0.5)
    scene.play(
        u_dot.animate.move_to(new_u_pos),
        Transform(steiner_label, new_steiner),
        *[Transform(old, new) for old, new in zip(edges_u_left, new_edges_u_left)],
        *[Transform(old, new) for old, new in zip(edges_u_mid, new_edges_u_mid)],
    )
    scene.next_slide()

    return {
        "heading": heading,
        "polygon": polygon,
        "red_region": red_region,
        "blue_region": blue_region,
        "yellow_region": yellow_region,
        "label": label,
        "u_dot": u_dot, "v_dot": v_dot,
        "u_label": u_label, "v_label": v_label,
        "edges_u_left": edges_u_left,
        "edges_u_mid": edges_u_mid,
        "edges_v_right": edges_v_right,
        "steiner_label": steiner_label,
    }


@app.function
def steiner_slide_2(scene, ctx):
    import numpy as np

    scene.play(
        FadeOut(ctx["polygon"]),
        FadeOut(ctx["red_region"]),
        FadeOut(ctx["blue_region"]),
        FadeOut(ctx["yellow_region"]),
        FadeOut(ctx["u_dot"]),
        FadeOut(ctx["v_dot"]),
        FadeOut(ctx["u_label"]),
        FadeOut(ctx["v_label"]),
        *[FadeOut(e) for e in ctx["edges_u_left"]],
        *[FadeOut(e) for e in ctx["edges_u_mid"]],
        *[FadeOut(e) for e in ctx["edges_v_right"]],
    )

    points = [
        np.array([0,     0,    0]),   # A  0
        np.array([0,     7,    0]),   # B  1
        np.array([2,     7,    0]),   # C  2
        np.array([2,     2,    0]),   # D  3
        np.array([4,     2,    0]),   # E  4
        np.array([4,     7,    0]),   # F  5
        np.array([6,     7,    0]),   # G  6
        np.array([6,     2,    0]),   # H  7
        np.array([8,     2,    0]),   # I  8
        np.array([8,     7,    0]),   # J  9
        np.array([10,    7,    0]),   # K  10
        np.array([10,    2,    0]),   # L  11
        np.array([12,    2,    0]),   # M  12
        np.array([12,    7,    0]),   # N  13
        np.array([14,    7,    0]),   # O  14
        np.array([14,    2,    0]),   # P  15
        np.array([16,    2,    0]),   # Q  16
        np.array([16,    7,    0]),   # R  17
        np.array([18,    7,    0]),   # S  18
        np.array([18,    0,    0]),   # T  19
    ]

    polygon2 = Polygon(*points, color=WHITE, stroke_width=3)
    polygon2.move_to(ORIGIN)
    polygon2.scale(0.65)
    scene.play(Create(polygon2))
    scene.next_slide()

    v = polygon2.get_vertices()

    red_region = Polygon(
        v[0], v[1], v[2], v[3],
        color=RED, stroke_width=2,
    ).set_fill(RED, opacity=0.5)

    gold_region = Polygon(
        v[0], v[3], v[4], v[7], v[8], v[11], v[12], v[15], v[16], v[19],
        color=GOLD, stroke_width=2,
    ).set_fill(GOLD, opacity=0.5)

    yellow_region = Polygon(
        v[4], v[5], v[6], v[7],
        color=YELLOW, stroke_width=2,
    ).set_fill(YELLOW, opacity=0.5)

    green_region = Polygon(
        v[8], v[9], v[10], v[11],
        color=GREEN, stroke_width=2,
    ).set_fill(GREEN, opacity=0.5)

    teal_region = Polygon(
        v[12], v[13], v[14], v[15],
        color=TEAL, stroke_width=2,
    ).set_fill(TEAL, opacity=0.5)

    blue_region = Polygon(
        v[16], v[17], v[18], v[19],
        color=BLUE, stroke_width=2,
    ).set_fill(BLUE, opacity=0.5)

    scene.play(
        FadeIn(red_region), FadeIn(gold_region), FadeIn(yellow_region),
        FadeIn(green_region), FadeIn(teal_region), FadeIn(blue_region),
    )

    new_label = Text("Regiones convexas: k = 6", font_size=24, color=WHITE)
    new_label.to_corner(DOWN + LEFT, buff=0.5)
    scene.play(Transform(ctx["label"], new_label))
    scene.next_slide()

    # Posiciones de los puntos Steiner en coordenadas de escena
    # bbox original: (0..18, 0..7) → centro (9, 3.5); luego scale 0.65
    def sc(px, py):
        return (np.array([px, py, 0.0]) - np.array([9.0, 3.5, 0.0])) * 0.65

    u_pos = sc(1,  1)
    v_pos = sc(5,  2)
    x_pos = sc(9,  2)
    y_pos = sc(13, 2)
    z_pos = sc(17, 1)

    u_dot = Dot(u_pos, radius=0.10, color=WHITE).set_z_index(3)
    v_dot = Dot(v_pos, radius=0.10, color=WHITE).set_z_index(3)
    x_dot = Dot(x_pos, radius=0.10, color=WHITE).set_z_index(3)
    y_dot = Dot(y_pos, radius=0.10, color=WHITE).set_z_index(3)
    z_dot = Dot(z_pos, radius=0.10, color=WHITE).set_z_index(3)

    new_steiner = Text("Puntos Steiner: k-1=5", font_size=24, color=WHITE)
    new_steiner.to_corner(DOWN + RIGHT, buff=0.5)

    scene.play(
        FadeIn(u_dot), FadeIn(v_dot), FadeIn(x_dot), FadeIn(y_dot), FadeIn(z_dot),
        Transform(ctx["steiner_label"], new_steiner),
    )
    scene.next_slide()

    def edge(a, b):
        return DashedLine(a, b, color=WHITE, stroke_width=1.5, dash_length=0.1)

    # Batch 1: aristas "locales" de cada punto Steiner a sus dos vecinos de región
    batch1 = [
        edge(u_pos, v[0]),   # U→A
        edge(u_pos, v[3]),   # U→D
        edge(v_pos, v[4]),   # V→E
        edge(v_pos, v[7]),   # V→H
        edge(x_pos, v[8]),   # X→I
        edge(x_pos, v[11]),  # X→L
        edge(y_pos, v[12]),  # Y→M
        edge(y_pos, v[15]),  # Y→P
        edge(z_pos, v[16]),  # Z→Q
        edge(z_pos, v[19]),  # Z→T
    ]
    scene.play(LaggedStart(*[Create(e) for e in batch1], lag_ratio=0.15))
    scene.next_slide()

    # Batch 2: aristas largas desde U
    batch2 = [
        edge(u_pos, v[1]),   # U→B
        edge(u_pos, v[2]),   # U→C
        edge(u_pos, v[4]),   # U→E
        edge(u_pos, v_pos),  # U→V
        edge(u_pos, v[7]),   # U→H
        edge(u_pos, v[8]),   # U→I
        edge(u_pos, x_pos),  # U→X
        edge(u_pos, v[11]),  # U→L
        edge(u_pos, v[12]),  # U→M
        edge(u_pos, y_pos),  # U→Y
        edge(u_pos, v[15]),  # U→P
        edge(u_pos, v[16]),  # U→Q
        edge(u_pos, z_pos),  # U→Z
        edge(u_pos, v[19]),  # U→T
    ]
    scene.play(LaggedStart(*[Create(e) for e in batch2], lag_ratio=0.1))
    scene.next_slide()

    # Batch 3: V→F, V→G
    batch3 = [edge(v_pos, v[5]), edge(v_pos, v[6])]
    scene.play(LaggedStart(*[Create(e) for e in batch3], lag_ratio=0.3))
    scene.next_slide()

    # Batch 4: X→J, X→K
    batch4 = [edge(x_pos, v[9]), edge(x_pos, v[10])]
    scene.play(LaggedStart(*[Create(e) for e in batch4], lag_ratio=0.3))
    scene.next_slide()

    # Batch 5: Y→N, Y→O
    batch5 = [edge(y_pos, v[13]), edge(y_pos, v[14])]
    scene.play(LaggedStart(*[Create(e) for e in batch5], lag_ratio=0.3))
    scene.next_slide()

    # Batch 6: Z→R, Z→S
    batch6 = [edge(z_pos, v[17]), edge(z_pos, v[18])]
    scene.play(LaggedStart(*[Create(e) for e in batch6], lag_ratio=0.3))
    scene.next_slide()

    # Remover todas las aristas punteadas
    all_edges = batch1 + batch2 + batch3 + batch4 + batch5 + batch6
    scene.play(*[FadeOut(e) for e in all_edges])
    scene.next_slide()

    # Bajar V, X, Y una unidad en coords originales → 0.75 en coords de escena
    new_v_pos = sc(5,  1)
    new_x_pos = sc(9,  1)
    new_y_pos = sc(13, 1)

    scene.play(
        v_dot.animate.shift(DOWN * 0.75),
        x_dot.animate.shift(DOWN * 0.75),
        y_dot.animate.shift(DOWN * 0.75),
    )
    scene.next_slide()

    # Nuevas aristas en un solo paso
    new_edges = [
        # U → A B C D E V
        edge(u_pos,    v[0]),      edge(u_pos,    v[1]),
        edge(u_pos,    v[2]),      edge(u_pos,    v[3]),
        edge(u_pos,    v[4]),      edge(u_pos,    new_v_pos),
        # V → A E F G H I X
        edge(new_v_pos, v[0]),     edge(new_v_pos, v[4]),
        edge(new_v_pos, v[5]),     edge(new_v_pos, v[6]),
        edge(new_v_pos, v[7]),     edge(new_v_pos, v[8]),
        edge(new_v_pos, new_x_pos),
        # X → A I J K L M Y T
        edge(new_x_pos, v[0]),     edge(new_x_pos, v[8]),
        edge(new_x_pos, v[9]),     edge(new_x_pos, v[10]),
        edge(new_x_pos, v[11]),    edge(new_x_pos, v[12]),
        edge(new_x_pos, new_y_pos), edge(new_x_pos, v[19]),
        # Y → M N O P Q Z T
        edge(new_y_pos, v[12]),    edge(new_y_pos, v[13]),
        edge(new_y_pos, v[14]),    edge(new_y_pos, v[15]),
        edge(new_y_pos, v[16]),    edge(new_y_pos, z_pos),
        edge(new_y_pos, v[19]),
        # Z → Q R S T
        edge(z_pos, v[16]),        edge(z_pos, v[17]),
        edge(z_pos, v[18]),        edge(z_pos, v[19]),
    ]
    scene.play(LaggedStart(*[Create(e) for e in new_edges], lag_ratio=0.04))
    scene.next_slide()

    return {
        "heading":       ctx["heading"],
        "label":         ctx["label"],
        "steiner_label": ctx["steiner_label"],
        "polygon":       polygon2,
        "regions":       [red_region, gold_region, yellow_region, green_region, teal_region, blue_region],
        "steiner_dots":  [u_dot, v_dot, x_dot, y_dot, z_dot],
        "steiner_edges": new_edges,
    }


@app.function
def steiner_slide_3(scene, ctx):
    import numpy as np

    new_label = Text("Regiones convexas: k = 5", font_size=24, color=WHITE)
    new_label.to_corner(DOWN + LEFT, buff=0.5)
    new_steiner = Text("Puntos Steiner: k=5", font_size=24, color=WHITE)
    new_steiner.to_corner(DOWN + RIGHT, buff=0.5)

    scene.play(
        FadeOut(ctx["polygon"]),
        *[FadeOut(r) for r in ctx["regions"]],
        *[FadeOut(d) for d in ctx["steiner_dots"]],
        *[FadeOut(e) for e in ctx["steiner_edges"]],
        Transform(ctx["label"], new_label),
        Transform(ctx["steiner_label"], new_steiner),
    )

    A = np.array([0, 3, 0])
    B = np.array([2, 0, 0])
    C = np.array([2, 4, 0])
    D = np.array([5, 4, 0])
    E = np.array([5, 2, 0])
    F = np.array([6, 0, 0])
    G = np.array([8, 3, 0])

    # Polygon outline: A→B→F→G→E→D→C→A
    polygon = Polygon(A, B, F, G, E, D, C, color=WHITE, stroke_width=3)
    polygon.move_to(ORIGIN)
    polygon.scale(1.3)
    scene.play(Create(polygon))
    scene.next_slide()

    # Vertices in order: A=0, B=1, F=2, G=3, E=4, D=5, C=6
    v = polygon.get_vertices()

    def dashed(a, b):
        return DashedLine(a, b, color=YELLOW, stroke_width=2, dash_length=0.15)

    dashed_edges = [
        dashed(v[1], v[6]),  # B → C
        dashed(v[6], v[4]),  # C → E
        dashed(v[1], v[4]),  # B → E
        dashed(v[4], v[2]),  # E → F
    ]
    scene.play(LaggedStart(*[Create(e) for e in dashed_edges], lag_ratio=0.3))
    scene.next_slide()

    # Scale polygon and dashed edges by 0.65
    group = VGroup(polygon, *dashed_edges)
    scene.play(group.animate.scale(0.65))
    scene.next_slide()

    # After full scale (1.3 * 0.65 = 0.845), original bbox center was (4, 2)
    def sc(px, py):
        return np.array([(px - 4.0) * 0.845, (py - 2.0) * 0.845, 0.0])

    # Incenter and inradius in original polygon coordinates
    def incenter_inradius(P1, P2, P3):
        a = np.linalg.norm(P2 - P3)
        b = np.linalg.norm(P1 - P3)
        c = np.linalg.norm(P1 - P2)
        I = (a * P1 + b * P2 + c * P3) / (a + b + c)
        area = 0.5 * abs((P2[0]-P1[0])*(P3[1]-P1[1]) - (P2[1]-P1[1])*(P3[0]-P1[0]))
        r = area / ((a + b + c) / 2)
        return I[:2], r

    ic_xy, ic_r = incenter_inradius(A, C, B)
    id_xy, id_r = incenter_inradius(C, B, E)
    ie_xy, ie_r = incenter_inradius(D, C, E)
    ir_xy, ir_r = incenter_inradius(E, F, G)
    is_xy, is_r = incenter_inradius(E, B, F)

    c_center = sc(ic_xy[0], ic_xy[1])
    d_center = sc(id_xy[0], id_xy[1])
    e_center = sc(ie_xy[0], ie_xy[1])
    r_center = sc(ir_xy[0], ir_xy[1])
    s_center = sc(is_xy[0], is_xy[1])

    circle_c = Circle(radius=ic_r * 0.845, color=BLUE, stroke_width=2).move_to(c_center)
    dot_c = Dot(c_center, radius=0.08, color=BLUE).set_z_index(3)

    circle_d = Circle(radius=id_r * 0.845, color=RED, stroke_width=2).move_to(d_center)
    dot_d = Dot(d_center, radius=0.08, color=RED).set_z_index(3)

    circle_e = Circle(radius=ie_r * 0.845, color=GREEN, stroke_width=2).move_to(e_center)
    dot_e = Dot(e_center, radius=0.08, color=GREEN).set_z_index(3)

    circle_r = Circle(radius=ir_r * 0.845, color=TEAL, stroke_width=2).move_to(r_center)
    dot_r = Dot(r_center, radius=0.08, color=TEAL).set_z_index(3)

    circle_s = Circle(radius=is_r * 0.845, color=GOLD, stroke_width=2).move_to(s_center)
    dot_s = Dot(s_center, radius=0.08, color=GOLD).set_z_index(3)

    scene.play(
        LaggedStart(
            Create(circle_c), FadeIn(dot_c),
            Create(circle_d), FadeIn(dot_d),
            Create(circle_e), FadeIn(dot_e),
            Create(circle_r), FadeIn(dot_r),
            Create(circle_s), FadeIn(dot_s),
            lag_ratio=0.4,
        )
    )
    scene.next_slide()

    # Fade out circles, keep center dots
    scene.play(
        FadeOut(circle_c), FadeOut(circle_d), FadeOut(circle_e),
        FadeOut(circle_r), FadeOut(circle_s),
    )
    scene.next_slide()

    # Vertex positions in scene coords after full scale
    A_pos = sc(0, 3)
    B_pos = sc(2, 0)
    C_pos = sc(2, 4)
    D_pos = sc(5, 4)
    E_pos = sc(5, 2)
    F_pos = sc(6, 0)
    G_pos = sc(8, 3)

    def bdash(a, b):
        return DashedLine(a, b, color=BLUE, stroke_width=1.5, dash_length=0.12)

    center_edges = [
        bdash(c_center, A_pos), bdash(c_center, B_pos), bdash(c_center, C_pos),
        bdash(d_center, C_pos), bdash(d_center, B_pos), bdash(d_center, E_pos),
        bdash(e_center, D_pos), bdash(e_center, C_pos), bdash(e_center, E_pos),
        bdash(r_center, E_pos), bdash(r_center, F_pos), bdash(r_center, G_pos),
        bdash(s_center, F_pos), bdash(s_center, B_pos), bdash(s_center, E_pos),
    ]
    scene.play(LaggedStart(*[Create(e) for e in center_edges], lag_ratio=0.15))
    scene.next_slide()

    # Red dashed edges between circumcenters
    def rdash(a, b):
        return DashedLine(a, b, color=RED, stroke_width=2, dash_length=0.12)

    red_edges = [
        rdash(c_center, d_center),
        rdash(d_center, e_center),
        rdash(d_center, s_center),
        rdash(s_center, r_center),
    ]
    scene.play(LaggedStart(*[Create(e) for e in red_edges], lag_ratio=0.3))
    scene.next_slide()

    # Fade out yellow dashed edges
    scene.play(*[FadeOut(e) for e in dashed_edges])
    scene.next_slide()

    return {
        "heading":       ctx["heading"],
        "label":         ctx["label"],
        "steiner_label": ctx["steiner_label"],
        "polygon":       polygon,
        "dashed_edges":  dashed_edges,
        "circles":       [circle_c, circle_d, circle_e, circle_r, circle_s],
        "circle_dots":   [dot_c, dot_d, dot_e, dot_r, dot_s],
        "center_edges":  center_edges,
        "red_edges":     red_edges,
    }


@app.function
def steiner_slide_4(scene, ctx):
    import numpy as np

    scene.play(
        FadeOut(ctx["polygon"]),
        FadeOut(ctx["label"]),
        FadeOut(ctx["steiner_label"]),
        *[FadeOut(d) for d in ctx["circle_dots"]],
        *[FadeOut(e) for e in ctx["center_edges"]],
        *[FadeOut(e) for e in ctx["red_edges"]],
    )

    A = np.array([0,  0, 0])
    B = np.array([0,  2, 0])
    C = np.array([4,  4, 0])
    D = np.array([8,  2, 0])
    E = np.array([12, 4, 0])
    F = np.array([16, 2, 0])
    G = np.array([16, 0, 0])
    H = np.array([12, 2, 0])
    I = np.array([8,  0, 0])
    J = np.array([4,  2, 0])

    # bbox: x 0..16 center 8, y 0..4 center 2; scale 0.7
    def sc(px, py):
        return np.array([(px - 8.0) * 0.7, (py - 2.0) * 0.7, 0.0])

    polygon = Polygon(A, B, C, D, E, F, G, H, I, J, color=WHITE, stroke_width=3)
    polygon.move_to(ORIGIN)
    polygon.scale(0.7)
    scene.play(Create(polygon))
    scene.next_slide()

    # Order in get_vertices(): A=0 B=1 C=2 D=3 E=4 F=5 G=6 H=7 I=8 J=9
    v = polygon.get_vertices()

    region_abcj = Polygon(v[0], v[1], v[2], v[9], color=RED,    stroke_width=2).set_fill(RED,    opacity=0.5)
    region_cdij = Polygon(v[2], v[3], v[8], v[9], color=BLUE,   stroke_width=2).set_fill(BLUE,   opacity=0.5)
    region_dehi = Polygon(v[3], v[4], v[7], v[8], color=GREEN,  stroke_width=2).set_fill(GREEN,  opacity=0.5)
    region_efgh = Polygon(v[4], v[5], v[6], v[7], color=YELLOW, stroke_width=2).set_fill(YELLOW, opacity=0.5)

    scene.play(FadeIn(region_abcj), FadeIn(region_cdij), FadeIn(region_dehi), FadeIn(region_efgh))
    scene.next_slide()

    k_pos = sc(4,  3)
    l_pos = sc(8,  1)
    m_pos = sc(12, 3)

    k_dot = Dot(k_pos, radius=0.1, color=WHITE).set_z_index(3)
    l_dot = Dot(l_pos, radius=0.1, color=WHITE).set_z_index(3)
    m_dot = Dot(m_pos, radius=0.1, color=WHITE).set_z_index(3)

    scene.play(FadeIn(k_dot), FadeIn(l_dot), FadeIn(m_dot))
    scene.next_slide()

    A_pos = sc(0,  0)
    B_pos = sc(0,  2)
    D_pos = sc(8,  2)
    E_pos = sc(12, 4)
    F_pos = sc(16, 2)
    G_pos = sc(16, 0)
    H_pos = sc(12, 2)
    I_pos = sc(8,  0)

    def dash(a, b):
        return DashedLine(a, b, color=WHITE, stroke_width=1.5, dash_length=0.1)

    steiner_edges = [
        dash(k_pos, B_pos),  # c:  K→B
        dash(k_pos, A_pos),  # d:  K→A
        dash(k_pos, D_pos),  # e:  K→D
        dash(k_pos, l_pos),  # f1: K→L
        dash(k_pos, I_pos),  # g1: K→I
        dash(l_pos, E_pos),  # h1: L→E
        dash(l_pos, m_pos),  # i1: L→M
        dash(l_pos, H_pos),  # j1: L→H
        dash(m_pos, G_pos),  # k1: M→G
        dash(m_pos, F_pos),  # l1: M→F
    ]
    scene.play(LaggedStart(*[Create(e) for e in steiner_edges], lag_ratio=0.15))
    scene.next_slide()

    # Label "Triángulos = 16"
    tri_label = Text("Triángulos = 16", font_size=24, color=WHITE)
    tri_label.to_corner(DOWN + LEFT, buff=0.5)
    scene.play(FadeIn(tri_label))
    scene.next_slide()

    # Move K to C = (4, 4) and update its incident edges
    new_k_pos = sc(4, 4)
    new_k_edges = [
        dash(new_k_pos, B_pos),  # c:  K→B
        dash(new_k_pos, A_pos),  # d:  K→A
        dash(new_k_pos, D_pos),  # e:  K→D
        dash(new_k_pos, l_pos),  # f1: K→L
        dash(new_k_pos, I_pos),  # g1: K→I
    ]
    scene.play(
        k_dot.animate.move_to(new_k_pos),
        *[Transform(old, new) for old, new in zip(steiner_edges[:5], new_k_edges)],
    )
    scene.next_slide()

    # Update label to "Triángulos = 14"
    new_tri_label = Text("Triángulos = 14", font_size=24, color=WHITE)
    new_tri_label.to_corner(DOWN + LEFT, buff=0.5)
    scene.play(Transform(tri_label, new_tri_label))
    scene.next_slide()

    # Duplicate polygon+regions: shift originals up, fade in copy below
    regions = [region_abcj, region_cdij, region_dehi, region_efgh]
    copy_polygon = polygon.copy()
    copy_regions = [r.copy() for r in regions]
    shift_amount = 1.3

    for obj in [copy_polygon] + copy_regions:
        obj.shift(DOWN * shift_amount)

    scene.play(
        polygon.animate.shift(UP * shift_amount),
        *[r.animate.shift(UP * shift_amount) for r in regions],
        k_dot.animate.shift(UP * shift_amount),
        l_dot.animate.shift(UP * shift_amount),
        m_dot.animate.shift(UP * shift_amount),
        *[e.animate.shift(UP * shift_amount) for e in steiner_edges],
        *[FadeIn(obj) for obj in [copy_polygon] + copy_regions],
    )
    scene.next_slide()

    # Edges on bottom polygon: BJ CJ DJ DI DH HE HF
    cv = copy_polygon.get_vertices()
    # Order: A=0 B=1 C=2 D=3 E=4 F=5 G=6 H=7 I=8 J=9
    copy_edges = [
        dash(cv[1], cv[9]),  # B-J
        dash(cv[2], cv[9]),  # C-J
        dash(cv[3], cv[9]),  # D-J
        dash(cv[3], cv[8]),  # D-I
        dash(cv[3], cv[7]),  # D-H
        dash(cv[7], cv[4]),  # H-E
        dash(cv[7], cv[5]),  # H-F
    ]
    tri_label_right = Text("Triángulos = 8", font_size=24, color=WHITE)
    tri_label_right.to_corner(DOWN + RIGHT, buff=0.5)
    scene.play(
        LaggedStart(*[Create(e) for e in copy_edges], lag_ratio=0.15),
        FadeIn(tri_label_right),
    )
    scene.next_slide()

    return {
        "heading":         ctx["heading"],
        "polygon":         polygon,
        "regions":         regions,
        "steiner_dots":    [k_dot, l_dot, m_dot],
        "steiner_edges":   steiner_edges,
        "tri_label":       tri_label,
        "copy_polygon":    copy_polygon,
        "copy_regions":    copy_regions,
        "copy_edges":      copy_edges,
        "tri_label_right": tri_label_right,
    }


@app.function
def steiner_complejidad(scene, ctx):
    if "polygon" in ctx:
        scene.play(
            FadeOut(ctx["polygon"]),
            FadeOut(ctx["copy_polygon"]),
            FadeOut(ctx["tri_label"]),
            FadeOut(ctx["tri_label_right"]),
            *[FadeOut(r) for r in ctx["regions"]],
            *[FadeOut(d) for d in ctx["steiner_dots"]],
            *[FadeOut(e) for e in ctx["steiner_edges"]],
            *[FadeOut(r) for r in ctx["copy_regions"]],
            *[FadeOut(e) for e in ctx["copy_edges"]],
        )
        heading = ctx["heading"]
    else:
        heading = Text("Puntos Steiner", font_size=28, color=WHITE)
        heading.to_corner(UP + LEFT, buff=0.4)
        scene.play(Write(heading))

    complejidad_text = Text("- complejidad temporal", font_size=28, color=WHITE)
    complejidad_text.next_to(heading, RIGHT, buff=0.3)
    scene.play(FadeIn(complejidad_text))
    scene.next_slide()

    item1 = Text("1. Calcula la descomposición convexa mínima del polígono P en k regiones convexas.", font_size=20, color=WHITE)
    item1.next_to(heading, DOWN, buff=0.6, aligned_edge=LEFT)
    scene.play(FadeIn(item1))
    scene.next_slide()

    cl1a = Text("Polígonos simples: con el algoritmo de Chazzelle  ", font_size=20, color=WHITE)
    cl1b = MathTex(r"\ O(n + r^2) \ ", font_size=28, color=BLUE)
    cl1c = Text("con ", font_size=20, color=WHITE)
    cl1d = MathTex(r"\ r \leq n \ ", font_size=28, color=WHITE)
    cl1e = Text(" vértices reflejo (cóncavos)", font_size=20, color=WHITE)
    clar_line1 = VGroup(cl1a, cl1b, cl1c, cl1d, cl1e).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)

    clar_line2 = Text("Polígonos con hoyos: problema NP-duro", font_size=20, color=WHITE)

    cl3a = Text("Sin descomposición mínima estricta: ", font_size=20, color=WHITE)
    cl3b = MathTex(r"\ O(n \log n) \ ", font_size=28, color=BLUE)
    cl3c = Text(" o ", font_size=20, color=WHITE)
    cl3d = MathTex(r"\ O(n) \ ", font_size=28, color=BLUE)
    clar_line3 = VGroup(cl3a, cl3b, cl3c, cl3d).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)

    clarification = VGroup(clar_line1, clar_line2, clar_line3).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    clarification.next_to(item1, DOWN, buff=0.5, aligned_edge=LEFT)
    scene.play(FadeIn(clarification))
    scene.next_slide()

    item2 = Text("2. Construye un árbol generador sobre esas k regiones.", font_size=20, color=WHITE)

    item3 = Text(
        "3. Designa una región raíz y una región adyacente a ella como \"root subareas\".",
        font_size=20, color=WHITE, line_spacing=0.8,
    )
    item4 = Text(
        "4. Coloca un punto Steiner sobre la frontera compartida entre esas dos\n   regiones raíz, y conecta todos los vértices del polígono a ese punto.",
        font_size=20, color=WHITE, line_spacing=0.8,
    )
    item5 = Text(
        "5. Para cada región restante, coloca otro punto Steiner sobre su frontera\n   compartida con la región raíz adyacente.",
        font_size=20, color=WHITE, line_spacing=0.8,
    )

    items = [item1]

    item2.next_to(item1, DOWN, buff=0.35, aligned_edge=LEFT)
    items.append(item2)
    scene.play(FadeOut(clarification), FadeIn(item2))
    scene.next_slide()

    clar2a = Text("Con Prim o Kruskal: ", font_size=20, color=WHITE)
    clar2b = MathTex(r"\ O(n \log n) \ ", font_size=28, color=BLUE)
    clar2 = VGroup(clar2a, clar2b).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
    clar2.next_to(item2, DOWN, buff=0.35, aligned_edge=LEFT)
    scene.play(FadeIn(clar2))
    scene.next_slide()

    item3.next_to(item2, DOWN, buff=0.35, aligned_edge=LEFT)
    items.append(item3)
    scene.play(FadeOut(clar2), FadeIn(item3))
    scene.next_slide()

    item4.next_to(item3, DOWN, buff=0.35, aligned_edge=LEFT)
    items.append(item4)
    scene.play(FadeIn(item4))
    scene.next_slide()

    cl4a = Text("Para k regiones con ", font_size=20, color=WHITE)
    cl4b = MathTex(r"\ n_i \ ", font_size=28, color=WHITE)
    cl4c = Text("vértices: \n", font_size=20, color=WHITE)
    cl4d = MathTex(r"\ \sum_{i=1}^{k} O(n_i) = O(n) \ ", font_size=28, color=BLUE)
    clar4 = VGroup(cl4a, cl4b, cl4c, cl4d).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
    clar4.next_to(item4, DOWN, buff=0.35, aligned_edge=LEFT)
    scene.play(FadeIn(clar4))
    scene.next_slide()

    item5.next_to(item4, DOWN, buff=0.35, aligned_edge=LEFT)
    items.append(item5)
    scene.play(FadeOut(clar4), FadeIn(item5))
    scene.next_slide()

    cl5a = Text("Recorrer con DFS: ", font_size=20, color=WHITE)
    cl5b = MathTex(r"\ O(k) \rightarrow O(n) \ ", font_size=28, color=BLUE)
    clar5 = VGroup(cl5a, cl5b).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
    clar5.next_to(item5, DOWN, buff=0.35, aligned_edge=LEFT)
    scene.play(FadeIn(clar5))
    scene.next_slide()

    big_o_n2 = MathTex(r"O(n^2)", font_size=80, color=BLUE)
    big_o_n2.to_edge(DOWN, buff=0.5)
    scene.play(FadeOut(clar5), FadeIn(big_o_n2))
    scene.next_slide()

    big_o_nlogn = MathTex(r"O(n \log n)", font_size=80, color=BLUE)
    big_o_nlogn.to_edge(DOWN, buff=0.5)
    scene.play(Transform(big_o_n2, big_o_nlogn))
    scene.next_slide()

    return {"heading": heading, "complejidad_text": complejidad_text, "items": items, "big_o": big_o_n2}


@app.function
def steiner_complejidad_espacio(scene, ctx):
    heading = ctx["heading"]

    espacial_text = Text("- complejidad espacial", font_size=28, color=WHITE)
    espacial_text.next_to(heading, RIGHT, buff=0.3)

    fade_items = [FadeOut(item) for item in ctx.get("items", [])]
    if "big_o" in ctx:
        fade_items.append(FadeOut(ctx["big_o"]))
    scene.play(Transform(ctx["complejidad_text"], espacial_text), *fade_items)
    scene.next_slide()

    info_text = Text("Tenemos n vértices y k puntos Steiner", font_size=24, color=WHITE)
    info_text.next_to(heading, DOWN, buff=0.6, aligned_edge=LEFT)
    scene.play(FadeIn(info_text))
    scene.next_slide()

    big_o = MathTex(r"O(n + k)", font_size=80, color=BLUE)
    big_o.to_edge(DOWN, buff=0.5)
    scene.play(FadeIn(big_o))
    scene.next_slide()

    big_o2 = MathTex(r"O(n + k) \rightarrow O(n)", font_size=80, color=BLUE)
    big_o2.to_edge(DOWN, buff=0.5)
    scene.play(Transform(big_o, big_o2))
    scene.next_slide()

    big_o3 = MathTex(r"O(n)", font_size=80, color=BLUE)
    big_o3.to_edge(DOWN, buff=0.5)
    scene.play(Transform(big_o, big_o3))
    scene.next_slide()

    text2 = Text(
        "Para las triangulaciones con polígonos simples, tenemos n-2 triángulos.\n"
        "Cuando añadimos puntos Steiner, las regiones locales son subdivididas",
        font_size=20, color=WHITE, line_spacing=0.8,
    )
    text2.next_to(heading, DOWN, buff=0.6, aligned_edge=LEFT)
    scene.play(Transform(info_text, text2))
    scene.next_slide()

    text3 = Text(
        "Para encontrar el camino hamiltoniano, tenemos que usar el grafo dual de la\n"
        "triangulación, que tienen un nodo por triángulo y una arista por cada adyacencia\n"
        "de triángulos. Hay k nodos y k-1 aristas.",
        font_size=20, color=WHITE, line_spacing=0.8,
    )
    text3.next_to(heading, DOWN, buff=0.6, aligned_edge=LEFT)
    scene.play(Transform(info_text, text3))
    scene.next_slide()

    return {
        "heading": heading,
        "complejidad_text": ctx["complejidad_text"],
        "items": [info_text],
        "big_o": big_o,
    }


@app.function
def steiner_triangulos(scene, ctx):
    heading = ctx["heading"]

    temporal_text = Text("- complejidad temporal", font_size=28, color=WHITE)
    temporal_text.next_to(heading, RIGHT, buff=0.3)

    fade_items = [FadeOut(item) for item in ctx.get("items", [])]
    if "big_o" in ctx:
        fade_items.append(FadeOut(ctx["big_o"]))
    scene.play(Transform(ctx["complejidad_text"], temporal_text), *fade_items)
    scene.next_slide()

    step_text = Text("1 - Calcular el incírculo de cada triángulo", font_size=24, color=WHITE)
    step_text.next_to(heading, DOWN, buff=0.6, aligned_edge=LEFT)
    scene.play(FadeIn(step_text))
    scene.next_slide()

    big_o = MathTex(r"O(k)", font_size=60, color=BLUE)
    big_o.to_edge(DOWN, buff=0.5)
    scene.play(FadeIn(big_o))
    scene.next_slide()

    for label in [
        "2 - Colocar Steiner points y subdividir",
        "3 - Construir la gráfica dual de T",
        "4 - Calcular el árbol generador de peso mínimo de la gráfica dual",
        "5 - Identificar aristas que necesitan flip",
        "6 - Realizar los flips",
    ]:
        new_step = Text(label, font_size=24, color=WHITE)
        new_step.next_to(heading, DOWN, buff=0.6, aligned_edge=LEFT)
        scene.play(Transform(step_text, new_step))
        scene.next_slide()

    scene.play(FadeOut(step_text))
    scene.next_slide()

    center_formula = MathTex(r"k = 2n - h - 2", font_size=60, color=WHITE)
    center_formula.move_to(ORIGIN)
    scene.play(FadeIn(center_formula))
    scene.next_slide()

    center_formula2 = MathTex(r"k = 2n - h - 2 \rightarrow h = 3", font_size=60, color=WHITE)
    center_formula2.move_to(ORIGIN)
    scene.play(Transform(center_formula, center_formula2))
    scene.next_slide()

    center_formula3 = MathTex(r"k = O(n)", font_size=80, color=WHITE)
    center_formula3.move_to(ORIGIN)
    scene.play(Transform(center_formula, center_formula3))
    scene.next_slide()

    big_o2 = MathTex(r"O(n)", font_size=80, color=BLUE)
    big_o2.to_edge(DOWN, buff=0.5)
    scene.play(Transform(big_o, big_o2))
    scene.next_slide()

    return {
        "heading": heading,
        "complejidad_text": ctx["complejidad_text"],
        "items": [center_formula],
        "big_o": big_o,
    }


@app.function
def steiner_conclusiones(scene, ctx):
    heading = ctx["heading"]

    conclusiones_text = Text("- conclusiones", font_size=28, color=WHITE)
    conclusiones_text.next_to(heading, RIGHT, buff=0.3)

    fade_items = [FadeOut(item) for item in ctx.get("items", [])]
    if "big_o" in ctx:
        fade_items.append(FadeOut(ctx["big_o"]))
    if "complejidad_text" in ctx:
        scene.play(Transform(ctx["complejidad_text"], conclusiones_text), *fade_items)
    else:
        scene.play(FadeIn(conclusiones_text), *fade_items)
    scene.next_slide()

    t1 = Text(
        "Con este algoritmo llegamos a una triagulación Hamiltoniana\n"
        "incluso si originalmente no la admite",
        font_size=22, color=WHITE, line_spacing=0.8,
    )
    t1.next_to(heading, DOWN, buff=0.7, aligned_edge=LEFT)

    t2 = Text(
        "La triangulación Hamiltoniana que se genera no es siempre óptima",
        font_size=22, color=WHITE,
    )
    t2.next_to(t1, DOWN, buff=0.5, aligned_edge=LEFT)

    t3 = Text(
        "La triangulación generada nunca va a ser secuencial",
        font_size=22, color=WHITE,
    )
    t3.next_to(t2, DOWN, buff=0.5, aligned_edge=LEFT)

    t4 = Text(
        "Generamos un ciclo Hamiltoniano con k−1 Steiner points",
        font_size=22, color=WHITE,
    )
    t4.next_to(t3, DOWN, buff=0.5, aligned_edge=LEFT)

    t5 = Text(
        "Generamos un camino  Hamiltoniano con k−2 Steiner points",
        font_size=22, color=WHITE,
    )
    t5.next_to(t4, DOWN, buff=0.5, aligned_edge=LEFT)

    scene.play(FadeIn(t1))
    scene.next_slide()
    scene.play(FadeIn(t2))
    scene.next_slide()
    scene.play(FadeIn(t3))
    scene.next_slide()
    scene.play(FadeIn(t4))
    scene.next_slide()
    scene.play(FadeIn(t5))
    scene.next_slide()

    return {"heading": heading, "conclusiones_text": conclusiones_text, "t1": t1, "t2": t2, "t3": t3, "t4": t4, "t5": t5}


@app.function
def section3_slide(scene, ctx):
    import numpy as np

    fade_keys = ["conclusiones_text", "t1", "t2", "t3", "t4", "t5"]
    fade_anims = [FadeOut(ctx[k]) for k in fade_keys if k in ctx]
    if fade_anims:
        scene.play(*fade_anims)

    title = Text(
        "Triangulaciones hamiltonianas\nde un conjunto de puntos",
        font_size=56, color=WHITE,
    ).move_to(ORIGIN)

    scene.play(Write(title))
    scene.next_slide()

    small_title = Text(
        "Triangulaciones hamiltonianas de un conjunto de puntos",
        font_size=20, color=WHITE,
    ).to_corner(UP + LEFT)

    scene.play(Transform(title, small_title))
    scene.next_slide()

    radius = 2.0
    angles = [np.pi / 2 + i * 2 * np.pi / 6 for i in range(6)]
    hex_verts = [np.array([radius * np.cos(a), radius * np.sin(a), 0.0]) for a in angles]

    dots = VGroup(*[Dot(v, color=WHITE) for v in hex_verts])
    scene.play(FadeIn(dots))
    scene.next_slide()

    hex_edges = VGroup(*[
        Line(hex_verts[i], hex_verts[(i + 1) % 6], color=WHITE)
        for i in range(6)
    ])
    scene.play(Create(hex_edges))
    scene.next_slide()

    diagonals = VGroup(*[
        Line(hex_verts[0], hex_verts[j], color=BLUE)
        for j in range(2, 5)
    ])
    scene.play(Create(diagonals))
    scene.next_slide()

    return {**ctx, "title": title, "dots": dots, "hex_edges": hex_edges, "diagonals": diagonals}


@app.function
def insertion_slide(scene, ctx):
    import numpy as np

    fade_keys = ["dots", "hex_edges", "diagonals"]
    fade_anims = [FadeOut(ctx[k]) for k in fade_keys if k in ctx]

    insertion_text = Text("- Inserción", font_size=20, color=WHITE)
    insertion_text.next_to(ctx["title"], RIGHT, buff=0.3)

    scene.play(*fade_anims, FadeIn(insertion_text))
    scene.next_slide()

    scale = 0.4
    raw_coords = [
        (0, 0), (-3, -9), (4, -6.2), (1.5, -6), (-0.6, -6), (-3, -5.4),
        (-2, -4), (6, -4), (0.8, -3.8), (4, -3.8), (-3.5, -2.6), (-1.4, -2.2),
        (1.6, -2), (4.6, -2), (-6, -1.5), (4, -1.6), (-0.6, -1.4), (3, -1),
        (1.6, -0.4), (4, -0.4), (6, 0), (5,1), (-1, 1), (-3, 1),
        (-3.6, 2), (0.6, 0.6), (2.8, 0.8), (-1, 3), (1.5, 4), (-3.5, 4.5),
        (-6, 4.6), (3.5, 5.6), (-1.4, 6.6),
    ]
    _names = [
        "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q",
        "R","S","T","U","V","W","Z","A1","B1","C1","D1","E1","F1","G1","H1","I1",
    ]
    pos = {
        name: np.array([x * scale, y * scale, 0.0])
        for name, (x, y) in zip(_names, raw_coords)
    }

    dot_list = [Dot(pos[n], color=WHITE, radius=0.06) for n in _names]
    point_dots = VGroup(*dot_list)
    scene.play(FadeIn(point_dots))
    scene.next_slide()

    sw = 1.5

    red_edges = VGroup(
        Line(pos["B"],  pos["C"],  color=RED,  stroke_width=sw),
        Line(pos["C"],  pos["H"],  color=RED,  stroke_width=sw),
        Line(pos["H"],  pos["U"],  color=RED,  stroke_width=sw),
        Line(pos["U"],  pos["H1"], color=RED,  stroke_width=sw),
        Line(pos["H1"], pos["I1"], color=RED,  stroke_width=sw),
        Line(pos["I1"], pos["G1"], color=RED,  stroke_width=sw),
        Line(pos["G1"], pos["O"],  color=RED,  stroke_width=sw),
        Line(pos["O"],  pos["B"],  color=RED,  stroke_width=sw),
    )
    scene.play(Create(red_edges))
    scene.next_slide()

    blue_edges = VGroup(
        DashedLine(pos["A"], pos["B"],  color=BLUE, stroke_width=sw),
        DashedLine(pos["A"], pos["C"],  color=BLUE, stroke_width=sw),
        DashedLine(pos["A"], pos["H"],  color=BLUE, stroke_width=sw),
        DashedLine(pos["A"], pos["U"],  color=BLUE, stroke_width=sw),
        DashedLine(pos["A"], pos["H1"], color=BLUE, stroke_width=sw),
        DashedLine(pos["A"], pos["I1"], color=BLUE, stroke_width=sw),
        DashedLine(pos["A"], pos["G1"], color=BLUE, stroke_width=sw),
        DashedLine(pos["A"], pos["O"],  color=BLUE, stroke_width=sw),
    )
    scene.play(dot_list[0].animate.set_color(BLUE), Create(blue_edges))
    scene.next_slide()

    yellow_raw = [
        (0, 5.2), (-4, 4), (-5, 2), (-4, -4), (0, -6), (4, -4), (5, -1), (4, 2),
    ]
    yellow_positions = [np.array([x * scale, y * scale, 0.0]) for x, y in yellow_raw]
    pJ1, pK1, pL1, pM1, pN1, pO1, pP1, pQ1 = yellow_positions

    yellow_dots = VGroup(*[Dot(p, color=YELLOW, radius=0.06) for p in yellow_positions])
    yellow_edges = VGroup(
        Line(pJ1, pK1, color=YELLOW, stroke_width=sw),
        Line(pK1, pL1, color=YELLOW, stroke_width=sw),
        Line(pL1, pM1, color=YELLOW, stroke_width=sw),
        Line(pM1, pN1, color=YELLOW, stroke_width=sw),
        Line(pN1, pO1, color=YELLOW, stroke_width=sw),
        Line(pO1, pP1, color=YELLOW, stroke_width=sw),
        Line(pP1, pQ1, color=YELLOW, stroke_width=sw),
        Line(pQ1, pJ1, color=YELLOW, stroke_width=sw),
    )
    scene.play(FadeIn(yellow_dots), Create(yellow_edges))
    scene.next_slide()

    return {**ctx, "insertion_text": insertion_text, "point_dots": point_dots,
            "red_edges": red_edges, "blue_edges": blue_edges,
            "yellow_dots": yellow_dots, "yellow_edges": yellow_edges,
            "pos": pos, "scale": scale}


@app.function
def insertion_slide_2(scene, ctx):
    import numpy as np

    pos = ctx["pos"]
    scale = ctx["scale"]
    sw = 1.5

    scene.play(FadeOut(ctx["yellow_dots"]), FadeOut(ctx["yellow_edges"]))
    scene.next_slide()

    triangle = Polygon(
        pos["A"], pos["I1"], pos["H1"],
        color=BLUE, fill_color=BLUE, fill_opacity=0.4,
    )
    scene.play(FadeIn(triangle))
    scene.next_slide()

    dashed_white = VGroup(
        DashedLine(pos["E1"], pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["E1"], pos["I1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["E1"], pos["H1"], color=WHITE, stroke_width=sw),
    )
    scene.play(Create(dashed_white))
    scene.next_slide()

    partial_raw = {
        "K1": (-4, 4), "L1": (-5, 2), "M1": (-4, -4),
        "N1": (0, -6),  "O1": (4, -4), "P1": (5, -1), "Q1": (4, 2),
    }
    ypos = {n: np.array([x * scale, y * scale, 0.0]) for n, (x, y) in partial_raw.items()}

    partial_dots = VGroup(*[Dot(ypos[n], color=YELLOW, radius=0.06) for n in ypos])
    partial_edges = VGroup(
        Line(ypos["K1"], ypos["L1"], color=YELLOW, stroke_width=sw),
        Line(ypos["L1"], ypos["M1"], color=YELLOW, stroke_width=sw),
        Line(ypos["M1"], ypos["N1"], color=YELLOW, stroke_width=sw),
        Line(ypos["N1"], ypos["O1"], color=YELLOW, stroke_width=sw),
        Line(ypos["O1"], ypos["P1"], color=YELLOW, stroke_width=sw),
        Line(ypos["P1"], ypos["Q1"], color=YELLOW, stroke_width=sw),
    )
    scene.play(FadeIn(partial_dots), Create(partial_edges))
    scene.next_slide()

    new_raw = {"R1": (2, 4), "S1": (1, 5), "T1": (0, 4)}
    nypos = {n: np.array([x * scale, y * scale, 0.0]) for n, (x, y) in new_raw.items()}

    new_dots = VGroup(*[Dot(nypos[n], color=YELLOW, radius=0.06) for n in nypos])
    new_edges = VGroup(
        Line(ypos["Q1"],   nypos["R1"], color=YELLOW, stroke_width=sw),
        Line(nypos["R1"],  nypos["S1"], color=YELLOW, stroke_width=sw),
        Line(nypos["S1"],  nypos["T1"], color=YELLOW, stroke_width=sw),
        Line(nypos["T1"],  ypos["K1"],  color=YELLOW, stroke_width=sw),
    )
    scene.play(FadeIn(new_dots), Create(new_edges))
    scene.next_slide()

    scene.play(
        FadeOut(partial_dots), FadeOut(new_dots),
        FadeOut(partial_edges), FadeOut(new_edges),
        FadeOut(triangle),
    )
    scene.next_slide()

    tri2 = Polygon(
        pos["A"], pos["O"], pos["G1"],
        color=BLUE, fill_color=BLUE, fill_opacity=0.4,
    )
    scene.play(FadeIn(tri2))
    scene.next_slide()

    dashed_z = VGroup(
        DashedLine(pos["Z"], pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["Z"], pos["O"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["Z"], pos["G1"], color=WHITE, stroke_width=sw),
    )
    scene.play(Create(dashed_z))
    scene.next_slide()

    tri3 = Polygon(
        pos["A"], pos["Z"], pos["G1"],
        color=BLUE, fill_color=BLUE, fill_opacity=0.4,
    )
    scene.play(FadeOut(tri2), FadeIn(tri3))
    scene.next_slide()

    dashed_a1 = VGroup(
        DashedLine(pos["A1"], pos["G1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["A1"], pos["Z"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["A1"], pos["A"],  color=WHITE, stroke_width=sw),
    )
    scene.play(Create(dashed_a1))
    scene.next_slide()

    scene.play(FadeOut(tri3))
    scene.next_slide()

    triang_edges = VGroup(
        DashedLine(pos["D1"], pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["D1"], pos["I1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["D1"], pos["G1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["W"],  pos["D1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["W"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["W"],  pos["G1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["F1"], pos["G1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["F1"], pos["I1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["F1"], pos["D1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["C1"], pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["C1"], pos["U"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["C1"], pos["H1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["B1"], pos["C1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["B1"], pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["B1"], pos["H1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["V"],  pos["C1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["V"],  pos["H1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["V"],  pos["U"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["P"],  pos["U"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["P"],  pos["H"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["P"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["N"],  pos["P"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["N"],  pos["H"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["N"],  pos["U"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["T"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["T"],  pos["P"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["T"],  pos["U"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["S"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["S"],  pos["T"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["S"],  pos["P"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["R"],  pos["S"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["R"],  pos["P"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["R"],  pos["T"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["J"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["J"],  pos["H"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["J"],  pos["C"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["M"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["M"],  pos["J"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["M"],  pos["C"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["I"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["I"],  pos["C"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["I"],  pos["B"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["D"],  pos["I"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["D"],  pos["C"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["D"],  pos["B"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["E"],  pos["I"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["E"],  pos["D"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["E"],  pos["B"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["G"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["G"],  pos["B"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["G"],  pos["O"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["Q"],  pos["B"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["Q"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["Q"],  pos["G"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["F"],  pos["O"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["F"],  pos["B"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["F"],  pos["G"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["K"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["K"],  pos["O"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["K"],  pos["G"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["L"],  pos["K"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["L"],  pos["G"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["L"],  pos["A"],  color=WHITE, stroke_width=sw),
    )
    scene.play(Create(triang_edges))
    scene.next_slide()

    scene.play(
        FadeOut(ctx["blue_edges"]),
        FadeOut(dashed_white),
        FadeOut(dashed_z),
        FadeOut(dashed_a1),
        FadeOut(triang_edges),
    )
    scene.next_slide()

    return {**ctx, "triangle": triangle, "tri2": tri2, "tri3": tri3,
            "dashed_white": dashed_white, "dashed_z": dashed_z, "dashed_a1": dashed_a1,
            "partial_dots": partial_dots, "partial_edges": partial_edges,
            "new_dots": new_dots, "new_edges": new_edges,
            "triang_edges": triang_edges}


@app.function
def onion_slide(scene, ctx):
    pos = ctx["pos"]
    sw = 1.5

    cebolla_text = Text("- Cebolla", font_size=20, color=WHITE)
    cebolla_text.next_to(ctx["title"], RIGHT, buff=0.3)

    scene.play(Transform(ctx["insertion_text"], cebolla_text))
    scene.next_slide()

    onion_edges = VGroup(
        # outer 10-cycle: F1→E1→V→N→J→D→E→F→K→A1→F1
        Line(pos["F1"], pos["E1"], color=RED, stroke_width=sw),
        Line(pos["E1"], pos["V"],  color=RED, stroke_width=sw),
        Line(pos["V"],  pos["N"],  color=RED, stroke_width=sw),
        Line(pos["N"],  pos["J"],  color=RED, stroke_width=sw),
        Line(pos["J"],  pos["D"],  color=RED, stroke_width=sw),
        Line(pos["D"],  pos["E"],  color=RED, stroke_width=sw),
        Line(pos["E"],  pos["F"],  color=RED, stroke_width=sw),
        Line(pos["F"],  pos["K"],  color=RED, stroke_width=sw),
        Line(pos["K"],  pos["A1"], color=RED, stroke_width=sw),
        Line(pos["A1"], pos["F1"], color=RED, stroke_width=sw),
        # middle 7-cycle: Z→D1→C1→T→P→I→G→Z
        Line(pos["Z"],  pos["D1"], color=RED, stroke_width=sw),
        Line(pos["D1"], pos["C1"], color=RED, stroke_width=sw),
        Line(pos["C1"], pos["T"],  color=RED, stroke_width=sw),
        Line(pos["T"],  pos["P"],  color=RED, stroke_width=sw),
        Line(pos["P"],  pos["I"],  color=RED, stroke_width=sw),
        Line(pos["I"],  pos["G"],  color=RED, stroke_width=sw),
        Line(pos["G"],  pos["Z"],  color=RED, stroke_width=sw),
        # inner 5-cycle: B1→R→M→L→W→B1
        Line(pos["B1"], pos["R"],  color=RED, stroke_width=sw),
        Line(pos["R"],  pos["M"],  color=RED, stroke_width=sw),
        Line(pos["M"],  pos["L"],  color=RED, stroke_width=sw),
        Line(pos["L"],  pos["W"],  color=RED, stroke_width=sw),
        Line(pos["W"],  pos["B1"], color=RED, stroke_width=sw),
        # core cycle: A→S→Q→A
        Line(pos["A"],  pos["S"],  color=RED, stroke_width=sw),
        Line(pos["S"],  pos["Q"],  color=RED, stroke_width=sw),
        Line(pos["Q"],  pos["A"],  color=RED, stroke_width=sw),
    )
    scene.play(Create(onion_edges))
    scene.next_slide()

    return {**ctx, "onion_edges": onion_edges}


@app.function
def onion_slide_2(scene, ctx):
    import numpy as np
    pos = ctx["pos"]
    sw = 1.5

    # Outer 10-cycle polygon filled, label Q inside and P outside
    outer_poly = Polygon(
        pos["F1"], pos["E1"], pos["V"], pos["N"], pos["J"],
        pos["D"], pos["E"], pos["F"], pos["K"], pos["A1"],
        fill_color=BLUE, fill_opacity=0.8, stroke_width=0,
    )
    label_q = Text("Q", font_size=18, color=WHITE)
    label_q.move_to(np.array([0.2, 0.0, 0.0]))
    label_p = Text("P", font_size=18, color=WHITE)
    label_p.move_to(np.array([2.8, 0.5, 0.0]))
    scene.play(FadeIn(outer_poly), FadeIn(label_q), FadeIn(label_p))
    scene.next_slide()

    # Dots B and C red, edge B-C blue, labels a, b, e
    dot_b = ctx["point_dots"][1]
    dot_c = ctx["point_dots"][2]
    edge_bc = Line(pos["B"], pos["C"], color=BLUE, stroke_width=sw)
    label_dot_a = Text("a", font_size=14, color=WHITE)
    label_dot_a.next_to(dot_b, DOWN, buff=0.12)
    label_dot_b = Text("b", font_size=14, color=WHITE)
    label_dot_b.next_to(dot_c, RIGHT, buff=0.1)
    mid_bc = (pos["B"] + pos["C"]) / 2
    label_edge_e = Text("e", font_size=14, color=WHITE)
    label_edge_e.move_to(mid_bc + np.array([0.0, -0.15, 0.0]))
    scene.play(
        dot_b.animate.set_color(RED),
        dot_c.animate.set_color(RED),
        Create(edge_bc),
        FadeIn(label_dot_a), FadeIn(label_dot_b), FadeIn(label_edge_e),
    )
    scene.next_slide()

    # Dot D red, label v
    dot_d = ctx["point_dots"][3]
    label_dot_v = Text("v", font_size=14, color=WHITE)
    label_dot_v.next_to(dot_d, LEFT, buff=0.12)
    label_dot_v.set_z_index(2)
    scene.play(dot_d.animate.set_color(RED), FadeIn(label_dot_v))
    scene.next_slide()

    # Blue triangle B-C-D
    tri_bcd = Polygon(
        pos["B"], pos["C"], pos["D"],
        fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE, stroke_width=sw,
    )
    scene.play(Create(tri_bcd))
    scene.next_slide()

    # Dot J red, label u, edge D-J blue with label f
    dot_j = ctx["point_dots"][9]
    label_dot_u = Text("u", font_size=14, color=WHITE)
    label_dot_u.next_to(dot_j, RIGHT, buff=0.12)
    label_dot_u.set_z_index(2)
    edge_dj = Line(pos["D"], pos["J"], color=BLUE, stroke_width=sw)
    mid_dj = (pos["D"] + pos["J"]) / 2
    label_edge_f = Text("f", font_size=14, color=WHITE)
    label_edge_f.move_to(mid_dj + np.array([0.2, 0.0, 0.0]))
    label_edge_f.set_z_index(2)
    scene.play(
        dot_j.animate.set_color(RED),
        FadeIn(label_dot_u),
        Create(edge_dj),
        FadeIn(label_edge_f),
    )
    scene.next_slide()

    # Yellow triangle C-D-J
    tri_cdj = Polygon(
        pos["C"], pos["D"], pos["J"],
        fill_color=YELLOW, fill_opacity=0.3, stroke_color=YELLOW, stroke_width=sw,
    )
    scene.play(Create(tri_cdj))
    scene.next_slide()

    # Color B, D, E, O green; add labels p, q, p', q'
    dot_e = ctx["point_dots"][4]
    dot_o = ctx["point_dots"][14]
    label_p_b = Text("p", font_size=14, color=WHITE)
    label_p_b.next_to(dot_b, LEFT, buff=0.12)
    label_p_b.set_z_index(2)
    label_q_d = Text("q", font_size=14, color=WHITE)
    label_q_d.next_to(dot_d, RIGHT, buff=0.12)
    label_q_d.set_z_index(2)
    label_pp_o = Text("p'", font_size=14, color=WHITE)
    label_pp_o.next_to(dot_o, LEFT, buff=0.12)
    label_pp_o.set_z_index(2)
    label_qp_e = Text("q'", font_size=14, color=WHITE)
    label_qp_e.next_to(dot_e, DOWN, buff=0.12)
    label_qp_e.set_z_index(2)
    scene.play(
        dot_b.animate.set_color(GREEN),
        dot_d.animate.set_color(GREEN),
        dot_e.animate.set_color(GREEN),
        dot_o.animate.set_color(GREEN),
        FadeIn(label_p_b), FadeIn(label_q_d), FadeIn(label_pp_o), FadeIn(label_qp_e),
    )
    scene.next_slide()

    # Red triangle B-E-O
    tri_beo_1 = Polygon(
        pos["B"], pos["D"], pos["O"],
        fill_color=RED, fill_opacity=0.3, stroke_color=RED, stroke_width=sw,
    )
    scene.play(Create(tri_beo_1))
    scene.next_slide()

    # Fade red triangle B-E-O
    scene.play(FadeOut(tri_beo_1))
    scene.next_slide()

    # Blue triangle B-D-E
    tri_bde = Polygon(
        pos["B"], pos["D"], pos["E"],
        fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE, stroke_width=sw,
    )
    scene.play(Create(tri_bde))
    scene.next_slide()

    # D→white, F→green, E label q'→q, F label q', remove D's q label
    dot_f = ctx["point_dots"][5]
    new_label_q_e = Text("q", font_size=14, color=WHITE)
    new_label_q_e.next_to(dot_e, DOWN, buff=0.12)
    new_label_q_e.set_z_index(2)
    label_qp_f = Text("q'", font_size=14, color=WHITE)
    label_qp_f.next_to(dot_f, DOWN, buff=0.12)
    label_qp_f.set_z_index(2)
    scene.play(
        dot_d.animate.set_color(WHITE),
        dot_f.animate.set_color(GREEN),
        Transform(label_qp_e, new_label_q_e),
        FadeIn(label_qp_f),
        FadeOut(label_q_d),
    )
    scene.next_slide()

    # Red triangle B-E-O (second time)
    tri_beo_2 = Polygon(
        pos["B"], pos["E"], pos["O"],
        fill_color=RED, fill_opacity=0.3, stroke_color=RED, stroke_width=sw,
    )
    scene.play(Create(tri_beo_2))
    scene.next_slide()

    # Fade it
    scene.play(FadeOut(tri_beo_2))
    scene.next_slide()

    # Blue triangle B-E-F
    tri_bef = Polygon(
        pos["B"], pos["E"], pos["F"],
        fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE, stroke_width=sw,
    )
    scene.play(Create(tri_bef))
    scene.next_slide()

    # Remove E's label, K gets q', F label q'→q
    dot_k = ctx["point_dots"][10]
    label_qp_k = Text("q'", font_size=14, color=WHITE)
    label_qp_k.next_to(dot_k, LEFT, buff=0.12)
    label_qp_k.set_z_index(2)
    new_label_q_f = Text("q", font_size=14, color=WHITE)
    new_label_q_f.next_to(dot_f, DOWN, buff=0.12)
    new_label_q_f.set_z_index(2)
    scene.play(
        FadeOut(label_qp_e),
        FadeIn(label_qp_k),
        Transform(label_qp_f, new_label_q_f),
    )
    scene.next_slide()

    # Yellow triangle B-F-K
    tri_bfk = Polygon(
        pos["B"], pos["F"], pos["K"],
        fill_color=YELLOW, fill_opacity=0.3, stroke_color=YELLOW, stroke_width=sw,
    )
    scene.play(Create(tri_bfk))
    scene.next_slide()

    # Fade it
    scene.play(FadeOut(tri_bfk))
    scene.next_slide()

    # Blue triangle B-F-O
    tri_bfo = Polygon(
        pos["B"], pos["F"], pos["O"],
        fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE, stroke_width=sw,
    )
    scene.play(Create(tri_bfo))
    scene.next_slide()

    # Fade out polygon, all triangles, all labels, all edges
    scene.play(
        FadeOut(outer_poly),
        FadeOut(label_q), FadeOut(label_p),
        FadeOut(edge_bc), FadeOut(edge_dj),
        FadeOut(label_dot_a), FadeOut(label_dot_b), FadeOut(label_edge_e),
        FadeOut(label_dot_v), FadeOut(label_dot_u), FadeOut(label_edge_f),
        FadeOut(tri_bcd), FadeOut(tri_cdj),
        FadeOut(label_p_b), FadeOut(label_pp_o),
        FadeOut(label_qp_f), FadeOut(label_qp_k),
        FadeOut(tri_bde), FadeOut(tri_bef), FadeOut(tri_bfo),
    )
    scene.next_slide()

    return {
        **ctx,
        "tri_bfo": tri_bfo,
    }


@app.function
def onion_slide_3(scene, ctx):
    pos = ctx["pos"]
    sw = 1.5

    # Reset all dots to white
    scene.play(*[dot.animate.set_color(WHITE) for dot in ctx["point_dots"]])
    scene.next_slide()

    # Batch 1
    batch1 = VGroup(
        DashedLine(pos["B"],  pos["C"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["C"],  pos["D"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["B"],  pos["D"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["B"],  pos["E"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["B"],  pos["F"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["F"],  pos["O"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["O"],  pos["K"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["O"],  pos["A1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["A1"], pos["G1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["G1"], pos["F1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["F1"], pos["I1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["I1"], pos["E1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["E1"], pos["H1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["H1"], pos["V"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["V"],  pos["U"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["U"],  pos["N"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["N"],  pos["H"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["H"],  pos["J"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["J"],  pos["C"],  color=WHITE, stroke_width=sw),
    )
    scene.play(Create(batch1))
    scene.next_slide()

    # Batch 2
    batch2 = VGroup(
        DashedLine(pos["J"],  pos["I"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["I"],  pos["D"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["I"],  pos["E"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["E"],  pos["G"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["G"],  pos["F"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["G"],  pos["K"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["K"],  pos["Z"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["Z"],  pos["A1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["A1"], pos["D1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["D1"], pos["F1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["D1"], pos["E1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["E1"], pos["C1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["C1"], pos["V"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["V"],  pos["T"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["T"],  pos["N"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["N"],  pos["P"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["P"],  pos["J"],  color=WHITE, stroke_width=sw),
    )
    scene.play(Create(batch2))
    scene.next_slide()

    # Batch 3
    batch3 = VGroup(
        DashedLine(pos["P"],  pos["M"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["M"],  pos["I"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["M"],  pos["P"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["I"],  pos["L"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["L"],  pos["G"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["L"],  pos["Z"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["Z"],  pos["W"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["W"],  pos["D1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["D1"], pos["B1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["B1"], pos["C1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["C1"], pos["R"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["R"],  pos["T"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["R"],  pos["P"],  color=WHITE, stroke_width=sw),
    )
    scene.play(Create(batch3))
    scene.next_slide()

    # Batch 4
    batch4 = VGroup(
        DashedLine(pos["R"],  pos["S"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["S"],  pos["M"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["M"],  pos["Q"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["Q"],  pos["L"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["Q"],  pos["W"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["W"],  pos["A"],  color=WHITE, stroke_width=sw),
        DashedLine(pos["A"],  pos["B1"], color=WHITE, stroke_width=sw),
        DashedLine(pos["B1"], pos["S"],  color=WHITE, stroke_width=sw),
    )
    scene.play(Create(batch4))
    scene.next_slide()

    # Fade out everything
    scene.play(
        FadeOut(batch1), FadeOut(batch2), FadeOut(batch3), FadeOut(batch4),
        FadeOut(ctx["point_dots"]),
        FadeOut(ctx["red_edges"]),
        FadeOut(ctx["onion_edges"]),
        FadeOut(ctx["title"]),
        FadeOut(ctx["insertion_text"]),
    )
    scene.next_slide()

    return {}


@app.cell
def _():
    import inspect
    import textwrap

    _slide_fns = [title_slide, hexagon_slide, vertex_slide, slide_90s, motivation_slide, primitives_slide, igl_slide, graph_slide, hershberger_slide, dp_slide, holes_slide, paper_slide, example_paper, steiner_slide, steiner_slide_2, steiner_slide_3, steiner_slide_4, steiner_complejidad, steiner_complejidad_espacio, steiner_triangulos, steiner_conclusiones, section3_slide, insertion_slide, insertion_slide_2, onion_slide, onion_slide_2, onion_slide_3]

    _header = """\
    # -*- coding: utf-8 -*-
    from manim import (
        Text, Square, Line, Dot, RegularPolygon, Polygon, Circle, DashedLine, RoundedRectangle,
        MathTex, VGroup,
        Write, FadeIn, FadeOut, Create, Transform,
        MoveAlongPath, LaggedStart,
        ImageMobject,
        BLACK, WHITE, YELLOW, BLUE, RED, GREEN, GOLD, TEAL,
        UP, DOWN, LEFT, RIGHT, ORIGIN, smooth
    )
    from manim_slides import Slide
    """

    _func_sources = "\n\n".join(
        textwrap.dedent(inspect.getsource(f)) for f in _slide_fns
    )

    _class_code = (
        "class SimpleSlides(Slide):\n"
        "    def construct(self):\n"
        "        self.camera.background_color = BLACK\n"
        "        ctx = title_slide(self, {})\n"
        "        self.next_slide()\n"
        "        ctx = hexagon_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = vertex_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = slide_90s(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = motivation_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = primitives_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = igl_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = graph_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = hershberger_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = dp_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = holes_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = paper_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = example_paper(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = steiner_slide(self, {})\n"
        "        self.next_slide()\n"
        "        ctx = steiner_slide_2(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = steiner_slide_3(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = steiner_slide_4(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = steiner_complejidad(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = steiner_complejidad_espacio(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = steiner_triangulos(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = steiner_conclusiones(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = section3_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = insertion_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = insertion_slide_2(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = onion_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = onion_slide_2(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = onion_slide_3(self, ctx)\n"
        "        self.next_slide()\n"
    )

    with open("render_slides-respaldo.py", "w", encoding="utf-8") as _f:
        _f.write(_header + "\n\n" + _func_sources + "\n\n" + _class_code)

    slides = _slide_fns
    return (slides,)


@app.cell
def _(slides):
    from moterm import Kmd

    _ = slides  # establece dependencia para que el ensamblado corra primero
    out1 = Kmd("manim-slides render render_slides-respaldo.py SimpleSlides -ql")
    out1
    return Kmd, out1


@app.cell
def _(Kmd, out1):
    out1

    out2 = Kmd("manim-slides convert SimpleSlides -c controls=true simple.html --one-file")
    out2
    return (out2,)


@app.cell
def _(Path, mo, out2):
    out2

    mo.iframe(Path("simple.html").read_text())
    return


if __name__ == "__main__":
    app.run()
