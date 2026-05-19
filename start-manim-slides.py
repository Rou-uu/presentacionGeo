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

__generated_with = "0.23.6"
app = marimo.App(sql_output="polars")

with app.setup:
    from manim import (
        Text, Square, Line, Dot, RegularPolygon, Polygon, Circle, DashedLine,
        MathTex, VGroup,
        Write, FadeIn, FadeOut, Create, Transform,
        MoveAlongPath, LaggedStart,
        ImageMobject,
        BLACK, WHITE, YELLOW, BLUE, RED, GREEN,
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
    scene.play(FadeOut(ctx["hexagon"]), *[FadeOut(d) for d in ctx["diagonals"]])

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

    return {"text": text_top, "imgs": g2_imgs, "caps": g2_caps}


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

    return {
        "polygon": polygon, "v_dots": v_dots, "v_labels": v_labels,
        "heading": heading, "success": desc,
        "k_segs": VGroup(k2_segs, k3_segs, k4_segs),
        "d_labels": VGroup(d_k2, d03, d04, d15),
        "tris": tris, "legend": legend,
    }


@app.cell
def _():
    import inspect
    import textwrap

    _slide_fns = [title_slide, graph_slide, hershberger_slide, dp_slide]

    _header = """\
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
        "        ctx = graph_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = hershberger_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = dp_slide(self, ctx)\n"
        "        self.next_slide()\n"
    )

    with open("render_slides.py", "w", encoding="utf-8") as _f:
        _f.write(_header + "\n\n" + _func_sources + "\n\n" + _class_code)

    slides = _slide_fns
    return (slides,)


@app.cell
def _(slides):
    from moterm import Kmd

    _ = slides  # establece dependencia para que el ensamblado corra primero
    out1 = Kmd("manim-slides render render_slides.py SimpleSlides")
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
