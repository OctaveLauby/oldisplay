"""Objects to draw lines"""
import pygame as pg

from .shape import Shape1D


# --------------------------------------------------------------------------- #
# Functions

def draw_segment(surface, p1, p2, color, width):
    """Draw segment on surface

    About:
        Line width extend centered on base line, when width is even the extra
        pixel goes on the right/bottom of the line (x/y positively)
    """
    pg.draw.line(surface, color, p1, p2, width)


def draw_line(surface, points, color, width, closed=False):
    """Draw line on surface

    About:
        Line width extend centered on base line, when width is even the extra
        pixel goes on the right/bottom of the line (x/y positively)
    """
    pg.draw.lines(surface, color, closed, points, width)


def draw_lines(surface, lines, color, width):
    """Draw a set of lines on surface

    About:
        Line width extend centered on base line, when width is even the extra
        pixel goes on the right/bottom of the line (x/y positively)
    """
    for points in lines:
        draw_line(surface, points, color, width)


# --------------------------------------------------------------------------- #
# Classes

class Segment(Shape1D):
    """Simple segment"""

    def __init__(self, p1, p2, **kwargs):
        """Initialize a segment

        Args:
            p1 (2-int-tuple)    : starting position
            p2 (2-int-tuple)    : ending position
            color (color)   : color of lines
            width (int)     : width of lines
        """
        super().__init__(**kwargs)
        self.p1 = p1
        self.p2 = p2

    def display(self, surface, **params):
        """Display segment"""
        draw_segment(surface, params['color'], self.p1, self.p2, params['width'])


class Line(Shape1D):
    """Continuous line"""

    def __init__(self, points, **kwargs):
        """Initialize a line

        Args:
            line (list) : list of points
            color (color)   : color of lines
            width (int)     : width of lines
        """
        super().__init__(**kwargs)
        self.points = points

    def display(self, surface, **params):
        """Display line"""
        draw_line(surface, self.points, params['color'], params['width'])


class LineSet(Shape1D):
    """Set of lines"""

    def __init__(self, lines, **kwargs):
        """Initialize a set of line

        Args:
            lines (list): list of lines (1 line is list[2-int-tuple])
            color (color)   : color of lines
            width (int)     : width of lines
        """
        super().__init__(**kwargs)
        self.lines = lines

    def display(self, surface, **params):
        """Display line"""
        draw_lines(surface, self.lines, params['color'], params['width'])
