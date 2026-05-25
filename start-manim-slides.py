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


@app.cell
def _(RoundedRectangle):
    def steiner_slide(scene, ctx):
        import numpy as np

        scene.play(
            FadeOut(ctx["title"]),
            FadeOut(ctx["subtitle"]),
            FadeOut(ctx["corner_left"]),
            FadeOut(ctx["corner_right"])
        )

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

    return


@app.cell
def _(GOLD, TEAL):
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

    return


@app.cell
def _(GOLD, TEAL):
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

    return


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

    scene.play(FadeIn(t1))
    scene.next_slide()
    scene.play(FadeIn(t2))
    scene.next_slide()
    scene.play(FadeIn(t3))
    scene.next_slide()

    return {"heading": heading, "conclusiones_text": conclusiones_text, "t1": t1, "t2": t2, "t3": t3}


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
# case1_theorem41.py — Caso 1 del Teorema 4.1


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


@app.function
# -*- coding: utf-8 -*-
# case2_theorem41.py — Caso 2 del Teorema 4.1: C = 4


def paper_slide2(scene, ctx):
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

    PA  = pt(25, 40)
    PB  = pt(35, 40)
    PC  = pt(55, 10)
    PD  = pt(50,  5)
    PE  = pt(10,  5)
    PF  = pt( 5, 10)
    Pc  = pt(30, 25)
    Pa  = pt(25, 15)
    Pb  = pt(35, 15)

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
        'Teorema 4.1 — Caso 2: C = 4',
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
    # SLIDE 1 — Asignación: a=1, b=2, c=3, C=4
    # ════════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(sub0), run_time=0.3)
    sub1 = Text('Asignación: a=1, b=2, c=3, C=4',
                font_size=SUB_SZ, color=GRAY_B)
    sub1.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub1), run_time=0.3)

    seg_l = mk_seg(PC, Pb)
    seg_m = mk_seg(PC, Pc)
    scene.play(Create(seg_l), Create(seg_m), run_time=0.6)

    num1 = mk_num('1', Pa, direction=DOWN+LEFT, buff=0.20, color=YELLOW)
    num2 = mk_num('2', Pb, direction=DOWN+RIGHT,buff=0.20, color=YELLOW)
    num3 = mk_num('3', Pc, direction=UP,        buff=0.20, color=YELLOW)
    num4 = mk_num('4', PC, direction=RIGHT,     buff=0.22, color=ORANGE)

    scene.play(
        FadeIn(num1), FadeOut(lbl_a),
        FadeIn(num2), FadeOut(lbl_b),
        FadeIn(num3), FadeOut(lbl_c),
        FadeIn(num4), FadeOut(lbl_C),
        run_time=0.6,
    )

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 2 — ¿Por qué F no puede ser el punto 0?
    # Polígono: F–E–D–C(4)–b(2)
    # ════════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(sub1), run_time=0.3)
    sub2 = Text('¿Por qué F no puede ser el punto 0?',
                font_size=SUB_SZ, color=GRAY_B)
    sub2.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub2), run_time=0.3)

    dash_fa = mk_dash(PF, Pa)
    dash_fb = mk_dash(PF, Pb)
    poly2 = mk_poly([PF, PE, PD, PC, Pb])
    seg2_blue = VGroup(
        mk_seg(PF, PE, color=BLUE_D, sw=2.5),
        mk_seg(PE, PD, color=BLUE_D, sw=2.5),
        mk_seg(PD, PC, color=BLUE_D, sw=2.5),
        mk_seg(PC, Pb, color=BLUE_D, sw=2.5),
        mk_seg(Pb, PF, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(dash_fa), Create(dash_fb), run_time=0.7)
    scene.play(FadeIn(poly2), run_time=0.5)
    scene.play(Create(seg2_blue), run_time=0.6)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 3 — ¿Por qué E no puede ser el punto 0?
    # Polígono: E–D–C(4)–b(2)
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub2),
        FadeOut(dash_fa), FadeOut(dash_fb),
        FadeOut(poly2),   FadeOut(seg2_blue),
        run_time=0.4,
    )
    sub3 = Text('¿Por qué E no puede ser el punto 0?',
                font_size=SUB_SZ, color=GRAY_B)
    sub3.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub3), run_time=0.3)

    dash_ea = mk_dash(PE, Pa)
    dash_eb = mk_dash(PE, Pb)
    poly3 = mk_poly([PE, PD, PC, Pb])
    seg3_blue = VGroup(
        mk_seg(PE, PD, color=BLUE_D, sw=2.5),
        mk_seg(PD, PC, color=BLUE_D, sw=2.5),
        mk_seg(PC, Pb, color=BLUE_D, sw=2.5),
        mk_seg(Pb, PE, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(dash_ea), Create(dash_eb), run_time=0.7)
    scene.play(FadeIn(poly3),  run_time=0.5)
    scene.play(Create(seg3_blue), run_time=0.6)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 4 — Candidatos para el punto 5: A y B
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub3),
        FadeOut(dash_ea), FadeOut(dash_eb),
        FadeOut(poly3),   FadeOut(seg3_blue),
        run_time=0.4,
    )
    sub4 = Text('Candidatos para el punto 5',
                font_size=SUB_SZ, color=GRAY_B)
    sub4.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub4), run_time=0.3)

    dash_c_a = mk_dash(PC, Pa)
    scene.play(Create(dash_c_a), run_time=0.5)

    lbl_fc1 = mk_lbl('FiveCand₁', PB, direction=UP+RIGHT, buff=0.10, color=ORANGE)
    lbl_fc2 = mk_lbl('FiveCand₂', PA, direction=UP+LEFT,  buff=0.10, color=ORANGE)
    scene.play(
        FadeIn(lbl_fc1), FadeOut(lbl_B),
        FadeIn(lbl_fc2), FadeOut(lbl_A),
        run_time=0.5,
    )

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 5 — B=5 no puede ser el punto 5
    # Polígono: A–B–C
    # ════════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(sub4), run_time=0.3)
    sub5 = Text('¿Por qué B no puede ser el punto 5?',
                font_size=SUB_SZ, color=GRAY_B)
    sub5.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub5), run_time=0.3)

    num5_b   = mk_num('5', PB, direction=UP+RIGHT, buff=0.20, color=GREEN)
    lbl_sc_a = mk_lbl('SixCand', PA, direction=UP+LEFT, buff=0.10, color=ORANGE)
    scene.play(
        FadeIn(num5_b),   FadeOut(lbl_fc1),
        FadeIn(lbl_sc_a), FadeOut(lbl_fc2),
        run_time=0.5,
    )

    seg_cb  = mk_seg(PC, PB, color=WHITE, sw=2.5)
    seg_cb2 = mk_seg(Pc, PB, color=WHITE, sw=2.5)
    poly5 = mk_poly([PA, PB, PC])
    seg5_blue = VGroup(
        mk_seg(PA, PB, color=BLUE_D, sw=2.5),
        mk_seg(PB, PC, color=BLUE_D, sw=2.5),
        mk_seg(PC, PA, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(seg_cb), Create(seg_cb2), run_time=0.6)
    scene.play(FadeIn(poly5), run_time=0.5)
    scene.play(Create(seg5_blue), run_time=0.6)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 6 — A=5 no puede ser el punto 5
    # Polígono: C–A–B
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub5),
        FadeOut(seg_cb),  FadeOut(seg_cb2),
        FadeOut(poly5),   FadeOut(seg5_blue),
        run_time=0.4,
    )
    sub6 = Text('¿Por qué A no puede ser el punto 5?',
                font_size=SUB_SZ, color=GRAY_B)
    sub6.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub6), run_time=0.3)

    num5_a   = mk_num('5', PA, direction=UP+LEFT,  buff=0.20, color=GREEN)
    lbl_sc_b = mk_lbl('SixCand', PB, direction=UP+RIGHT, buff=0.10, color=ORANGE)
    scene.play(
        FadeIn(num5_a),   FadeOut(lbl_sc_a),
        FadeIn(lbl_sc_b), FadeOut(num5_b),
        run_time=0.5,
    )

    seg_ca  = mk_seg(PC, PA, color=WHITE, sw=2.5)
    seg_ca2 = mk_seg(Pc, PA, color=WHITE, sw=2.5)
    poly6 = mk_poly([PC, PA, PB])
    seg6_blue = VGroup(
        mk_seg(PC, PA, color=BLUE_D, sw=2.5),
        mk_seg(PA, PB, color=BLUE_D, sw=2.5),
        mk_seg(PB, PC, color=BLUE_D, sw=2.5),
    )

    scene.play(Create(seg_ca), Create(seg_ca2), run_time=0.6)
    scene.play(FadeIn(poly6),  run_time=0.5)
    scene.play(Create(seg6_blue), run_time=0.6)

    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 7 — Conclusión
    # ════════════════════════════════════════════════════════════════════════
    scene.play(
        FadeOut(sub6),
        FadeOut(seg_ca),  FadeOut(seg_ca2),
        FadeOut(poly6),   FadeOut(seg6_blue),
        FadeOut(num5_a),  FadeOut(lbl_sc_b),
        run_time=0.4,
    )
    sub7 = Text('Conclusión Caso 2: ningún candidato a 5 es válido',
                font_size=SUB_SZ, color=GRAY_B)
    sub7.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub7), run_time=0.3)

    scene.next_slide()

    return {'heading': heading}


@app.function
# -*- coding: utf-8 -*-
# case3_theorem41.py — Caso 3 del Teorema 4.1: B = 4


def paper_slide3(scene, ctx):
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
        run_time=0.6)


    scene.next_slide()

    # ════════════════════════════════════════════════════════════════════════
    # SLIDE 2 — ¿Por qué F no puede ser el punto 0?
    # Segs: Four–F(n), F–Three(p)
    # Polígono: A–F–Four(B)
    # ════════════════════════════════════════════════════════════════════════
    scene.play(FadeOut(sub1), run_time=0.3)
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
    scene.play(FadeIn(poly2),  run_time=0.5)
    scene.play(Create(seg2_blue), run_time=0.6)

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
        run_time=0.4)
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
    scene.play(FadeIn(poly3),  run_time=0.5)
    scene.play(Create(seg3_blue), run_time=0.6)

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
        run_time=0.4)
    sub4 = Text('¿Por qué A no puede ser el punto 5?',
                font_size=SUB_SZ, color=GRAY_B)
    sub4.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub4), run_time=0.3)

    # A toma número 5; E recupera su label; F ya tiene su label (volvió en slide 3)
    num5_a = mk_num('5', PA, direction=UP+LEFT, buff=0.20, color=GREEN)
    scene.play(
        FadeIn(num5_a), FadeOut(lbl_A),
        FadeIn(lbl_E),
        run_time=0.5)

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
        run_time=0.4)
    sub5 = Text('Continuación: A=6, F=7',
                font_size=SUB_SZ, color=GRAY_B)
    sub5.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.10)
    scene.play(FadeIn(sub5), run_time=0.3)

    num6 = mk_num('6', PA, direction=UP+LEFT, buff=0.20, color=GREEN)
    num7 = mk_num('7', PF, direction=LEFT,    buff=0.20, color=GREEN)

    # num1 ya está sobre Pa (dirección DOWN+LEFT); num5 va en dirección DOWN
    num5_one = mk_num('5', Pa, direction=DOWN+RIGHT, buff=0.20, color=GREEN)

    scene.play(
        FadeIn(num6),     FadeOut(num5_a),
        FadeIn(num7),     FadeOut(lbl_F),
        FadeIn(num5_one),
        run_time=0.5)

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


    scene.next_slide()

    return {'heading': heading}


@app.cell
def _():
    import inspect
    import textwrap

    _slide_fns = [title_slide, holes_slide, paper_slide]

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
        "        ctx = holes_slide(self, ctx)\n"
        "        self.next_slide()\n"
        "        ctx = paper_slide(self, ctx)\n"
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
