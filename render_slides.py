# -*- coding: utf-8 -*-
from manim import (
    Text, Square, Line, Dot, RegularPolygon, Polygon, Circle, DashedLine,
    MathTex, VGroup,
    Write, FadeIn, FadeOut, Create, Transform,
    MoveAlongPath, LaggedStart,
    ImageMobject,
    BLACK, WHITE, YELLOW, BLUE, RED, GREEN,
    UP, DOWN, LEFT, RIGHT, ORIGIN, smooth
)
from manim_slides import Slide


def insertion_time(self):
    title = Text("Inserción", font_size=72)
    self.play(Write(title))
    self.next_slide()

    small_title = Text("Inserción", font_size=36).to_corner(UP + LEFT)
    step = Text("1- Calcular el cierre convexo", font_size=32).move_to(ORIGIN)
    formula = MathTex(r"O(n \log n)", font_size=80, color=BLUE).to_edge(DOWN)
    self.play(Transform(title, small_title), Write(step), FadeIn(formula))
    self.next_slide()

    self.play(
        Transform(
            step,
            Text(
                "2- Triangular con un punto interior y el casco convexo",
                font_size=32,
            ).move_to(ORIGIN),
        ),
        Transform(formula, MathTex(r"O(n)", font_size=80, color=BLUE).to_edge(DOWN)),
    )
    self.next_slide()

    self.play(
        Transform(
            step,
            Text("3- Localizar el triángulo contenedor", font_size=32).move_to(ORIGIN),
        ),
        Transform(formula, MathTex(r"O(\log n)", font_size=80, color=BLUE).to_edge(DOWN)),
    )
    self.next_slide()

    self.play(
        Transform(
            step,
            Text(
                "4- Dividir el triángulo en tres.\n"
                "Esto implica crear nuevos registros para los triángulos nuevos,\n"
                "actualizar las adyacencias entre triángulos\n"
                "y añadir un nodo con tres hijos a la DAG.",
                font_size=24,
            ).move_to(ORIGIN),
        ),
        Transform(formula, MathTex(r"O(1)", font_size=80, color=BLUE).to_edge(DOWN)),
    )
    self.next_slide()

    self.play(
        Transform(
            step,
            Text("5- Actualizar el ciclo hamiltoniano", font_size=32).move_to(ORIGIN),
        ),
        Transform(formula, MathTex(r"O(1)", font_size=80, color=BLUE).to_edge(DOWN)),
    )
    self.next_slide()

    self.play(
        FadeOut(step),
        Transform(
            formula,
            MathTex(r"O(n \log n)^{*}", font_size=80, color=BLUE).move_to(ORIGIN),
        ),
    )
    self.next_slide()

    self._it_title = title
    self._it_formula = formula


def splitter_points_slide(self):
    import numpy as np

    title = self._it_title
    formula = self._it_formula
    separator = Text("- Puntos separadores", font_size=32).next_to(title, RIGHT)
    self.play(FadeOut(formula), FadeIn(separator))
    self.next_slide()

    def pt(x, y):
        return np.array([x * 0.8 - 2.8, y * 0.8 - 2.5, 0])

    A = pt(0, 0)
    B = pt(4, 6)
    C = pt(7, 0)
    S = pt(4, 2)
    D = S  # splitter point
    E = pt(5, 2)
    F = pt(5, 3)
    G = pt(4.5, 2.5)
    H = pt(5, 0.6)
    I = pt(1, 1)
    J = pt(4, 1)
    K = pt(3.6, 1.4)
    L = pt(3.0, 1.2)
    M = pt(3, 3)

    dots = VGroup(
        Dot(A), Dot(B), Dot(C), Dot(S), Dot(E), Dot(F),
        Dot(G), Dot(H), Dot(I), Dot(J), Dot(K), Dot(L), Dot(M),
    )
    edge_AB = Line(A, B)
    edge_BC = Line(B, C)
    edge_CA = Line(C, A)
    outer_edges = VGroup(edge_AB, edge_BC, edge_CA)

    self.play(FadeIn(dots), Create(outer_edges))
    self.next_slide()

    edge_DA = Line(D, A)
    edge_DB = Line(D, B)
    edge_DC = Line(D, C)
    d_edges = VGroup(edge_DA, edge_DB, edge_DC)
    self.play(Create(d_edges))
    self.next_slide()

    tri_ABD = Polygon(A, B, D, color=BLUE, fill_color=BLUE, fill_opacity=0.3)
    self.play(FadeIn(tri_ABD))
    self.next_slide()

    tri_BCD = Polygon(B, C, D, color=BLUE, fill_color=BLUE, fill_opacity=0.3)
    self.play(FadeOut(tri_ABD), FadeIn(tri_BCD))
    self.next_slide()

    tri_ACD = Polygon(A, C, D, color=BLUE, fill_color=BLUE, fill_opacity=0.3)
    self.play(FadeOut(tri_BCD), FadeIn(tri_ACD))
    self.next_slide()

    self.play(FadeOut(tri_ACD), FadeOut(d_edges))
    self.next_slide()

    edge_IA = Line(I, A)
    edge_IB = Line(I, B)
    edge_IC = Line(I, C)
    i_edges = VGroup(edge_IA, edge_IB, edge_IC)
    self.play(Create(i_edges))
    self.next_slide()

    tri_IBC = Polygon(I, B, C, color=RED, fill_color=RED, fill_opacity=0.3)
    self.play(FadeIn(tri_IBC))
    self.next_slide()

    self._sp_separator = separator
    self._sp_visible = VGroup(dots, outer_edges, i_edges, tri_IBC)


def insertion_space(self):
    title = self._it_title
    separator = self._sp_separator
    visible = self._sp_visible

    new_separator = Text("- Espacio", font_size=32).next_to(title, RIGHT)
    self.play(FadeOut(visible), Transform(separator, new_separator))
    self.next_slide()

    items = [
        "• Puntos de entrada",
        "• Triangulación actual",
        "• DAG",
        "• Lista por triángulo de asignación",
        "• Ciclo Hamiltoniano actual",
    ]
    bullet_list = VGroup(
        *[Text(item, font_size=28) for item in items]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(ORIGIN)

    formula = MathTex(r"O(n)", font_size=80, color=BLUE).to_edge(DOWN)
    self.play(FadeIn(bullet_list), FadeIn(formula))
    self.next_slide()


def onion_time(self):
    self.play(*[FadeOut(m) for m in self.mobjects])

    title = Text("Cebolla", font_size=72)
    self.play(Write(title))
    self.next_slide()

    small_title = Text("Cebolla", font_size=36).to_corner(UP + LEFT)
    separator = Text("- Tiempo", font_size=32).next_to(small_title, RIGHT)
    step = Text("1- Calcular los anillos de la cebolla", font_size=32).move_to(ORIGIN)
    formula = MathTex(r"O(n \log n)", font_size=80, color=BLUE).to_edge(DOWN)
    self.play(
        Transform(title, small_title),
        Write(separator),
        Write(step),
        FadeIn(formula)
    )
    self.next_slide()

    self.play(
        Transform(
            step,
            Text(
                "2- Encontrar el vértice v más cercano\n"
                "a la arista de entrada en cada anillo",
                font_size=32,
            ).move_to(ORIGIN),
        ),
        Transform(formula, MathTex(r"O(n)", font_size=80, color=BLUE).to_edge(DOWN)),
    )
    self.next_slide()

    self.play(
        Transform(
            step,
            Text(
                "3- Triangular cada anillo con el zigzag.\n"
                "En cada paso se avanza un puntero sobre P o Q\n"
                "y se genera un triángulo en O(1).",
                font_size=28,
            ).move_to(ORIGIN),
        ),
        Transform(formula, MathTex(r"O(n)", font_size=80, color=BLUE).to_edge(DOWN)),
    )
    self.next_slide()

    self.play(
        Transform(
            step,
            Text("4- Triangular el núcleo en abanico", font_size=32).move_to(ORIGIN),
        ),
        Transform(formula, MathTex(r"O(n)", font_size=80, color=BLUE).to_edge(DOWN)),
    )
    self.next_slide()

    self.play(
        Transform(
            step,
            Text(
                "5- Encadenar los caminos Hamiltonianos.\n"
                "O(1) por par de anillos consecutivos.",
                font_size=32,
            ).move_to(ORIGIN),
        ),
        Transform(formula, MathTex(r"O(n)", font_size=80, color=BLUE).to_edge(DOWN)),
    )
    self.next_slide()

    self.play(
        FadeOut(step),
        Transform(
            formula,
            MathTex(r"O(n \log n)", font_size=80, color=BLUE).move_to(ORIGIN),
        ),
    )
    self.play(FadeOut(formula))
    self.next_slide()

    self._ot_title = title
    self._ot_separator = separator


def onion_space(self):


    title = self._ot_title
    separator = self._ot_separator

    new_separator = Text("- Espacio", font_size=32).next_to(title, RIGHT)
    self.play(Transform(separator, new_separator))
    self.next_slide()

    items = [
        "• Puntos de entrada",
        "• Capas del onion",
        "• Triángulos de todos los anillos",
        "• Triángulos del núcleo",
        "• Adyacencias entre triángulos",
        "• Camino Hamiltoniano",
    ]
    bullet_list = VGroup(
        *[Text(item, font_size=28) for item in items]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(ORIGIN)

    formula = MathTex(r"O(n)", font_size=80, color=BLUE).to_edge(DOWN)
    self.play(FadeIn(bullet_list), FadeIn(formula))
    self.next_slide()

    self._ot_visible = bullet_list


def distribution(self):
    self.play(*[FadeOut(m) for m in self.mobjects])

    img_100 = ImageMobject("100").scale_to_fit_height(5).to_edge(LEFT)
    img_10k = ImageMobject("10k").scale_to_fit_height(5).to_edge(RIGHT)

    self.play(FadeIn(img_100), FadeIn(img_10k))
    self.next_slide()


def lemma24_c1(self):
    import numpy as np

    self.play(*[FadeOut(m) for m in self.mobjects])

    def pt(x, y):
        return np.array([x * 0.7 - 1.5, y * 0.7 - 1.5, 0])

    A = pt(0, 0)
    B = pt(0, 5)
    C = pt(5, 0)
    D = pt(1, 3)
    E = pt(2, 2)

    dot_A = Dot(A)
    dot_B = Dot(B)
    dot_C = Dot(C)
    dot_D = Dot(D)
    dot_E = Dot(E)
    dots = VGroup(dot_A, dot_B, dot_C, dot_D, dot_E)

    edge_AB = Line(A, B)
    edge_AC = Line(A, C)
    edge_BC = DashedLine(B, C)

    self.play(FadeIn(dots), Create(edge_AB), Create(edge_AC), Create(edge_BC))
    self.next_slide()

    lbl_A = Text("i", font_size=28).next_to(dot_A, DOWN + LEFT, buff=0.1)
    lbl_B = Text("i+1", font_size=28).next_to(dot_B, UP + LEFT, buff=0.1)
    lbl_C = Text("i-1", font_size=28).next_to(dot_C, DOWN + RIGHT, buff=0.1)

    self.play(FadeIn(lbl_A), FadeIn(lbl_B), FadeIn(lbl_C))
    self.next_slide()

    blue_AD = DashedLine(A, D, color=BLUE)
    blue_CE = DashedLine(C, E, color=BLUE)
    blue_DE = DashedLine(D, E, color=BLUE)
    blue_BE = DashedLine(B, E, color=BLUE)
    blue_BD = DashedLine(B, D, color=BLUE)
    blue_edges = VGroup(blue_AD, blue_CE, blue_DE, blue_BE, blue_BD)

    self.play(Create(blue_edges))
    self.next_slide()

    new_lbl_A = Text("4", font_size=28).next_to(dot_A, DOWN + LEFT, buff=0.1)
    new_lbl_B = Text("2, 7", font_size=28).next_to(dot_B, UP + LEFT, buff=0.1)
    new_lbl_C = Text("6", font_size=28).next_to(dot_C, DOWN + RIGHT, buff=0.1)
    lbl_D = Text("3", font_size=28).next_to(dot_D, UP, buff=0.1)
    lbl_E = Text("1, 5", font_size=28).next_to(dot_E, RIGHT, buff=0.1)

    self.play(
        Transform(lbl_A, new_lbl_A),
        Transform(lbl_B, new_lbl_B),
        Transform(lbl_C, new_lbl_C),
        FadeIn(lbl_D),
        FadeIn(lbl_E),
    )
    self.next_slide()


def lemma24_c2(self):
    import numpy as np

    self.play(*[FadeOut(m) for m in self.mobjects])

    def pt(x, y):
        return np.array([x * 0.7 - 1.5, y * 0.7 - 1.5, 0])

    A = pt(0, 0)
    B = pt(0, 5)
    C = pt(5, 5)
    D = pt(5, 0)
    E = pt(1, 2)
    F = pt(2, 4)

    dot_A = Dot(A)
    dot_B = Dot(B)
    dot_C = Dot(C)
    dot_D = Dot(D)
    dot_E = Dot(E)
    dot_F = Dot(F)
    dots = VGroup(dot_A, dot_B, dot_C, dot_D, dot_E, dot_F)

    edge_AB = Line(A, B)
    edge_BC = Line(B, C)
    edge_AD = Line(A, D)

    self.play(FadeIn(dots))
    self.next_slide()

    lbl_A = Text("i", font_size=28).next_to(dot_A, DOWN + LEFT, buff=0.1)
    lbl_B = Text("j+1", font_size=28).next_to(dot_B, UP + LEFT, buff=0.1)
    lbl_C = Text("j", font_size=28).next_to(dot_C, UP + RIGHT, buff=0.1)
    lbl_D = Text("i+1", font_size=28).next_to(dot_D, DOWN + RIGHT, buff=0.1)

    self.play(FadeIn(lbl_A), FadeIn(lbl_B), FadeIn(lbl_C), FadeIn(lbl_D), FadeIn(edge_AB), FadeIn(edge_AD), FadeIn(edge_BC))
    self.next_slide()

    edge_CD = DashedLine(C, D, color=WHITE)

    self.play(Create(edge_CD))
    self.next_slide()

    blue_AE = DashedLine(A, E, color=BLUE)
    blue_AC = DashedLine(A, C, color=BLUE)
    blue_BE = DashedLine(B, E, color=BLUE)
    blue_BF = DashedLine(B, F, color=BLUE)
    blue_EF = DashedLine(E, F, color=BLUE)
    blue_EC = DashedLine(E, C, color=BLUE)
    blue_FC = DashedLine(F, C, color=BLUE)
    blue_edges = VGroup(blue_AE, blue_AC, blue_BE, blue_BF, blue_EF, blue_EC, blue_FC)

    self.play(Create(blue_edges))
    self.next_slide()

    new_lbl_A = Text("6", font_size=28).next_to(dot_A, DOWN + LEFT, buff=0.1)
    new_lbl_B = Text("4", font_size=28).next_to(dot_B, UP + LEFT, buff=0.1)
    new_lbl_C = Text("2, 7", font_size=28).next_to(dot_C, UP + RIGHT, buff=0.1)
    lbl_E = Text("1, 5", font_size=28).next_to(dot_E, LEFT, buff=0.1)
    lbl_F = Text("3", font_size=28).next_to(dot_F, LEFT, buff=0.1)

    self.play(
        Transform(lbl_A, new_lbl_A),
        Transform(lbl_B, new_lbl_B),
        Transform(lbl_C, new_lbl_C),
        FadeIn(lbl_E),
        FadeIn(lbl_F),
    )
    self.next_slide()

    self._c2_dots = (dot_A, dot_B, dot_C, dot_D, dot_E, dot_F)
    self._c2_blue_edges = blue_edges
    self._c2_edge_AB = edge_AB
    self._c2_lbl_A = lbl_A
    self._c2_lbl_B = lbl_B
    self._c2_lbl_C = lbl_C
    self._c2_lbl_D = lbl_D
    self._c2_lbl_E = lbl_E
    self._c2_lbl_F = lbl_F


def lemma24_c3(self):
    import numpy as np

    dot_A, dot_B, dot_C, dot_D, dot_E, dot_F = self._c2_dots
    blue_edges = self._c2_blue_edges
    edge_AB = self._c2_edge_AB
    lbl_A = self._c2_lbl_A
    lbl_B = self._c2_lbl_B
    lbl_C = self._c2_lbl_C
    lbl_D = self._c2_lbl_D
    lbl_E = self._c2_lbl_E
    lbl_F = self._c2_lbl_F

    def pt(x, y):
        return np.array([x * 0.7 - 1.5, y * 0.7 - 1.5, 0])

    # Step 1: fade blue edges, dash A-B, reset labels, remove E and F labels
    rst_A = Text("i", font_size=28).next_to(dot_A, DOWN + LEFT, buff=0.1)
    rst_B = Text("j+1", font_size=28).next_to(dot_B, UP + LEFT, buff=0.1)
    rst_C = Text("j", font_size=28).next_to(dot_C, UP + RIGHT, buff=0.1)
    dashed_AB = DashedLine(dot_A.get_center(), dot_B.get_center())

    self.play(
        FadeOut(blue_edges),
        Transform(edge_AB, dashed_AB),
        Transform(lbl_A, rst_A),
        Transform(lbl_B, rst_B),
        Transform(lbl_C, rst_C),
        FadeOut(lbl_E),
        FadeOut(lbl_F),
    )
    self.next_slide()

    # Step 2: move F to (4, 4)
    F_new = pt(4, 4)
    self.play(dot_F.animate.move_to(F_new))
    self.next_slide()

    # Step 3: first blue dashed edge B-D
    blue_BD = DashedLine(dot_B.get_center(), dot_D.get_center(), color=BLUE)
    self.play(Create(blue_BD))
    self.next_slide()

    # Step 4: remaining blue dashed edges
    blue_AE = DashedLine(dot_A.get_center(), dot_E.get_center(), color=BLUE)
    blue_EB = DashedLine(dot_E.get_center(), dot_B.get_center(), color=BLUE)
    blue_ED = DashedLine(dot_E.get_center(), dot_D.get_center(), color=BLUE)
    blue_FB = DashedLine(F_new, dot_B.get_center(), color=BLUE)
    blue_FD = DashedLine(F_new, dot_D.get_center(), color=BLUE)
    blue_FC = DashedLine(F_new, dot_C.get_center(), color=BLUE)
    more_blue = VGroup(blue_AE, blue_EB, blue_ED, blue_FB, blue_FD, blue_FC)

    self.play(Create(more_blue))
    self.next_slide()

    # Step 5: final labels
    fin_A = Text("7", font_size=28).next_to(dot_A, DOWN + LEFT, buff=0.1)
    fin_B = Text("4, 8", font_size=28).next_to(dot_B, UP + LEFT, buff=0.1)
    fin_C = Text("2", font_size=28).next_to(dot_C, UP + RIGHT, buff=0.1)
    fin_D = Text("1, 5", font_size=28).next_to(dot_D, DOWN + RIGHT, buff=0.1)
    fin_E = Text("6", font_size=28).next_to(dot_E, LEFT, buff=0.1)
    fin_F = Text("3", font_size=28).next_to(dot_F, RIGHT, buff=0.1)

    self.play(
        Transform(lbl_A, fin_A),
        Transform(lbl_B, fin_B),
        Transform(lbl_C, fin_C),
        Transform(lbl_D, fin_D),
        FadeIn(fin_E),
        FadeIn(fin_F),
    )
    self.next_slide()


def lemma24_c4(self):
    import numpy as np

    self.play(*[FadeOut(m) for m in self.mobjects])

    def pt(x, y):
        return np.array([x * 0.9 - 1.8, y * 0.9 - 1.8, 0])

    A = pt(0, 1)
    B = pt(1, 0)
    C = pt(3, 0)
    D = pt(4, 1)
    E = pt(2, 4)
    F = pt(2, 3)
    G = pt(2, 2)

    dot_A = Dot(A)
    dot_B = Dot(B)
    dot_C = Dot(C)
    dot_D = Dot(D)
    dot_E = Dot(E)
    dot_F = Dot(F)
    dot_G = Dot(G)
    dots = VGroup(dot_A, dot_B, dot_C, dot_D, dot_E, dot_F, dot_G)

    self.play(FadeIn(dots))
    self.next_slide()

    # Solid chain A-B-C-D + dashed A-E and D-E
    edge_AB = Line(A, B)
    edge_BC = Line(B, C)
    edge_CD = Line(C, D)
    edge_AE = DashedLine(A, E)
    edge_DE = DashedLine(D, E)

    self.play(Create(edge_AB), Create(edge_BC), Create(edge_CD),
              Create(edge_AE), Create(edge_DE))
    self.next_slide()

    # Labels: A=i-1, B=i, C=i+1, D=i+2, E=j+1
    lbl_A = Text("i-1", font_size=28).next_to(dot_A, LEFT, buff=0.1)
    lbl_B = Text("i", font_size=28).next_to(dot_B, DOWN, buff=0.1)
    lbl_C = Text("i+1", font_size=28).next_to(dot_C, DOWN, buff=0.1)
    lbl_D = Text("i+2", font_size=28).next_to(dot_D, RIGHT, buff=0.1)
    lbl_E = Text("j+1", font_size=28).next_to(dot_E, UP, buff=0.1)

    self.play(FadeIn(lbl_A), FadeIn(lbl_B), FadeIn(lbl_C), FadeIn(lbl_D), FadeIn(lbl_E))
    self.next_slide()

    # Blue dashed edges: A-F, B-F, B-G, G-F, C-G, C-F, D-F, F-E
    blue_AF = DashedLine(A, F, color=BLUE)
    blue_BF = DashedLine(B, F, color=BLUE)
    blue_BG = DashedLine(B, G, color=BLUE)
    blue_GF = DashedLine(G, F, color=BLUE)
    blue_CG = DashedLine(C, G, color=BLUE)
    blue_CF = DashedLine(C, F, color=BLUE)
    blue_DF = DashedLine(D, F, color=BLUE)
    blue_FE = DashedLine(F, E, color=BLUE)
    blue_edges = VGroup(blue_AF, blue_BF, blue_BG, blue_GF, blue_CG, blue_CF, blue_DF, blue_FE)

    self.play(Create(blue_edges))
    self.next_slide()

    # Final labels: A=8, B=6, C=4, D=2, E="9, 1", F="7, 3", G=5
    fin_A = Text("8", font_size=28).next_to(dot_A, LEFT, buff=0.1)
    fin_B = Text("6", font_size=28).next_to(dot_B, DOWN, buff=0.1)
    fin_C = Text("4", font_size=28).next_to(dot_C, DOWN, buff=0.1)
    fin_D = Text("2", font_size=28).next_to(dot_D, RIGHT, buff=0.1)
    fin_E = Text("9, 1", font_size=28).next_to(dot_E, UP, buff=0.1)
    lbl_F = Text("7, 3", font_size=28).next_to(dot_F, RIGHT, buff=0.1)
    lbl_G = Text("5", font_size=28).next_to(dot_G, RIGHT, buff=0.1)

    self.play(
        Transform(lbl_A, fin_A),
        Transform(lbl_B, fin_B),
        Transform(lbl_C, fin_C),
        Transform(lbl_D, fin_D),
        Transform(lbl_E, fin_E),
        FadeIn(lbl_F),
        FadeIn(lbl_G),
    )
    self.next_slide()


class SimpleSlides(Slide):
    def construct(self):
        self.camera.background_color = BLACK
        insertion_time(self)
        splitter_points_slide(self)
        insertion_space(self)
        onion_time(self)
        onion_space(self)
        distribution(self)
        lemma24_c1(self)
        lemma24_c2(self)
        lemma24_c3(self)
        lemma24_c4(self)
