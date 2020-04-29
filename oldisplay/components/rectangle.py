import pygame as pg

from .component import LocatedObject
from .line import LineSet
from .shape import Shape2D, ActiveShape



class Rectangle(LocatedObject, Shape2D):

    def __init__(self, ref_pos, size, **kwargs):
        """Initialize instance of rectangle

        Args:
            ref_pos (2-int-tuple)   : reference position
                default is top-left
            size (2-int-tuple)      : size of rectangle in pixels
            **kwargs                : aspect & position description
                @see ActiveShape
                @see LocatedComponent
        """
        super().__init__(ref_pos, size, **kwargs)
        self.cache = pg.Rect(self.position, size)

    def display(self, surface, color, outline, width):
        """Display rectangle regarding given aspect"""
        if color:
            pg.draw.rect(surface, color, self.cache)
        if outline and width:
            # Build my own outline as pg.draw.rect draw awkward outline
            # # (that goes outside rectangle and ignore corners)
            x, y = self.position
            dx, dy = self.cache.size
            dx -= 1
            dy -= 1
            width = min([width, dx, dy])
            delta_p = (width-1) // 2
            delta_m = (width-1) // 2 + ((width+1) % 2)
            x_lft, x_rgt = x+delta_p, x+dx-delta_m
            y_top, y_bot = y+delta_p, y+dy-delta_m
            line = LineSet([
                [(x, y_top), (x+dx, y_top)],
                [(x, y_bot), (x+dx, y_bot)],
                [(x_lft, y), (x_lft, y+dx)],
                [(x_rgt, y), (x_rgt, y+dx)],
            ], color=outline, width=width)
            line.update(surface)


class ActiveRectangle(Rectangle, ActiveShape):
    """Rectangle w. potential outline & look change when hovered or clicked"""

    def is_within(self, position):
        """Return whether position is within rectangle"""
        return self.cache.collidepoint(position)
