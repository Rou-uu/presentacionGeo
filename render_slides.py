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


def steiner_conclusiones(scene, ctx):
    # heading = ctx["heading"]
    heading = Text("Puntos Steiner", font_size=28, color=WHITE)

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


def onion_slide_2(scene, ctx):
    import numpy as np
    pos = ctx["pos"]
    sw = 1.5

    # Outer 10-cycle polygon filled, label Q inside and P outside
    outer_poly = Polygon(
        pos["F1"], pos["E1"], pos["V"], pos["N"], pos["J"],
        pos["D"], pos["E"], pos["F"], pos["K"], pos["A1"],
        fill_color=BLUE, fill_opacity=0.2, stroke_width=0,
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
    edge_dj = Line(pos["D"], pos["J"], color=BLUE, stroke_width=sw)
    mid_dj = (pos["D"] + pos["J"]) / 2
    label_edge_f = Text("f", font_size=14, color=WHITE)
    label_edge_f.move_to(mid_dj + np.array([0.2, 0.0, 0.0]))
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

    return {
        **ctx,
        "outer_poly": outer_poly, "label_q": label_q, "label_p": label_p,
        "edge_bc": edge_bc, "label_dot_a": label_dot_a, "label_dot_b_text": label_dot_b,
        "label_edge_e": label_edge_e, "label_dot_v": label_dot_v,
        "tri_bcd": tri_bcd, "label_dot_u": label_dot_u,
        "edge_dj": edge_dj, "label_edge_f": label_edge_f, "tri_cdj": tri_cdj,
    }


class SimpleSlides(Slide):
    def construct(self):
        self.camera.background_color = BLACK
        ctx = steiner_conclusiones(self, {})
        self.next_slide()
        ctx = section3_slide(self, ctx)
        self.next_slide()
        ctx = insertion_slide(self, ctx)
        self.next_slide()
        ctx = insertion_slide_2(self, ctx)
        self.next_slide()
        ctx = onion_slide(self, ctx)
        self.next_slide()
        ctx = onion_slide_2(self, ctx)
        self.next_slide()
