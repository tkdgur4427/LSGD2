from re import A
from tkinter import BOTTOM, TOP
from manim import *
import math

# add SGDPyUtil's path dynamically
import sys

sgdpyutil_dir = os.path.dirname(__file__)
sgdpyutil_dir = os.path.join(sgdpyutil_dir, os.path.pardir)
sgdpyutil_dir = os.path.normpath(os.path.abspath(sgdpyutil_dir))
sys.path.append(sgdpyutil_dir)

from SGDPyUtil import debugpy_utils

# set config
config.save_as_gif = True


class SquareRoot(Scene):
    def construct(self):
        # debugging
        # debugpy_utils.breakpoint(True)

        title = Title("Square Root Study Case: $\sqrt{5}$")
        desc = Tex("$\sqrt{5}$ is located somewhere here!")

        x_axis = NumberLine(
            x_range=[2.21, 2.25 + 0.01, 0.01],
            length=10,
            include_tip=True,
            include_numbers=True,
        )

        # get the position of sqrt(5)
        position = x_axis.n2p(2.235)

        # calculate rectangle width
        position_start = x_axis.n2p(2.231)
        position_end = x_axis.n2p(2.239)
        rect_width = position_end[0] - position_start[0]

        # generate dot to indicate the position
        mark_rect = Rectangle(width=rect_width, height=0.5, stroke_color=BLUE).move_to(
            position
        )
        self.add(title, x_axis, mark_rect)

        # start the animation by dot
        # note that animated_dot_0 is the moving object! animated_dot_1 is just target!
        animated_dot_0 = Dot(position, color=RED)
        animated_dot_1 = animated_dot_0.copy().shift([-rect_width / 2, 0, 0])
        self.play(Transform(animated_dot_0, animated_dot_1))

        animated_dot_1 = animated_dot_1.shift([rect_width, 0, 0])
        self.play(Transform(animated_dot_0, animated_dot_1))

        animated_dot_1 = animated_dot_1.shift([-rect_width / 2, 0, 0])
        self.play(Transform(animated_dot_0, animated_dot_1))

        # add description to mark_rect
        desc.next_to(mark_rect, UP)
        self.play(FadeIn(desc))


class Variance(Scene):
    def construct(self):
        # class A
        class_A_title = Text("'A' Class (Average=50)").to_edge(LEFT)

        class_A_scores = [50, 60, 40, 30, 70, 50]
        class_A_score_minus_average = [0, 10, -10, -20, 20, 0]
        class_A_score_minus_average_square = [0, 100, 100, 400, 400, 0]

        class_A_table = (
            IntegerTable(
                [
                    class_A_scores,
                    class_A_score_minus_average,
                    class_A_score_minus_average_square,
                ],
                row_labels=[
                    MathTex("Score"),
                    MathTex("Score-Avg"),
                    MathTex("(Score-Avg)^{2}"),
                ],
                include_outer_lines=True,
                h_buff=1,
            )
            .scale(0.7)
            .next_to(class_A_title, DOWN, aligned_edge=LEFT)
        )

        group_A = Group(class_A_title, class_A_table).move_to(UP * 2)
        self.add(group_A)

        # class B
        class_B_title = Text("'B' Class (Average=50)").to_edge(LEFT)

        class_B_scores = [40, 30, 40, 40, 100]
        class_B_score_minus_average = [-10, -20, -10, -10, 50]
        class_B_score_minus_average_square = [100, 400, 100, 100, 2500]
        class_B_table = (
            IntegerTable(
                [
                    class_B_scores,
                    class_B_score_minus_average,
                    class_B_score_minus_average_square,
                ],
                row_labels=[
                    MathTex("Score"),
                    MathTex("Score-Avg"),
                    MathTex("(Score-Avg)^{2}"),
                ],
                include_outer_lines=True,
                h_buff=1,
            )
            .scale(0.7)
            .next_to(class_B_title, DOWN, aligned_edge=LEFT)
        )

        group_B = Group(class_B_title, class_B_table).move_to(DOWN * 2)
        self.add(group_B)

        return


class Function(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10],
            y_range=[0, 100, 10],
        )
        labels = ax.get_axis_labels(x_label="x", y_label="y")

        def function(x):
            return 2 * (x - 4) ** 2 + 5

        # plot the function from axes (coordinates)
        graph = ax.plot(function, color=MAROON)

        # calculate the dot position and add dot
        dot_position = [ax.coords_to_point(7, function(7))]
        dot = Dot(point=dot_position)

        # add dot information line
        dot_lines = ax.get_lines_to_point(ax.c2p(7, function(7)))

        # dot label
        dot_label = ax.get_graph_label(graph, "(a,f(a))", x_val=7, direction=RIGHT * 2)

        # add x label
        x_label = ax.get_T_label(x_val=7, graph=graph, label="a")

        # add graph label
        graph_label = ax.get_graph_label(graph, "y=f(x)", x_val=9, direction=LEFT * 2)

        self.add(ax, labels, graph, dot, dot_lines, dot_label, x_label, graph_label)

        return


class Function2ndOrder(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 5],
            y_range=[0, 40, 5],
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def function(x):
            return 2 * (x - 2) ** 2 + 10

        # plot the function from axes
        graph = axes.plot(function, color=PURPLE)

        # calculate the quadratic vertex
        quadratic_vertex = Dot(point=[axes.coords_to_point(2, function(2))])

        # add dot information line
        dot_lines = axes.get_lines_to_point(axes.c2p(2, function(2)))

        # vertex label
        vertex_label = axes.get_graph_label(graph, "(p,q)", x_val=2, direction=UP * 2)

        # add x label
        x_label = axes.get_T_label(x_val=2, graph=graph, label="p")

        # graph label
        graph_label = axes.get_graph_label(
            graph, "y=a(x-p)^2+q", x_val=4.9, direction=LEFT * 2
        )

        self.add(
            axes,
            labels,
            graph,
            quadratic_vertex,
            dot_lines,
            vertex_label,
            x_label,
            graph_label,
        )

        return


class PerfectSquareExpression(Scene):
    def construct(self):
        # render math equation
        text = MathTex("x^2+", "2k", "x", "=", "(x+", "k", ")^2", "-", "k^2")
        self.play(Write(text))

        # render frame boxes for k
        framebox_0 = SurroundingRectangle(text[1], buff=0.1)
        framebox_1 = SurroundingRectangle(text[5], buff=0.1)
        framebox_2 = SurroundingRectangle(text[8], buff=0.1)
        self.play(Create(framebox_0), Create(framebox_1), Create(framebox_2))

        # half!
        start_position = framebox_0.get_bottom()
        end_position = framebox_1.get_bottom()
        curved_arrow = CurvedArrow(start_position, end_position, radius=2)
        curved_arrow_desc = Text("Half!").next_to(curved_arrow, direction=DOWN)
        self.play(Create(curved_arrow), Create(curved_arrow_desc))

        # square!
        start_position = framebox_1.get_top()
        end_position = framebox_2.get_top()
        curved_arrow = CurvedArrow(start_position, end_position, radius=-2)
        curved_arrow_desc = Text("Square!").next_to(curved_arrow, direction=UP)
        self.play(Create(curved_arrow), Create(curved_arrow_desc))


class PerfectSquareExample(Scene):
    def construct(self):
        # construct math text
        text = MathTex(
            r"ax^2+bx=a(",
            r"x^2+\frac{b}{a}x",
            r")&=a\{",
            r"(x+\frac{b}{2a})^{2}-(\frac{b}{2a})^{2}",
            r"\}\\&=a\{(x+\frac{b}{2a})^2-\frac{b^2}{4a^2}\}",
        )
        self.play(Write(text))

        # frame boxes
        frame_box_0 = SurroundingRectangle(text[1], buff=0.1)
        frame_box_1 = SurroundingRectangle(text[3], buff=0.1)
        self.play(Create(frame_box_0), Create(frame_box_1))

        # arc arrow
        arrow_start = frame_box_0.get_top()
        arrow_end = frame_box_1.get_top()
        arc_arrow = CurvedArrow(arrow_start, arrow_end, radius=-6.0)
        arc_arrow_desc = (
            Text("Perfect Square!").scale(0.7).next_to(arc_arrow, direction=UP)
        )
        self.play(Create(arc_arrow), Create(arc_arrow_desc))


class PerfectSquareExample2(Scene):
    def construct(self):
        math_text_0 = MathTex(
            r"y=ax^2+bx+c=",
            r"a",
            r"\{",
            r"(x+\frac{b}{2a})^2",
            r"-",
            r"\frac{b^2}{4a^2}",
            r"\}+c",
        )
        self.add(math_text_0)

        framebox_0 = SurroundingRectangle(math_text_0[1])
        framebox_1 = SurroundingRectangle(math_text_0[3])
        framebox_2 = SurroundingRectangle(math_text_0[5])
        self.play(Create(framebox_0), Create(framebox_1), Create(framebox_2))
        self.wait()

        dest_location_0 = framebox_0.get_top()
        dest_location_1 = framebox_1.get_top()
        dest_location_2 = framebox_2.get_top()
        arrow_0 = CurvedArrow(dest_location_0, dest_location_1, radius=-2)
        arrow_1 = CurvedArrow(dest_location_0, dest_location_2, radius=-8)
        group_arrows = Group(arrow_0, arrow_1)
        group_desc = Text("Distribution").scale(0.7).next_to(group_arrows, direction=UP)

        self.play(FadeIn(group_arrows), FadeIn(group_desc))
        self.wait()

        self.play(FadeOut(group_arrows), FadeOut(group_desc))
        self.wait()

        self.play(Uncreate(framebox_0), Uncreate(framebox_1), Uncreate(framebox_2))
        self.wait()

        # move math_text_0 above
        math_text_0.generate_target()
        math_text_0.target.scale(0.5).to_edge(edge=UP)
        self.play(MoveToTarget(math_text_0))
        self.wait()

        math_text_1 = MathTex(
            r"y&=a(x+\frac{b}{2a})^2-\frac{b^2}{4a}+c",
            r"\\ \\",
            r"&=a(x+\frac{b}{2a})^2-\frac{b^2-4ac}{4a}",
        )
        self.play(FadeIn(math_text_1))

        math_text_1.generate_target()
        math_text_1.target.to_edge(edge=LEFT)
        self.play(MoveToTarget(math_text_1))
        self.wait()

        framebox_0 = SurroundingRectangle(math_text_1[0])
        framebox_1 = SurroundingRectangle(math_text_1[2])
        dest_location_0 = framebox_0.get_right()
        dest_location_1 = framebox_1.get_right()
        arrow_0 = CurvedArrow(dest_location_0, dest_location_1, radius=-2.0)
        group = Group(framebox_0, framebox_1, arrow_0)

        self.play(FadeIn(group))

        math_text_2 = MathTex(
            r"-\frac{b^2}{4a}+c&=-\frac{b^2}{4a}+\frac{4ac}{4a}\\",
            r"&=(\frac{b^2}{4a}-\frac{4ac}{4a})",
        )
        framebox_2 = SurroundingRectangle(math_text_2)
        group_1 = Group(math_text_2, framebox_2).next_to(group, direction=RIGHT)
        self.play(FadeIn(group_1))
        self.wait()

        return


class Function2ndMinimumMaximum(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 5],
            y_range=[0, 40, 5],
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def function(x):
            return -2 * (x - 2) ** 2 + 10

        # plot the graph
        graph = axes.plot(function, color=PURPLE)

        # calcaulte the vertex
        vertex = Dot(point=[axes.coords_to_point(2, function(2))])
        vertex_desc = MathTex(r"(-\frac{b}{2a}, -\frac{b^2-4ac}{4a})")
        vertex_desc.scale(0.7).next_to(vertex, direction=DOWN)
        group_vertex = Group(vertex, vertex_desc)

        # y intercept
        y_intercept = Dot(point=[axes.coords_to_point(0, function(0))])
        y_intercept_desc = MathTex("c")
        y_intercept_desc.scale(0.7).next_to(y_intercept, direction=RIGHT)
        group_y_intercept = Group(y_intercept, y_intercept_desc)

        self.add(axes, labels, graph, group_vertex, group_y_intercept)

        return


class QuadraticInequality0(Scene):
    def construct(self):
        title = MathTex("ax^2+bx+c>0").to_edge(edge=UP)

        axes = Axes(x_range=[-0.5, 5], y_range=[-2, 6])
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def function(x):
            return (x - 1) * (x - 3)

        graph_0 = axes.plot(function, x_range=[-0.5, 1, 0.001], color=RED)
        graph_1 = axes.plot(function, x_range=[1, 3, 0.001], color=YELLOW)
        graph_2 = axes.plot(function, x_range=[3, 5, 0.001], color=RED)
        group_graphs = Group(graph_0, graph_1, graph_2)

        # arrows
        arrow_0_start = axes.coords_to_point(1.1, 0)
        arrow_0_end = axes.coords_to_point(-0.5, 0)
        arrow_0 = Arrow(start=arrow_0_start, end=arrow_0_end, color=RED)
        arrow_0_dot = Dot(axes.coords_to_point(1, 0), color=RED)
        arrow_0_desc = (
            MathTex(r"x<\alpha").scale(0.7).next_to(arrow_0_dot, direction=DOWN)
        )

        arrow_1_start = axes.coords_to_point(2.9, 0)
        arrow_1_end = axes.coords_to_point(5, 0)
        arrow_1 = Arrow(start=arrow_1_start, end=arrow_1_end, color=RED)
        arrow_1_dot = Dot(axes.coords_to_point(3, 0), color=RED)
        arrow_1_desc = (
            MathTex(r"x>\beta").scale(0.7).next_to(arrow_1_dot, direction=DOWN)
        )

        group_arrows = Group(
            arrow_0, arrow_0_dot, arrow_0_desc, arrow_1, arrow_1_dot, arrow_1_desc
        )

        self.add(title, axes, labels, group_graphs, group_arrows)
        return


class QuadraticInequality1(Scene):
    def construct(self):
        title = MathTex("ax^2+bx+c<0").to_edge(edge=UP)

        axes = Axes(x_range=[-0.5, 5], y_range=[-2, 6])
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def function(x):
            return (x - 1) * (x - 3)

        graph_0 = axes.plot(function, x_range=[-0.5, 1, 0.001], color=YELLOW)
        graph_1 = axes.plot(function, x_range=[1, 3, 0.001], color=RED)
        graph_2 = axes.plot(function, x_range=[3, 5, 0.001], color=YELLOW)
        group_graphs = Group(graph_0, graph_1, graph_2)

        # arrows
        arrow_0_start = axes.coords_to_point(0.9, 0)
        arrow_0_end = axes.coords_to_point(3.1, 0)
        arrow_0 = DoubleArrow(start=arrow_0_start, end=arrow_0_end, color=RED)
        arrow_0_dot_0 = Dot(axes.coords_to_point(1, 0), color=RED)
        arrow_0_dot_1 = Dot(axes.coords_to_point(3, 0), color=RED)
        arrow_0_desc = (
            MathTex(r"\alpha<x<\beta").scale(0.7).next_to(graph_1, direction=DOWN)
        )

        group_arrows = Group(arrow_0, arrow_0_dot_0, arrow_0_dot_1, arrow_0_desc)

        self.add(title, axes, labels, group_graphs, group_arrows)
        return


class ScatterPlot(Scene):
    def construct(self):
        numbers = [1, 2, 3, 4, 5, 6]
        math_scores = [50, 60, 40, 30, 70, 50]
        physics_scores = [40, 60, 40, 20, 80, 50]
        labels = [Text("Number"), Text("Math"), Text("Physics")]

        # construct table
        table = IntegerTable(
            [numbers, math_scores, physics_scores],
            row_labels=labels,
            include_outer_lines=True,
            h_buff=1,
        ).scale(0.7)
        # self.add(table)

        # add axes
        axis_length = 6.5
        x_range = [0, 100, 20]
        y_range = [0, 100, 20]
        axes = Axes(
            x_range=x_range, y_range=y_range, x_length=axis_length, y_length=axis_length
        ).add_coordinates()
        graph_labels = axes.get_axis_labels(x_label="Math", y_label="Physics")
        self.add(axes, graph_labels)

        # add dots
        dots = []
        for index in range(len(numbers)):
            math_score = math_scores[index]
            physics_score = physics_scores[index]
            position = axes.coords_to_point(math_score, physics_score)
            dots.append(Dot(position))
        self.add(*dots)

        return


class ScatterPlot2(Scene):
    def construct(self):
        numbers = [1, 2, 3, 4, 5, 6]
        math_scores = [50, 60, 40, 30, 70, 50]
        talls = [173, 173, 170, 178, 167, 177]
        labels = [Text("Number"), Text("Math"), Text("Tall")]

        # construct table
        table = IntegerTable(
            [numbers, math_scores, talls],
            row_labels=labels,
            include_outer_lines=True,
            h_buff=1,
        ).scale(0.7)
        # self.add(table)

        # add axes
        axis_length = 6.5
        x_range = [0, 100, 20]
        y_range = [165, 180, 5]
        axes = Axes(
            x_range=x_range, y_range=y_range, x_length=axis_length, y_length=axis_length
        ).add_coordinates()
        graph_labels = axes.get_axis_labels(x_label="Math", y_label="Tall")

        # add dots
        dots = []
        positions = []
        for index in range(len(numbers)):
            math_score = math_scores[index]
            tall = talls[index]
            position = axes.coords_to_point(math_score, tall)
            dots.append(Dot(position))
            positions.append(position)
        group_dots = Group(*dots)

        self.add(axes, graph_labels, group_dots)

        return


class CorrelationCoefficientTable(Scene):
    def construct(self):
        numbers = ["1", "2", "3", "...", "n"]
        x_range = [r"x_1", r"x_2", r"x_3", "...", r"x_n"]
        y_range = [r"y_1", r"y_2", r"y_3", "...", r"y_n"]
        labels = [MathTex("number"), MathTex("x"), MathTex("y")]

        # construct table
        table = MathTable(
            [numbers, x_range, y_range],
            row_labels=labels,
            include_outer_lines=True,
            h_buff=1,
        ).scale(0.7)
        self.add(table)

        return


class CorrelationCoefficient(Scene):
    def construct(self):
        numbers = ["1", "2", "3", "4", "5", "6", "Sum", "Avg"]
        math_scores = ["50", "60", "40", "30", "70", "50", "300", "50.00"]
        physics_scores = ["40", "60", "40", "20", "80", "50", "290", "48.33"]
        math_minus_avg = [
            "0.00",
            "10.00",
            "-10.00",
            "-20.00",
            "20.00",
            "0.00",
            "0.00",
            "0.00",
        ]
        physics_minus_avg = [
            "-8.33",
            "11.67",
            "-8.33",
            "-28.33",
            "31.67",
            "1.67",
            "0.00",
            "0.00",
        ]
        math_minus_avg_square = [
            "0.00",
            "100.00",
            "100.00",
            "400.00",
            "400.00",
            "0.00",
            "1000.00",
            "166.67",
        ]
        physics_minus_avg_square = [
            "69.44",
            "136.11",
            "69.44",
            "802.78",
            "1002.78",
            "2.78",
            "2083.33",
            "347.22",
        ]
        physics_minus_avg_multi_math_minus_avg_square = [
            "0.00",
            "116.67",
            "83.33",
            "566.67",
            "633.33",
            "0.00",
            "1400.00",
            "233.33",
        ]

        labels = [
            MathTex("Number"),
            MathTex("Math"),
            MathTex("Physics"),
            MathTex(r"x-\overline{x}"),
            MathTex(r"y-\overline{y}"),
            MathTex(r"(x-\overline{x})^2"),
            MathTex(r"(y-\overline{y})^2"),
            MathTex(r"(x-\overline{x})(y-\overline{y})"),
        ]

        # construct table
        table = (
            MathTable(
                [
                    numbers,
                    math_scores,
                    physics_scores,
                    math_minus_avg,
                    physics_minus_avg,
                    math_minus_avg_square,
                    physics_minus_avg_square,
                    physics_minus_avg_multi_math_minus_avg_square,
                ],
                row_labels=labels,
                include_outer_lines=True,
                h_buff=1,
            )
            .scale(0.5)
            .to_edge(edge=LEFT)
        )

        table.add_highlighted_cell((2, 9), color=GREEN)
        x_avg_cell = table.get_cell((2, 9))
        x_avg_desc = (
            Tex(r"$\overline{x}$ (Avg of $x$)")
            .scale(0.5)
            .next_to(x_avg_cell, direction=RIGHT)
        )

        table.add_highlighted_cell((3, 9), color=YELLOW)
        y_avg_cell = table.get_cell((3, 9))
        y_avg_desc = (
            Tex(r"$\overline{y}$ (Avg of $y$)")
            .scale(0.5)
            .next_to(y_avg_cell, direction=RIGHT)
        )

        table.add_highlighted_cell((6, 9), color=GREEN)
        x_minus_avg_cell = table.get_cell((6, 9))
        x_minus_avg_desc = (
            Tex(r"$V_{x}$ (Variance of $x$)")
            .scale(0.5)
            .next_to(x_minus_avg_cell, direction=RIGHT)
        )

        table.add_highlighted_cell((7, 9), color=YELLOW)
        y_minus_avg_cell = table.get_cell((7, 9))
        y_minus_avg_desc = (
            Tex(r"$V_{y}$ (Variance of $y$)")
            .scale(0.5)
            .next_to(y_minus_avg_cell, direction=RIGHT)
        )

        table.add_highlighted_cell((8, 9), color=BLUE)
        covariance = table.get_cell((8, 9))
        covariance_desc = (
            Tex(r"$c_{xy}$ (Covariance)")
            .scale(0.5)
            .next_to(covariance, direction=RIGHT)
        )

        self.add(
            table,
            x_avg_desc,
            y_avg_desc,
            x_minus_avg_desc,
            y_minus_avg_desc,
            covariance_desc,
        )


class CorrelationCoefficientExplain(Scene):
    def construct(self):
        line = NumberLine(
            x_range=[-1.0, 1.2, 0.2], length=10, include_numbers=True, include_tip=True
        )
        self.add(line)

        # positive arrow
        origin = line.n2p(-0.05)
        pos_end = line.n2p(1.05)
        neg_end = line.n2p(-1.05)

        pos_arrow = Arrow(start=origin, end=pos_end, color=YELLOW).shift(UP * 0.5)
        pos_arrow_desc = (
            Text("Strong Positive Correlation Coeff.")
            .scale(0.7)
            .next_to(pos_arrow, direction=UP)
        )
        pos_arrow_group = Group(pos_arrow, pos_arrow_desc)
        self.add(pos_arrow_group)

        neg_arrow = Arrow(start=origin, end=neg_end, color=YELLOW).shift(DOWN)
        neg_arrow_desc = (
            Text("Strong Negative Correlation Coeff.")
            .scale(0.7)
            .next_to(neg_arrow, direction=DOWN)
        )
        neg_arrow_group = Group(neg_arrow, neg_arrow_desc)
        self.add(neg_arrow_group)

        return


class UnderstandingCorrelationCoefficient(Scene):
    def construct(self):
        numbers = [1, 2, 3, 4, 5, 6]
        math_scores = [50, 60, 40, 30, 70, 50]
        physics_scores = [40, 60, 40, 20, 80, 50]

        # add axes
        axis_length = 6.5
        x_range = [0, 100, 20]
        y_range = [0, 100, 20]
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=axis_length,
            y_length=axis_length,
        ).add_coordinates()
        graph_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.add(axes, graph_labels)

        # add dots
        dots = []
        for index in range(len(numbers)):
            math_score = math_scores[index]
            physics_score = physics_scores[index]
            position = axes.coords_to_point(math_score, physics_score)
            dots.append(Dot(position))
        self.add(*dots)

        # x_avg line
        x_avg = 0
        for math_score in math_scores:
            x_avg = x_avg + math_score
        x_avg = x_avg / len(math_scores)

        x_avg_start_pt = axes.coords_to_point(x_avg, 0)
        x_avg_end_pt = axes.coords_to_point(x_avg, 100)
        x_avg_line = Line(x_avg_start_pt, x_avg_end_pt, color=YELLOW)
        x_avg_line_desc = (
            MathTex("\overline{x}", color=YELLOW)
            .scale(1.2)
            .next_to(x_avg_line, direction=DOWN)
        )
        self.add(x_avg_line, x_avg_line_desc)

        # y_avg line
        y_avg = 0
        for physics_score in physics_scores:
            y_avg = y_avg + physics_score
        y_avg = y_avg / len(physics_scores)

        y_avg_start_pt = axes.coords_to_point(0, y_avg)
        y_avg_end_pt = axes.coords_to_point(100, y_avg)
        y_avg_line = Line(y_avg_start_pt, y_avg_end_pt, color=YELLOW)
        y_avg_line_desc = (
            MathTex("\overline{y}", color=YELLOW)
            .scale(1.2)
            .next_to(y_avg_line, direction=LEFT)
        )
        self.add(y_avg_line, y_avg_line_desc)

        # label dots
        x_min = 20
        x_max = 90
        y_min = 30
        y_max = 90
        label_dot_1_pos = axes.coords_to_point(x_max, y_max)
        label_dot_1 = LabeledDot("1").move_to(label_dot_1_pos)
        label_dot_2_pos = axes.coords_to_point(x_min, y_max)
        label_dot_2 = LabeledDot("2").move_to(label_dot_2_pos)
        label_dot_3_pos = axes.coords_to_point(x_min, y_min)
        label_dot_3 = LabeledDot("3").move_to(label_dot_3_pos)
        label_dot_4_pos = axes.coords_to_point(x_max, y_min)
        label_dot_4 = LabeledDot("4").move_to(label_dot_4_pos)

        self.add(label_dot_1, label_dot_2, label_dot_3, label_dot_4)

        return


class UnderstandingCorrelationCoefficient2(Scene):
    def construct(self):
        numbers = [1, 2, 3, 4, 5, 6]
        math_scores = [50, 60, 40, 30, 70, 50]
        physics_scores = [40, 60, 40, 20, 80, 50]

        # add axes
        axis_length = 6.5
        x_range = [0, 100, 20]
        y_range = [0, 100, 20]
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=axis_length,
            y_length=axis_length,
        )
        graph_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.add(axes, graph_labels)

        # x_avg line
        x_avg = 0
        for math_score in math_scores:
            x_avg = x_avg + math_score
        x_avg = x_avg / len(math_scores)

        x_avg_start_pt = axes.coords_to_point(x_avg, 0)
        x_avg_end_pt = axes.coords_to_point(x_avg, 100)
        x_avg_line = Line(x_avg_start_pt, x_avg_end_pt, color=YELLOW)
        x_avg_line_desc = (
            MathTex("\overline{x}", color=YELLOW)
            .scale(1.2)
            .next_to(x_avg_line, direction=DOWN)
        )
        self.add(x_avg_line, x_avg_line_desc)

        # y_avg line
        y_avg = 0
        for physics_score in physics_scores:
            y_avg = y_avg + physics_score
        y_avg = y_avg / len(physics_scores)

        y_avg_start_pt = axes.coords_to_point(0, y_avg)
        y_avg_end_pt = axes.coords_to_point(100, y_avg)
        y_avg_line = Line(y_avg_start_pt, y_avg_end_pt, color=YELLOW)
        y_avg_line_desc = (
            MathTex("\overline{y}", color=YELLOW)
            .scale(1.2)
            .next_to(y_avg_line, direction=LEFT)
        )
        self.add(y_avg_line, y_avg_line_desc)

        # label dots
        x_min = 20
        x_max = 90
        y_min = 30
        y_max = 90
        label_dot_1_pos = axes.coords_to_point(x_max, y_max)
        label_dot_1 = LabeledDot("1").move_to(label_dot_1_pos)
        label_dot_2_pos = axes.coords_to_point(x_min, y_max)
        label_dot_2 = LabeledDot("2").move_to(label_dot_2_pos)
        label_dot_3_pos = axes.coords_to_point(x_min, y_min)
        label_dot_3 = LabeledDot("3").move_to(label_dot_3_pos)
        label_dot_4_pos = axes.coords_to_point(x_max, y_min)
        label_dot_4 = LabeledDot("4").move_to(label_dot_4_pos)

        self.add(label_dot_1, label_dot_2, label_dot_3, label_dot_4)

        # dots (x=70, y=70)
        dot_position = axes.coords_to_point(70, 70)
        dot = Dot(dot_position, color=RED)

        # area
        avg_position = axes.coords_to_point(x_avg, y_avg)
        width = dot_position[0] - avg_position[0]
        height = dot_position[1] - avg_position[1]

        area_position = (dot_position + avg_position) / 2.0
        area = Rectangle(
            width=width, height=height, fill_color=GRAY, fill_opacity=1
        ).move_to(area_position)

        # area desc
        area_x_min = area_position[0] - width / 2.0
        area_x_max = area_position[0] + width / 2.0
        area_y_min = area_position[1] - height / 2.0
        area_y_max = area_position[1] + height / 2.0

        area_x_brace = BraceBetweenPoints(
            [area_x_min, area_y_min, 0], [area_x_max, area_y_min, 0]
        )
        area_x_desc = (
            MathTex("x-\overline{x}").scale(0.7).next_to(area_x_brace, direction=DOWN)
        )

        area_y_brace = BraceBetweenPoints(
            [area_x_max, area_y_min, 0], [area_x_max, area_y_max, 0]
        )
        area_y_desc = (
            MathTex("y-\overline{y}").scale(0.7).next_to(area_y_brace, direction=RIGHT)
        )

        self.add(area, dot, area_x_brace, area_x_desc, area_y_brace, area_y_desc)

        return


class DeepThinkingCorrelationCoefficient(Scene):
    def construct(self):
        numbers = [1, 2, 3, 4, 5, 6]
        math_scores = [50, 60, 40, 30, 70, 50]
        physics_scores = [80, 50, 40, 60, 40, 20]
        labels = [Text("Number"), Text("Math"), Text("Physics")]

        # construct table
        table = IntegerTable(
            [numbers, math_scores, physics_scores],
            row_labels=labels,
            include_outer_lines=True,
            h_buff=1,
        ).scale(0.7)
        # self.add(table)

        # add axes
        axis_length = 6.5
        x_range = [0, 100, 20]
        y_range = [0, 100, 20]
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=axis_length,
            y_length=axis_length,
        ).add_coordinates()
        graph_labels = axes.get_axis_labels(x_label="Math", y_label="Physics")
        self.add(axes, graph_labels)

        # add dots
        dots = []
        for index in range(len(numbers)):
            math_score = math_scores[index]
            physics_score = physics_scores[index]
            position = axes.coords_to_point(math_score, physics_score)
            dots.append(Dot(position))
        self.add(*dots)

        # x_avg line
        x_avg = 0
        for math_score in math_scores:
            x_avg = x_avg + math_score
        x_avg = x_avg / len(math_scores)

        x_avg_start_pt = axes.coords_to_point(x_avg, 0)
        x_avg_end_pt = axes.coords_to_point(x_avg, 100)
        x_avg_line = Line(x_avg_start_pt, x_avg_end_pt, color=YELLOW)
        x_avg_line_desc = (
            MathTex("\overline{x}", color=YELLOW)
            .scale(1.2)
            .next_to(x_avg_line, direction=DOWN)
        )
        self.add(x_avg_line, x_avg_line_desc)

        # y_avg line
        y_avg = 0
        for physics_score in physics_scores:
            y_avg = y_avg + physics_score
        y_avg = y_avg / len(physics_scores)

        y_avg_start_pt = axes.coords_to_point(0, y_avg)
        y_avg_end_pt = axes.coords_to_point(100, y_avg)
        y_avg_line = Line(y_avg_start_pt, y_avg_end_pt, color=YELLOW)
        y_avg_line_desc = (
            MathTex("\overline{y}", color=YELLOW)
            .scale(1.2)
            .next_to(y_avg_line, direction=LEFT)
        )
        self.add(y_avg_line, y_avg_line_desc)

        # label dots
        x_min = 20
        x_max = 90
        y_min = 30
        y_max = 90
        label_dot_1_pos = axes.coords_to_point(x_max, y_max)
        label_dot_1 = LabeledDot("1").move_to(label_dot_1_pos)
        label_dot_2_pos = axes.coords_to_point(x_min, y_max)
        label_dot_2 = LabeledDot("2").move_to(label_dot_2_pos)
        label_dot_3_pos = axes.coords_to_point(x_min, y_min)
        label_dot_3 = LabeledDot("3").move_to(label_dot_3_pos)
        label_dot_4_pos = axes.coords_to_point(x_max, y_min)
        label_dot_4 = LabeledDot("4").move_to(label_dot_4_pos)

        self.add(label_dot_1, label_dot_2, label_dot_3, label_dot_4)

        return


class Combination(Scene):
    def construct(self):
        square = Square(side_length=3.0)
        point_A = Text("A").scale(0.7).next_to(square, UL)
        point_B = Text("B").scale(0.7).next_to(square, DL)
        point_C = Text("C").scale(0.7).next_to(square, DR)
        point_D = Text("D").scale(0.7).next_to(square, UR)
        group_square = Group(square, point_A, point_B, point_C, point_D)
        self.add(group_square)

        square_vertices = square.get_vertices()
        marked_triangle = Polygon(
            square_vertices[0],
            square_vertices[1],
            square_vertices[2],
            color=RED,
            fill_opacity=0.5,
        )
        self.add(marked_triangle)

        return


class BinormialCoefficient(Scene):
    def construct(self):
        equation = MathTex(r"(a+b)", r"\times", r"(a+b)", r"\times", r"(a+b)").shift(UP)
        self.add(equation)

        coeff_0_0 = MathTex(r"a").next_to(equation[0], direction=DOWN * 2)
        coeff_1_0 = MathTex(r"a").next_to(coeff_0_0, direction=DOWN * 2)
        coeff_2_0 = MathTex(r"b").next_to(coeff_1_0, direction=DOWN * 2)
        marked_coeff_2_0 = SurroundingRectangle(coeff_2_0)
        group_col_0 = Group(coeff_0_0, coeff_1_0, coeff_2_0, marked_coeff_2_0)
        brace_obj = Brace(group_col_0, direction=LEFT)
        brace_desc = brace_obj.get_text("Three!")
        self.add(group_col_0, brace_obj, brace_desc)

        coeff_0_1 = MathTex(r"a").next_to(equation[2], direction=DOWN * 2)
        coeff_1_1 = MathTex(r"b").next_to(coeff_0_1, direction=DOWN * 2)
        coeff_2_1 = MathTex(r"a").next_to(coeff_1_1, direction=DOWN * 2)
        marked_coeff_2_1 = SurroundingRectangle(coeff_1_1)
        group_col_1 = Group(coeff_0_1, coeff_1_1, coeff_2_1, marked_coeff_2_1)
        self.add(group_col_1)

        coeff_0_2 = MathTex(r"b").next_to(equation[4], direction=DOWN * 2)
        coeff_1_2 = MathTex(r"a").next_to(coeff_0_2, direction=DOWN * 2)
        coeff_2_2 = MathTex(r"a").next_to(coeff_1_2, direction=DOWN * 2)
        marked_coeff_2_2 = SurroundingRectangle(coeff_0_2)
        group_col_2 = Group(coeff_0_2, coeff_1_2, coeff_2_2, marked_coeff_2_2)
        self.add(group_col_2)

        return


class Subset(Scene):
    def construct(self):
        element_B_0 = MathTex("6").scale(0.8).move_to([0, -1, 0])
        element_B_1 = MathTex("8").scale(0.8).move_to([0, 0, 0])
        element_B_2 = MathTex("24").scale(0.8).move_to([1, -0.5, 0])

        set_B = Group(element_B_0, element_B_1, element_B_2)
        set_B_outline = SurroundingRectangle(set_B, corner_radius=0.2, buff=0.5)
        set_B_title = MathTex("B").next_to(set_B, direction=UP * 2.5)

        element_A_0 = MathTex("1").scale(0.8).move_to([-2.5, 1.5, 0])
        element_A_1 = MathTex("2").scale(0.8).move_to([-1.5, 1.5, 0])
        element_A_2 = MathTex("3").scale(0.8).move_to([-0.5, 1.5, 0])
        element_A_3 = MathTex("4").scale(0.8).move_to([-2.5, 0.5, 0])
        element_A_4 = MathTex("12").scale(0.8).move_to([-2.5, -0.5, 0])
        set_A = Group(
            element_A_0,
            element_A_1,
            element_A_2,
            element_A_3,
            element_A_4,
            set_B,
            set_B_outline,
            set_B_title,
        )
        set_A_outline = SurroundingRectangle(set_A, corner_radius=0.2, buff=0.5)
        set_A_title = MathTex("A").next_to(set_A, direction=UP * 2.5)
        self.add(set_A, set_A_outline, set_A_title)

        return


class DiceCombination(Scene):
    def construct(self):
        table = MathTable(
            [
                ["(1,1)", "(1,2)", "(1,3)", "(1,4)", "(1,5)", "(1,6)"],
                ["(2,1)", "(2,2)", "(2,3)", "(2,4)", "(2,5)", "(2,6)"],
                ["(3,1)", "(3,2)", "(3,3)", "(3,4)", "(3,5)", "(3,6)"],
                ["(4,1)", "(4,2)", "(4,3)", "(4,4)", "(4,5)", "(4,6)"],
                ["(5,1)", "(5,2)", "(5,3)", "(5,4)", "(5,5)", "(5,6)"],
                ["(6,1)", "(6,2)", "(6,3)", "(6,4)", "(6,5)", "(6,6)"],
            ],
            include_outer_lines=True,
        ).scale(0.9)

        self.add(table)

        highlighted_cell_0 = table.get_highlighted_cell((1, 2))
        highlighted_cell_1 = table.get_highlighted_cell((2, 1))
        highlighted_cell_2 = table.get_highlighted_cell((1, 1), color=RED)
        highlighted_cells = Group(
            highlighted_cell_0, highlighted_cell_1, highlighted_cell_2
        )

        self.play(FadeIn(highlighted_cells))
        self.wait()

        self.play(FadeOut(highlighted_cells))
        self.wait()

        return


class UnionAndIntersection(Scene):
    def construct(self):
        ellipse_A = Ellipse(
            width=5.0, height=4.0, fill_opacity=0.5, color=BLUE, stroke_width=10
        ).move_to(LEFT)
        ellipse_B = Ellipse(
            width=5.0, height=4.0, fill_opacity=0.5, color=RED, stroke_width=10
        ).move_to(RIGHT)

        set_A_desc = MathTex("A", color=GOLD).next_to(ellipse_A, direction=UP)
        set_B_desc = MathTex("B", color=GOLD).next_to(ellipse_B, direction=UP)

        group_set_A = Group(ellipse_A, set_A_desc)
        group_set_B = Group(ellipse_B, set_B_desc)
        group_union = Group(group_set_A, group_set_B)

        union_rect = SurroundingRectangle(group_union, buff=0.5, corner_radius=0.2)
        union_desc = MathTex("U", color=GOLD).next_to(union_rect, direction=UP)
        total_group = Group(group_union, union_rect, union_desc)

        element_0 = MathTex("3").move_to([0, 0.5, 0])
        element_1 = MathTex("5").move_to([0, -0.5, 0])
        element_2 = MathTex("1").move_to([-2.5, 0, 0])
        element_3 = MathTex("2").move_to([2.5, 0, 0])
        element_4 = MathTex("4").move_to([-3, 2, 0])
        element_5 = MathTex("6").move_to([3, 2, 0])

        element_group = Group(
            element_0, element_1, element_2, element_3, element_4, element_5
        )

        self.add(group_set_A, group_set_B, total_group, element_group)
        return


class UnionShape(Scene):
    def construct(self):
        ellipse_A = Ellipse(width=5.0, height=4.0, color=BLUE, stroke_width=10).move_to(
            LEFT
        )
        ellipse_B = Ellipse(width=5.0, height=4.0, color=RED, stroke_width=10).move_to(
            RIGHT
        )

        union_A_B = Union(ellipse_A, ellipse_B, color=ORANGE, fill_opacity=0.5)

        set_A_desc = MathTex("A", color=GOLD).next_to(ellipse_A, direction=UP)
        set_B_desc = MathTex("B", color=GOLD).next_to(ellipse_B, direction=UP)

        group_set_A = Group(set_A_desc)
        group_set_B = Group(set_B_desc)
        group_union = Group(union_A_B, group_set_A, group_set_B)

        union_rect = SurroundingRectangle(group_union, buff=0.5, corner_radius=0.2)
        union_desc = MathTex("U", color=GOLD).next_to(union_rect, direction=UP)
        total_group = Group(group_union, union_rect, union_desc)

        self.add(group_set_A, group_set_B, total_group)
        return


class IntersectionShape(Scene):
    def construct(self):
        ellipse_A = Ellipse(width=5.0, height=4.0, color=BLUE, stroke_width=10).move_to(
            LEFT
        )
        ellipse_B = Ellipse(width=5.0, height=4.0, color=RED, stroke_width=10).move_to(
            RIGHT
        )

        intersection_A_B = Intersection(
            ellipse_A, ellipse_B, color=ORANGE, fill_opacity=0.5
        )

        set_A_desc = MathTex("A", color=GOLD).next_to(ellipse_A, direction=UP)
        set_B_desc = MathTex("B", color=GOLD).next_to(ellipse_B, direction=UP)

        group_set_A = Group(ellipse_A, set_A_desc)
        group_set_B = Group(ellipse_B, set_B_desc)
        group_union = Group(intersection_A_B, group_set_A, group_set_B)

        union_rect = SurroundingRectangle(group_union, buff=0.5, corner_radius=0.2)
        union_desc = MathTex("U", color=GOLD).next_to(union_rect, direction=UP)
        total_group = Group(group_union, union_rect, union_desc)

        self.add(group_set_A, group_set_B, total_group)
        return


class MutuallyExclusive(Scene):
    def construct(self):
        ellipse_A = Ellipse(
            width=4.0, height=4.0, color=BLUE, stroke_width=10, fill_opacity=0.5
        ).move_to(LEFT * 2.5)
        ellipse_B = Ellipse(
            width=4.0, height=4.0, color=RED, stroke_width=10, fill_opacity=0.5
        ).move_to(RIGHT * 2.5)

        set_A_desc = MathTex("A", color=GOLD).next_to(ellipse_A, direction=UP)
        set_B_desc = MathTex("B", color=GOLD).next_to(ellipse_B, direction=UP)

        group_set_A = Group(ellipse_A, set_A_desc)
        group_set_B = Group(ellipse_B, set_B_desc)
        group_union = Group(group_set_A, group_set_B)

        union_rect = SurroundingRectangle(group_union, buff=0.5, corner_radius=0.2)
        union_desc = MathTex("U", color=GOLD).next_to(union_rect, direction=UP)
        total_group = Group(group_union, union_rect, union_desc)

        self.add(group_set_A, group_set_B, total_group)
        return


class IndependentTrial(Scene):
    def construct(self):
        cross = VGroup(
            Line(UP + LEFT, DOWN + RIGHT),
            Line(UP + RIGHT, DOWN + LEFT),
        )
        circle = Circle().set_color(RED).scale(0.2)
        cross = cross.set_color(BLUE).scale(0.2)

        table = (
            MobjectTable(
                [
                    [
                        Text(""),
                        circle.copy(),
                        circle.copy(),
                        cross.copy(),
                        cross.copy(),
                        cross.copy(),
                    ],
                    [circle.copy(), Text(""), Text(""), Text(""), Text(""), Text("")],
                    [circle.copy(), Text(""), Text(""), Text(""), Text(""), Text("")],
                    [cross.copy(), Text(""), Text(""), Text(""), Text(""), Text("")],
                    [cross.copy(), Text(""), Text(""), Text(""), Text(""), Text("")],
                    [cross.copy(), Text(""), Text(""), Text(""), Text(""), Text("")],
                ]
            )
            .scale(0.8)
            .shift(DOWN * 0.5)
        )

        # high lighted cells
        highlighted_cell_0 = table.get_highlighted_cell((2, 2), color=GREEN)
        highlighted_cell_1 = table.get_highlighted_cell((3, 2), color=GREEN)
        highlighted_cell_2 = table.get_highlighted_cell((2, 3), color=GREEN)
        highlighted_cell_3 = table.get_highlighted_cell((3, 3), color=GREEN)
        highlighted_cells = Group(
            highlighted_cell_0,
            highlighted_cell_1,
            highlighted_cell_2,
            highlighted_cell_3,
        )

        # brace
        cell_0 = table.get_cell((2, 1))
        cell_1 = table.get_cell((3, 1))
        brace_B_cells = Group(cell_0, cell_1)
        brace_B = Brace(brace_B_cells, direction=LEFT)
        brace_B_desc = Text("Event B").scale(0.6).next_to(brace_B, direction=LEFT)

        cell_0 = table.get_cell((1, 2))
        cell_1 = table.get_cell((1, 3))
        brace_A_cells = Group(cell_0, cell_1)
        brace_A = Brace(brace_A_cells, direction=UP)
        brace_A_desc = Text("Event A").scale(0.6).next_to(brace_A, direction=UP)

        braces = Group(brace_B, brace_B_desc, brace_A, brace_A_desc)

        self.add(table, highlighted_cells, braces)
        return


class RepeatTrial(Scene):
    def construct(self):
        cross = VGroup(
            Line(UP + LEFT, DOWN + RIGHT),
            Line(UP + RIGHT, DOWN + LEFT),
        )
        circle = Circle().set_color(RED).scale(0.2)
        cross = cross.set_color(BLUE).scale(0.2)

        table = MobjectTable(
            [
                [
                    Text("1 Try"),
                    Text("2 Try"),
                    Text("3 Try"),
                    Text("4 Try"),
                    Text("Percentage"),
                ],
                [
                    circle.copy(),
                    circle.copy(),
                    cross.copy(),
                    cross.copy(),
                    MathTex(r"(\frac{1}{6})^2(\frac{5}{6})^2"),
                ],
                [
                    circle.copy(),
                    cross.copy(),
                    circle.copy(),
                    cross.copy(),
                    MathTex(r"(\frac{1}{6})^2(\frac{5}{6})^2"),
                ],
                [
                    circle.copy(),
                    cross.copy(),
                    cross.copy(),
                    circle.copy(),
                    MathTex(r"(\frac{1}{6})^2(\frac{5}{6})^2"),
                ],
                [
                    cross.copy(),
                    circle.copy(),
                    circle.copy(),
                    cross.copy(),
                    MathTex(r"(\frac{1}{6})^2(\frac{5}{6})^2"),
                ],
                [
                    cross.copy(),
                    circle.copy(),
                    cross.copy(),
                    circle.copy(),
                    MathTex(r"(\frac{1}{6})^2(\frac{5}{6})^2"),
                ],
                [
                    cross.copy(),
                    cross.copy(),
                    circle.copy(),
                    circle.copy(),
                    MathTex(r"(\frac{1}{6})^2(\frac{5}{6})^2"),
                ],
            ]
        ).scale(0.5)

        brace_cells = []
        for index in range(6):
            row_index = 2 + index
            col_index = 1
            selected_cell = table.get_cell((row_index, col_index))
            brace_cells.append(selected_cell)
        brace_cell_group = Group(*brace_cells)
        brace = Brace(brace_cell_group, direction=LEFT)
        brace_text = Tex(r"$_4C_2=6$").next_to(brace, direction=LEFT)

        self.add(table, brace, brace_text)

        return


class ArithmeticSequence(Scene):
    def construct(self):
        # scale
        direction_scale = 8.0

        # a_3 is middle value
        a_3 = MathTex(r"a_3")

        # a_1, a_2 is left values
        a_2 = MathTex(r"a_2").next_to(a_3, direction=LEFT * direction_scale)
        a_1 = MathTex(r"a_1").next_to(a_2, direction=LEFT * direction_scale)

        # a_4, a_5 is right values
        a_4 = MathTex(r"a_4").next_to(a_3, direction=RIGHT * direction_scale)
        a_5 = MathTex(r"a_5").next_to(a_4, direction=RIGHT * direction_scale)

        a_group = Group(a_1, a_2, a_3, a_4, a_5)
        self.add(a_group)

        a_1_pt = a_1.get_top() + UP * 0.3
        a_2_pt = a_2.get_top() + UP * 0.3
        a_3_pt = a_3.get_top() + UP * 0.3
        a_4_pt = a_4.get_top() + UP * 0.3
        a_5_pt = a_5.get_top() + UP * 0.3

        arrow_radius = -2.0

        arrow_0 = CurvedArrow(a_1_pt, a_2_pt, radius=arrow_radius)
        arrow_0_desc = MathTex(r"+d").next_to(arrow_0, direction=UP)

        arrow_1 = CurvedArrow(a_2_pt, a_3_pt, radius=arrow_radius)
        arrow_1_desc = MathTex(r"+d").next_to(arrow_1, direction=UP)

        arrow_2 = CurvedArrow(a_3_pt, a_4_pt, radius=arrow_radius)
        arrow_2_desc = MathTex(r"+d").next_to(arrow_2, direction=UP)

        arrow_3 = CurvedArrow(a_4_pt, a_5_pt, radius=arrow_radius)
        arrow_3_desc = MathTex(r"+d").next_to(arrow_3, direction=UP)

        arrow_group = Group(
            arrow_0,
            arrow_0_desc,
            arrow_1,
            arrow_1_desc,
            arrow_2,
            arrow_2_desc,
            arrow_3,
            arrow_3_desc,
        )
        self.add(arrow_group)

        return


class ArithmeticSequenceSum(Scene):
    def construct(self):
        # common difference
        d = 0.8
        rect_width = 0.8

        # rects
        a_1_shift = LEFT * 5.5 + DOWN * 2.0

        # a_1
        a_1 = 1.2
        a_1_rect = Rectangle(width=rect_width, height=a_1).shift(a_1_shift)
        a_1_center = a_1_rect.get_center()
        a_1_text = MathTex(r"a_1").move_to(a_1_center)
        a_1_brace = Brace(a_1_rect, direction=LEFT, buff=0.1)
        a_1_desc = MathTex(r"a_1").next_to(a_1_brace, direction=LEFT)
        a_1_down_brace = Brace(a_1_rect, direction=DOWN, buff=0.1)
        a_1_down_brace_text = MathTex(r"1").next_to(a_1_down_brace, direction=DOWN)
        a_1_group = Group(
            a_1_rect, a_1_text, a_1_brace, a_1_desc, a_1_down_brace, a_1_down_brace_text
        )

        # a_2
        a_2 = a_1 + d
        a_2_rect = Rectangle(width=rect_width, height=a_2).next_to(
            a_1_rect, buff=0.0, direction=RIGHT, aligned_edge=DOWN
        )
        a_2_center = a_2_rect.get_center()
        a_2_text = MathTex(r"a_2").move_to(a_2_center)
        brace_start_pt = a_2_rect.get_corner(UL)
        brace_end_pt = a_1_rect.get_corner(UR)
        a_2_brace = BraceBetweenPoints(brace_start_pt, brace_end_pt, buff=0.1)
        a_2_brace_tex = MathTex(r"d").next_to(a_2_brace, direction=LEFT)
        a_2_group = Group(a_2_rect, a_2_text, a_2_brace, a_2_brace_tex)

        # a_3
        a_3 = a_2 + d
        a_3_rect = Rectangle(width=rect_width, height=a_3).next_to(
            a_2_rect, buff=0.0, direction=RIGHT, aligned_edge=DOWN
        )
        a_3_center = a_3_rect.get_center()
        a_3_text = MathTex(r"a_3").move_to(a_3_center)
        a_3_group = Group(a_3_rect, a_3_text)

        # a_4
        a_4 = a_3 + d
        a_4_rect = Rectangle(width=rect_width, height=a_4).next_to(
            a_3_rect, buff=0.0, direction=RIGHT, aligned_edge=DOWN
        )
        a_4_center = a_4_rect.get_center()
        a_4_text = MathTex(r"a_4").move_to(a_4_center)
        a_4_group = Group(a_4_rect, a_4_text)

        # a_5
        a_5 = a_4 + d
        a_5_rect = Rectangle(width=rect_width, height=a_5).next_to(
            a_4_rect, buff=0.0, direction=RIGHT, aligned_edge=DOWN
        )
        a_5_center = a_5_rect.get_center()
        a_5_text = MathTex(r"a_5").move_to(a_5_center)
        a_5_brace = Brace(a_5_rect, direction=RIGHT, buff=0.1)
        a_5_brace_text = MathTex(r"a_5").next_to(a_5_brace, direction=RIGHT)
        a_5_group = Group(a_5_rect, a_5_text, a_5_brace, a_5_brace_text)

        # x2
        left_rect_group = Group(a_1_group, a_2_group, a_3_group, a_4_group, a_5_group)
        left_rect_group_text = (
            MathTex(r"\times 2 =", color=YELLOW)
            .scale(1.5)
            .next_to(left_rect_group, direction=RIGHT)
        )

        self.add(left_rect_group, left_rect_group_text)

        # sum a_1
        a_1_rect_right = Rectangle(width=rect_width, height=a_1).shift(DOWN * 2.0)
        a_1_center_right = a_1_rect_right.get_center()
        a_1_text_right = MathTex(r"a_1").move_to(a_1_center_right)
        a_1_sum_rect = Rectangle(width=rect_width, height=a_5, color=RED).next_to(
            a_1_rect_right, buff=0.0, direction=UP
        )
        a_1_sum_rect_center = a_1_sum_rect.get_center()
        a_1_sum_rect_text = MathTex(r"a_5").move_to(a_1_sum_rect_center)
        a_1_sum_group = Group(
            a_1_rect_right,
            a_1_text_right,
            a_1_sum_rect,
            a_1_sum_rect_text,
        )

        # sum a_2
        a_2_rect_right = Rectangle(width=rect_width, height=a_2).next_to(
            a_1_rect_right, buff=0.0, direction=RIGHT, aligned_edge=DOWN
        )
        a_2_center_right = a_2_rect_right.get_center()
        a_2_text_right = MathTex(r"a_2").move_to(a_2_center_right)
        a_2_sum_rect = Rectangle(width=rect_width, height=a_4, color=RED).next_to(
            a_2_rect_right, buff=0.0, direction=UP
        )
        a_2_sum_rect_center = a_2_sum_rect.get_center()
        a_2_sum_rect_text = MathTex(r"a_4").move_to(a_2_sum_rect_center)
        a_2_sum_group = Group(
            a_2_rect_right,
            a_2_text_right,
            a_2_sum_rect,
            a_2_sum_rect_text,
        )

        # sum a_3
        a_3_rect_right = Rectangle(width=rect_width, height=a_3).next_to(
            a_2_rect_right, buff=0.0, direction=RIGHT, aligned_edge=DOWN
        )
        a_3_center_right = a_3_rect_right.get_center()
        a_3_text_right = MathTex(r"a_3").move_to(a_3_center_right)
        a_3_sum_rect = Rectangle(width=rect_width, height=a_3, color=RED).next_to(
            a_3_rect_right, buff=0.0, direction=UP
        )
        a_3_sum_rect_center = a_3_sum_rect.get_center()
        a_3_sum_rect_text = MathTex(r"a_3").move_to(a_3_sum_rect_center)
        a_3_sum_group = Group(
            a_3_rect_right,
            a_3_text_right,
            a_3_sum_rect,
            a_3_sum_rect_text,
        )

        # sum a_4
        a_4_rect_right = Rectangle(width=rect_width, height=a_4).next_to(
            a_3_rect_right, buff=0.0, direction=RIGHT, aligned_edge=DOWN
        )
        a_4_center_right = a_4_rect_right.get_center()
        a_4_text_right = MathTex(r"a_4").move_to(a_4_center_right)
        a_4_sum_rect = Rectangle(width=rect_width, height=a_2, color=RED).next_to(
            a_4_rect_right, buff=0.0, direction=UP
        )
        a_4_sum_rect_center = a_4_sum_rect.get_center()
        a_4_sum_rect_text = MathTex(r"a_2").move_to(a_4_sum_rect_center)
        a_4_sum_group = Group(
            a_4_rect_right,
            a_4_text_right,
            a_4_sum_rect,
            a_4_sum_rect_text,
        )

        # sum a_5
        a_5_rect_right = Rectangle(width=rect_width, height=a_5).next_to(
            a_4_rect_right, buff=0.0, direction=RIGHT, aligned_edge=DOWN
        )
        a_5_center_right = a_5_rect_right.get_center()
        a_5_text_right = MathTex(r"a_5").move_to(a_5_center_right)
        a_5_sum_rect = Rectangle(width=rect_width, height=a_1, color=RED).next_to(
            a_5_rect_right, buff=0.0, direction=UP
        )
        a_5_sum_rect_center = a_5_sum_rect.get_center()
        a_5_sum_rect_text = MathTex(r"a_1").move_to(a_5_sum_rect_center)
        a_5_sum_group = Group(
            a_5_rect_right,
            a_5_text_right,
            a_5_sum_rect,
            a_5_sum_rect_text,
        )

        right_rect_group = Group(
            a_1_sum_group, a_2_sum_group, a_3_sum_group, a_4_sum_group, a_5_sum_group
        ).shift(RIGHT * 2)
        self.add(right_rect_group)

        return


class GeometricSequence(Scene):
    def construct(self):
        # scale
        direction_scale = 8.0

        # a_3 is middle value
        a_3 = MathTex(r"a_3")

        # a_1, a_2 is left values
        a_2 = MathTex(r"a_2").next_to(a_3, direction=LEFT * direction_scale)
        a_1 = MathTex(r"a_1").next_to(a_2, direction=LEFT * direction_scale)

        # a_4, a_5 is right values
        a_4 = MathTex(r"a_4").next_to(a_3, direction=RIGHT * direction_scale)
        a_5 = MathTex(r"a_5").next_to(a_4, direction=RIGHT * direction_scale)

        a_group = Group(a_1, a_2, a_3, a_4, a_5)
        self.add(a_group)

        a_1_pt = a_1.get_top() + UP * 0.3
        a_2_pt = a_2.get_top() + UP * 0.3
        a_3_pt = a_3.get_top() + UP * 0.3
        a_4_pt = a_4.get_top() + UP * 0.3
        a_5_pt = a_5.get_top() + UP * 0.3

        arrow_radius = -2.0

        arrow_0 = CurvedArrow(a_1_pt, a_2_pt, radius=arrow_radius)
        arrow_0_desc = MathTex(r"\times r").next_to(arrow_0, direction=UP)

        arrow_1 = CurvedArrow(a_2_pt, a_3_pt, radius=arrow_radius)
        arrow_1_desc = MathTex(r"\times r").next_to(arrow_1, direction=UP)

        arrow_2 = CurvedArrow(a_3_pt, a_4_pt, radius=arrow_radius)
        arrow_2_desc = MathTex(r"\times r").next_to(arrow_2, direction=UP)

        arrow_3 = CurvedArrow(a_4_pt, a_5_pt, radius=arrow_radius)
        arrow_3_desc = MathTex(r"\times r").next_to(arrow_3, direction=UP)

        arrow_group = Group(
            arrow_0,
            arrow_0_desc,
            arrow_1,
            arrow_1_desc,
            arrow_2,
            arrow_2_desc,
            arrow_3,
            arrow_3_desc,
        )
        self.add(arrow_group)

        return


class RandomVariable1(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X"),
                    MathTex(r"1"),
                    MathTex(r"2"),
                    MathTex(r"3"),
                    MathTex(r"4"),
                    MathTex(r"5"),
                    MathTex(r"6"),
                ],
                [
                    MathTex(r"P"),
                    MathTex(r"\frac{1}{6}"),
                    MathTex(r"\frac{1}{6}"),
                    MathTex(r"\frac{1}{6}"),
                    MathTex(r"\frac{1}{6}"),
                    MathTex(r"\frac{1}{6}"),
                    MathTex(r"\frac{1}{6}"),
                ],
            ],
            include_outer_lines=True,
        )
        self.add(table)
        return


class ProbabilityDistribution(Scene):
    def construct(self):
        x_range = [0, 7, 1]
        y_range = [0, 2.0 / 6, 1.0 / 6]
        y_label = {}
        y_label[1.0 / 6] = MathTex(r"\frac{1}{6}")
        x_labels = [1, 2, 3, 4, 5, 6]
        axes = Axes(x_range=x_range, y_range=y_range).add_coordinates(x_labels, y_label)

        # axis label
        axis_labels = axes.get_axis_labels(x_label="X", y_label="P")

        # dots
        dot_radius = 0.1
        dots = []
        for index in range(6):
            y_value = 1.0 / 6
            position = axes.coords_to_point(index + 1, y_value)
            dots.append(Dot(position, radius=dot_radius))

        group_dots = Group(*dots)

        self.add(axes, axis_labels, group_dots)
        return


class RandomVariable2(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X"),
                    MathTex(r"x_1"),
                    MathTex(r"x_2"),
                    MathTex(r"x_3"),
                    MathTex(r"\cdots"),
                    MathTex(r"x_n"),
                ],
                [
                    MathTex(r"P"),
                    MathTex(r"p_1"),
                    MathTex(r"p_2"),
                    MathTex(r"p_3"),
                    MathTex(r"\cdots"),
                    MathTex(r"p_n"),
                ],
            ],
            include_outer_lines=True,
        )
        self.add(table)
        return


class RandomVariable3(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X"),
                    MathTex(r"2"),
                    MathTex(r"3"),
                    MathTex(r"4"),
                    MathTex(r"5"),
                    MathTex(r"6"),
                    MathTex(r"7"),
                    MathTex(r"8"),
                    MathTex(r"9"),
                    MathTex(r"10"),
                    MathTex(r"11"),
                    MathTex(r"12"),
                ],
                [
                    MathTex(r"P"),
                    MathTex(r"\frac{1}{36}"),
                    MathTex(r"\frac{2}{36}"),
                    MathTex(r"\frac{3}{36}"),
                    MathTex(r"\frac{4}{36}"),
                    MathTex(r"\frac{5}{36}"),
                    MathTex(r"\frac{6}{36}"),
                    MathTex(r"\frac{5}{36}"),
                    MathTex(r"\frac{4}{36}"),
                    MathTex(r"\frac{3}{36}"),
                    MathTex(r"\frac{2}{36}"),
                    MathTex(r"\frac{1}{36}"),
                ],
            ],
            include_outer_lines=True,
        ).scale(0.6)
        self.add(table)
        return


class ProbabilityDistribution2(Scene):
    def construct(self):
        x_range = [0, 13, 1]
        y_range = [0, 6.5 / 36, 1.0 / 36]
        y_labels = {}
        y_labels[1.0 / 36] = MathTex(r"\frac{1}{36}")
        y_labels[2.0 / 36] = MathTex(r"\frac{2}{36}")
        y_labels[3.0 / 36] = MathTex(r"\frac{3}{36}")
        y_labels[4.0 / 36] = MathTex(r"\frac{4}{36}")
        y_labels[5.0 / 36] = MathTex(r"\frac{5}{36}")
        y_labels[6.0 / 36] = MathTex(r"\frac{6}{36}")
        x_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        axes = Axes(x_range=x_range, y_range=y_range).add_coordinates(
            x_labels, y_labels
        )

        # axis label
        axis_labels = axes.get_axis_labels(x_label="X", y_label="P")

        # dots
        dot_radius = 0.1
        dots = []

        position = axes.coords_to_point(2, 1.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(3, 2.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(4, 3.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(5, 4.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(6, 5.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(7, 6.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(8, 5.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(9, 4.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(10, 3.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(11, 2.0 / 36)
        dots.append(Dot(position, radius=dot_radius))
        position = axes.coords_to_point(12, 1.0 / 36)
        dots.append(Dot(position, radius=dot_radius))

        group_dots = Group(*dots)

        self.add(axes, axis_labels, group_dots)
        return


class ExpectedValue2(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"y"),
                    MathTex(r"y_1"),
                    MathTex(r"y_2"),
                    MathTex(r"y_3"),
                    MathTex(r"\cdots"),
                    MathTex(r"y_n"),
                ],
                [
                    MathTex(r"Probability"),
                    MathTex(r"p_1"),
                    MathTex(r"p_2"),
                    MathTex(r"p_3"),
                    MathTex(r"\cdots"),
                    MathTex(r"p_n"),
                ],
            ],
            include_outer_lines=True,
        )
        self.add(table)


class SumExpectedValue2(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(""),
                    MathTex(r"x_1"),
                    MathTex(r"x_2"),
                    MathTex(r"x_3"),
                    MathTex("Sum"),
                ],
                [
                    MathTex(r"y_1"),
                    MathTex(r"p_{11}"),
                    MathTex(r"p_{21}"),
                    MathTex(r"p_{31}"),
                    MathTex(r"v_1"),
                ],
                [
                    MathTex(r"y_2"),
                    MathTex(r"p_{12}"),
                    MathTex(r"p_{22}"),
                    MathTex(r"p_{32}"),
                    MathTex(r"v_2"),
                ],
                [
                    MathTex(r"Sum"),
                    MathTex(r"u_1"),
                    MathTex(r"u_2"),
                    MathTex(r"u_3"),
                    MathTex(r"1"),
                ],
            ],
            include_outer_lines=True,
        )
        self.add(table)
        return


class SumExpectedValue3(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X"),
                    MathTex(r"x_1"),
                    MathTex(r"x_2"),
                    MathTex(r"x_3"),
                    MathTex("Sum"),
                ],
                [
                    MathTex(r"Probability"),
                    MathTex(r"u_1"),
                    MathTex(r"u_2"),
                    MathTex(r"u_3"),
                    MathTex(r"1"),
                ],
            ],
            include_outer_lines=True,
        )
        self.add(table)
        return


class SumExpectedValue4(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"Y"),
                    MathTex(r"y_1"),
                    MathTex(r"y_2"),
                    MathTex("Sum"),
                ],
                [
                    MathTex(r"Probability"),
                    MathTex(r"v_1"),
                    MathTex(r"v_2"),
                    MathTex(r"1"),
                ],
            ],
            include_outer_lines=True,
        )
        self.add(table)
        return


class ProbabilityDistributionExample0(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X"),
                    MathTex(r"0"),
                    MathTex(r"1"),
                    MathTex(r"2"),
                    MathTex(r"3"),
                ],
                [
                    MathTex(r"Probability"),
                    MathTex(r"\frac{1}{27}"),
                    MathTex(r"\frac{6}{27}"),
                    MathTex(r"\frac{12}{27}"),
                    MathTex(r"\frac{8}{27}"),
                ],
            ],
            include_outer_lines=True,
        )
        self.add(table)
        return


class ProbabilityDistributionExample1(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X"),
                    MathTex(r"0"),
                    MathTex(r"1"),
                    MathTex(r"2"),
                    MathTex(r"3"),
                ],
                [
                    MathTex(r"Probability"),
                    MathTex(r"{}_3C_0(\frac{1}{3})^3"),
                    MathTex(r"{}_3C_1(\frac{2}{3})(\frac{1}{3})^2"),
                    MathTex(r"{}_3C_2(\frac{2}{3})^2(\frac{1}{3})^1"),
                    MathTex(r"{}_3C_3(\frac{2}{3})^3"),
                ],
            ],
            include_outer_lines=True,
        ).scale(0.7)
        self.add(table)
        return


class ProbabilityDistributionExample2(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X"),
                    MathTex(r"0"),
                    MathTex(r"1"),
                    MathTex(r"\cdots"),
                    MathTex(r"n"),
                ],
                [
                    MathTex(r"Probability"),
                    MathTex(r"{}_nC_0(1-p)^n"),
                    MathTex(r"{}_nC_1(p)^1(1-p)^{n-1}"),
                    MathTex(r"\cdots"),
                    MathTex(r"{}_nC_n(p)^n"),
                ],
            ],
            include_outer_lines=True,
        ).scale(0.7)
        self.add(table)
        return


class ProbabilityDistributionExample3(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X"),
                    MathTex(r"0"),
                    MathTex(r"1"),
                    MathTex(r"2"),
                    MathTex(r"3"),
                ],
                [
                    MathTex(r"Probability"),
                    MathTex(r"{}_3C_0(1-p)^3"),
                    MathTex(r"{}_3C_1(p)^1(1-p)^2"),
                    MathTex(r"{}_3C_2(p)^2(1-p)^1"),
                    MathTex(r"{}_3C_3(p)^3"),
                ],
            ],
            include_outer_lines=True,
        ).scale(0.7)
        self.add(table)
        return


class ProbabilityDistributionExample4(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X_i"),
                    MathTex(r"0"),
                    MathTex(r"1"),
                ],
                [
                    MathTex(r"p"),
                    MathTex(r"1-p"),
                    MathTex(r"p"),
                ],
            ],
            include_outer_lines=True,
        ).scale(0.7)
        self.add(table)
        return


class ProbabilityDistributionExample5(Scene):
    def construct(self):
        # binormial distribution data
        value_p = 2.0 / 3
        value_1_minus_p = 1.0 - value_p
        value_n = 100
        sample_num = value_n + 1

        samples = []
        sample_names = []
        max_sample_value = 0.0
        for index in range(sample_num):
            p_count = index
            one_minus_p_count = value_n - p_count
            combination_value = math.factorial(value_n) / (
                math.factorial(one_minus_p_count) * math.factorial(p_count)
            )
            # calculate value
            sample = (
                combination_value
                * (value_p**p_count)
                * (value_1_minus_p**one_minus_p_count)
            )
            sample = round(sample, 3)

            # get the value name
            sample_name = str(index)

            # update max value
            if max_sample_value < sample:
                max_sample_value = sample

            samples.append(sample)
            sample_names.append(sample_name)

        # calculate y_step
        y_step = max_sample_value / 10.0
        y_step = round(y_step, 2)

        chart = BarChart(
            values=samples,
            bar_names=sample_names,
            y_range=[0, max_sample_value + y_step, y_step],
            y_length=6,
            x_length=12,
            x_axis_config={"font_size": 10},
            y_axis_config={"font_size": 20},
            bar_width=1.0,
        )
        # bar_labels = chart.get_bar_labels(font_size=48)
        self.add(chart)
        return


class ProbabilityDistributionExample6(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 99, 10],
            y_range=[0, 0.09, 0.01],
            tips=False,
            axis_config={"include_numbers": True},
        )

        def function(x):
            # binormial distribution data
            value_p = 2.0 / 3
            value_1_minus_p = 1.0 - value_p
            value_n = 100
            one_minus_p_count = value_n - x

            combination_value = math.factorial(value_n) / (
                math.factorial(one_minus_p_count) * math.factorial(x)
            )
            # calculate value
            sample = (
                combination_value
                * (value_p**x)
                * (value_1_minus_p**one_minus_p_count)
            )
            return sample

        graph = ax.plot(function, x_range=[0, 99], use_smoothing=False)
        self.add(ax, graph)


class InfiniteWorld(Scene):
    def construct(self):
        boundary = Rectangle(width=1.0, height=4.0)
        boundary_desc = (
            Tex(r"Impenetrable Wall").scale(0.8).next_to(boundary, direction=DOWN)
        )
        boundary_group = Group(boundary, boundary_desc)

        finite_world = Rectangle(width=4.0, height=2.0).next_to(
            boundary, direction=LEFT
        )
        desc_pos = finite_world.get_center()
        finite_world_desc = Tex("Finite World").scale(0.8).move_to(desc_pos)
        finite_world_group = Group(finite_world, finite_world_desc)

        infinite_world = Rectangle(width=4.0, height=2.0).next_to(
            boundary, direction=RIGHT
        )
        desc_pos = infinite_world.get_center()
        infinite_world_desc = Tex("Infinite World").scale(0.8).move_to(desc_pos)
        infinite_world_group = Group(infinite_world, infinite_world_desc)

        lim_magic_start = finite_world.get_top()
        lim_magic_end = infinite_world.get_top()
        lim_magic = CurvedArrow(lim_magic_start, lim_magic_end, radius=-3.0)
        lim_magic_desc = Tex(r"$\lim_{x\to\infty}$ Magic!").next_to(
            lim_magic, direction=UP
        )

        lim_magic_group = Group(lim_magic, lim_magic_desc)

        self.add(
            boundary_group, finite_world_group, infinite_world_group, lim_magic_group
        )


class LimitExample0(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"x"),
                    MathTex(r"2"),
                    MathTex(r"4"),
                    MathTex(r"8"),
                    MathTex(r"16"),
                    MathTex(r"\cdots"),
                ],
                [
                    MathTex(r"a_{x}"),
                    MathTex(r"0.5"),
                    MathTex(r"0.75"),
                    MathTex(r"0.875"),
                    MathTex(r"0.9375"),
                    MathTex(r"\cdots"),
                ],
            ],
            include_outer_lines=True,
        )
        self.add(table)


class LimitExample1(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 23, 2], y_range=[-0.2, 1.1, 0.1])

        def function(x):
            return 1.0 - (1.0 / x)

        graph = axes.plot(function, x_range=[0.8, 22])

        # get horizontal line
        line_end = axes.c2p(23, 1.0)
        line = axes.get_horizontal_line(line_end)
        line_desc = MathTex(r"y=1").scale(0.8).move_to(line_end + RIGHT * 0.5)
        line_group = Group(line, line_desc)

        self.add(axes, graph, line_group)


class NapierNumber(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"n"),
                    MathTex(r"10"),
                    MathTex(r"100"),
                    MathTex(r"1000"),
                    MathTex(r"10000"),
                    MathTex(r"100000"),
                    MathTex(r"\cdots"),
                ],
                [
                    MathTex(r"b_n"),
                    MathTex(r"2.59374\cdots"),
                    MathTex(r"2.70481\cdots"),
                    MathTex(r"2.71692\cdots"),
                    MathTex(r"2.71814\cdots"),
                    MathTex(r"2.71826\cdots"),
                    MathTex(r"\cdots"),
                ],
            ],
            include_outer_lines=True,
        ).scale(0.6)
        self.add(table)

        return


class IntegrationExample0(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 1.1, 0.1], y_range=[0, 1.1, 0.1], x_length=6, y_length=6
        )

        def function(x):
            return -(x**2) + 1

        graph = axes.plot(function, x_range=[0, 1])

        # triangle
        fill_opacity = 0.4

        tri0_vertices = [axes.c2p(0, 1), axes.c2p(0, 0), axes.c2p(1, 0)]
        tri0 = Polygon(
            *tri0_vertices, color=PURPLE, fill_color=PURPLE, fill_opacity=fill_opacity
        )

        tri1_vertices = [axes.c2p(0, 1), axes.c2p(1.0 / 2, 3.0 / 4), axes.c2p(1, 0)]
        tri1 = Polygon(
            *tri1_vertices, color=YELLOW, fill_color=YELLOW, fill_opacity=fill_opacity
        )

        tri2_vertices = [
            axes.c2p(0, 1),
            axes.c2p(1.0 / 4, 15.0 / 16),
            axes.c2p(1.0 / 2, 3.0 / 4),
        ]
        tri2 = Polygon(
            *tri2_vertices, color=RED, fill_color=RED, fill_opacity=fill_opacity
        )

        tri3_vertices = [
            axes.c2p(1.0 / 2, 3.0 / 4),
            axes.c2p(3.0 / 4, 7.0 / 16),
            axes.c2p(1, 0),
        ]
        tri3 = Polygon(
            *tri3_vertices, color=RED, fill_color=RED, fill_opacity=fill_opacity
        )

        tri_group = Group(tri0, tri1, tri2, tri3)

        self.add(axes, graph, tri_group)
        return


class IntegrationExample1(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 6],
            tips=False,
        )

        # get the label
        labels = ax.get_axis_labels()

        label_a_pos = ax.c2p(1, 0)
        label_a = MathTex(r"a").move_to(label_a_pos + DOWN * 0.5)
        label_b_pos = ax.c2p(3, 0)
        label_b = MathTex(r"b").move_to(label_b_pos + DOWN * 0.5)

        labels_group = Group(labels, label_a, label_b)

        # plot the function
        def function(x):
            return 4 * x - x**2

        graph = ax.plot(function, x_range=[0, 4], color=BLUE_C)

        line_1 = ax.get_vertical_line(ax.i2gp(1, graph), color=YELLOW)
        line_2 = ax.get_vertical_line(ax.i2gp(3, graph), color=YELLOW)
        line_group = Group(line_1, line_2)

        # plot riemann rectangles
        area = ax.get_riemann_rectangles(
            graph, x_range=[1, 3], dx=0.05, color=RED_C, fill_opacity=0.4
        )

        self.add(ax, labels_group, line_group, graph, area)

        return


class IntegrationExample2(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 6],
            tips=False,
        )

        # get the label
        labels = ax.get_axis_labels()

        label_a_pos = ax.c2p(1, 0)
        label_a = MathTex(r"a").move_to(label_a_pos + DOWN * 0.5)
        label_b_pos = ax.c2p(3, 0)
        label_b = MathTex(r"b").move_to(label_b_pos + DOWN * 0.5)

        labels_group = Group(labels, label_a, label_b)

        # plot the function
        def function(x):
            return 4 * x - x**2

        graph = ax.plot(function, x_range=[0, 4], color=BLUE_C)

        line_1 = ax.get_vertical_line(ax.i2gp(1, graph), color=YELLOW)
        line_2 = ax.get_vertical_line(ax.i2gp(3, graph), color=YELLOW)
        line_group = Group(line_1, line_2)

        # plot riemann rectangles
        area = ax.get_area(graph, x_range=[1, 3], color=RED_C, fill_opacity=0.4)

        self.add(ax, labels_group, line_group, graph, area)

        return


class ContinuousRandomVariableExample0(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 140, 20],
            y_range=[0, 0.5, 0.25],
            x_axis_config={"numbers_to_include": [0, 30, 60, 120]},
        )

        axis_labels = axes.get_axis_labels()

        def function(x):
            return 0.25

        graph = axes.plot(function, x_range=[0, 120])
        line = axes.get_vertical_line(
            axes.input_to_graph_point(120, graph), color=YELLOW
        )

        area = axes.get_area(graph, x_range=[30, 60], color=PURPLE_B)

        self.add(axes, axis_labels, graph, line, area)
        return


class ContinuousRandomVariableExample1(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 6],
            tips=False,
        )

        # get the label
        labels = ax.get_axis_labels()

        label_alpha_pos = ax.c2p(1, 0)
        label_alpha = MathTex(r"\alpha").move_to(label_alpha_pos + DOWN * 0.5)
        label_beta_pos = ax.c2p(3, 0)
        label_beta = MathTex(r"\beta").move_to(label_beta_pos + DOWN * 0.5)

        label_a_pos = ax.c2p(1.8, 0)
        label_a = MathTex(r"a").move_to(label_a_pos + DOWN * 0.5)

        label_b_pos = ax.c2p(2.2, 0)
        label_b = MathTex(r"b").move_to(label_b_pos + DOWN * 0.5)

        labels_group = Group(labels, label_alpha, label_beta, label_a, label_b)

        # plot the function
        def function(x):
            return 4 * x - x**2

        graph = ax.plot(function, x_range=[1, 3], color=BLUE_C)

        line_1 = ax.get_vertical_line(ax.i2gp(1, graph), color=YELLOW)
        line_2 = ax.get_vertical_line(ax.i2gp(3, graph), color=YELLOW)
        line_group = Group(line_1, line_2)

        # plot riemann rectangles
        area = ax.get_area(graph, x_range=[1.8, 2.2], color=RED_C, fill_opacity=0.4)

        self.add(ax, labels_group, line_group, graph, area)

        return


class ContinuousRandomVariableExample2(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 6],
            tips=False,
        )

        # get the label
        labels = ax.get_axis_labels()

        label_alpha_pos = ax.c2p(1, 0)
        label_alpha = MathTex(r"\alpha").move_to(label_alpha_pos + DOWN * 0.5)
        label_beta_pos = ax.c2p(3, 0)
        label_beta = MathTex(r"\beta").move_to(label_beta_pos + DOWN * 0.5)

        label_a_pos = ax.c2p(1.8, 0)
        label_a = MathTex(r"a").move_to(label_a_pos + DOWN * 0.5)

        label_b_pos = ax.c2p(2.2, 0)
        label_b = MathTex(r"b").move_to(label_b_pos + DOWN * 0.5)

        labels_group = Group(labels, label_alpha, label_beta, label_a, label_b)

        # plot the function
        def function(x):
            return 4 * x - x**2

        graph = ax.plot(function, x_range=[1, 3], color=BLUE_C)

        line_1 = ax.get_vertical_line(ax.i2gp(1, graph), color=YELLOW)
        line_2 = ax.get_vertical_line(ax.i2gp(3, graph), color=YELLOW)
        line_group = Group(line_1, line_2)

        # plot riemann rectangles
        area = ax.get_riemann_rectangles(
            graph, x_range=[1.4, 2.2], dx=0.4, color=RED_C, fill_opacity=0.4
        )

        self.add(ax, labels_group, line_group, graph, area)

        return


class ContinuousRandomVariableExample3(Scene):
    def construct(self):
        table = MobjectTable(
            [
                [
                    MathTex(r"X'"),
                    MathTex(r"x_1"),
                    MathTex(r"x_2"),
                    MathTex(r"x_3"),
                    MathTex(r"\cdots"),
                    MathTex(r"x_n"),
                ],
                [
                    MathTex(r"Probability"),
                    MathTex(r"p_1"),
                    MathTex(r"p_2"),
                    MathTex(r"p_3"),
                    MathTex(r"\cdots"),
                    MathTex(r"p_n"),
                ],
            ],
            include_outer_lines=True,
        )

        self.add(table)
        return


class NormalDistribution(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[0, 0.45, 0.1],
            x_axis_config={"numbers_to_include": [-3, -2, -1, 0, 1, 2, 3]},
            y_axis_config={"numbers_to_include": [0, 0.1, 0.2, 0.3, 0.4]},
        )

        def function(x):
            return 1.0 / math.sqrt(2 * math.pi) * math.exp(-(x**2) / 2.0)

        graph = axes.plot(function, x_range=[-3.5, 3.5])
        graph_label = axes.get_graph_label(
            graph, MathTex(r"y=\frac{1}{\sqrt{2\pi}}e^{-\frac{x^2}{2}}")
        ).shift(UP * 2)

        self.add(axes, graph, graph_label)
        return


class NormalDistributionExample0(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[0, 0.45, 0.1],
            x_axis_config={"numbers_to_include": [-3, -2, -1, 0, 1, 2, 3]},
            y_axis_config={"numbers_to_include": [0, 0.1, 0.2, 0.3, 0.4]},
        )

        def function(x):
            return 1.0 / math.sqrt(2 * math.pi) * math.exp(-(x**2) / 2.0)

        graph = axes.plot(function, x_range=[-3.5, 3.5])
        graph_label = axes.get_graph_label(
            graph, MathTex(r"y=\frac{1}{\sqrt{2\pi}}e^{-\frac{x^2}{2}}")
        ).shift(UP * 2)

        area = axes.get_area(graph, x_range=[0, 1.5], color=RED_C, fill_opacity=0.4)

        label_u_pos = axes.c2p(1.5, 0)
        label_u = MathTex(r"u", color=YELLOW).move_to(label_u_pos + DOWN * 0.5)

        p_u_start_pt = axes.c2p(1, 0.15)
        p_u_end_pt = axes.c2p(2, 0.3)
        p_u = Line(p_u_start_pt, p_u_end_pt, color=YELLOW)
        P_u_label = MathTex(r"p(u)", color=YELLOW).move_to(p_u_end_pt + UP * 0.5)
        p_u_group = Group(p_u, P_u_label)

        self.add(axes, graph, graph_label, area, label_u, p_u_group)
        return


class NormalDistributionExample1(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3.5, 3.5, 1.96],
            y_range=[0, 0.45, 0.1],
            x_axis_config={"numbers_to_include": [-1.96, 1.96]},
            y_axis_config={"numbers_to_include": [0, 0.1, 0.2, 0.3, 0.4]},
        )

        def function(x):
            return 1.0 / math.sqrt(2 * math.pi) * math.exp(-(x**2) / 2.0)

        graph = axes.plot(function, x_range=[-3.5, 3.5])
        graph_label = axes.get_graph_label(
            graph, MathTex(r"y=\frac{1}{\sqrt{2\pi}}e^{-\frac{x^2}{2}}")
        ).shift(UP * 2)

        area = axes.get_area(
            graph, x_range=[-1.96, 1.96], color=RED_C, fill_opacity=0.4
        )

        p_u_start_pt = axes.c2p(1, 0.15)
        p_u_end_pt = axes.c2p(2, 0.3)
        p_u = Line(p_u_start_pt, p_u_end_pt, color=YELLOW)
        P_u_label = MathTex(r"95\%", color=YELLOW).move_to(p_u_end_pt + UP * 0.5)
        p_u_group = Group(p_u, P_u_label)

        self.add(axes, graph, graph_label, area, p_u_group)
        return
