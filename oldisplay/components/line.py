import pygame as pg

from .shape import LinearShape


# --------------------------------------------------------------------------- #
# Functions

def draw_segment(surface, p1, p2, color, width):
    """Draw segment on surface"""
    pg.draw.line(surface, color, p1, p2, width)


def draw_line(surface, points, color, width):
    """Draw line on surface"""
    for p1, p2 in zip(points[:-1], points[1:]):
        draw_segment(surface, p1, p2, color, width)


def draw_lines(surface, lines, color, width):
    """Draw a set of lines on surface"""
    for points in lines:
        draw_line(surface, points, color, width)


# --------------------------------------------------------------------------- #
# Classes

class Segment(LinearShape):

    def __init__(self, p1, p2, **kwargs):
        """Initialize a segment"""
        super().__init__(**kwargs)
        self.p1 = p1
        self.p2 = p2

    def update(self, surface, events=None):
        """Display segment"""
        draw_segment(surface, self.color, self.p1, self.p2, self.width)


class Line(LinearShape):

    def __init__(self, points, **kwargs):
        """Initialize a line"""
        super().__init__(**kwargs)
        self.points = points

    def update(self, surface, events=None):
        """Display line"""
        draw_line(surface, self.points, self.color, self.width)


class LineSet(LinearShape):

    def __init__(self, lines, **kwargs):
        """Initialize a set of line"""
        super().__init__(**kwargs)
        self.lines = lines

    def update(self, surface, events=None):
        """Display line"""
        draw_lines(surface, self.lines, self.color, self.width)
