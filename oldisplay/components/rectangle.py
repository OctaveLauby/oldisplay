import pygame as pg

from .shape import ActiveShape


class ActiveRectangle(ActiveShape):
    """Rectangle w. potential outline & look change when hovered or clicked"""

    def __init__(self, position, size, **kwargs):
        """Initialize instance of rectangle

        Args:
            position (2-int-tuple)  : position of top-right on surface
            size (2-int-tuple)      : size of rectangle
            **kwargs                : aspect description
                color (color desc)      : inside color
                outline (color desc)    : outline color
                width (int)             : width of border
                hovered (dict)          : aspect when mouse hover rect
                clicked (dict)          : aspect when user click on rect
        """
        super().__init__(**kwargs)
        self.cache = pg.Rect(position, size)

    def display_(self, surface, color, outline, width):
        """Display rectangle regarding given aspect"""
        if color:
            pg.draw.rect(surface, color, self.cache)
        if outline and width:
            pg.draw.rect(surface, outline, self.cache, width)

    def is_within(self, position):
        """Return whether position is within rectangle"""
        return self.cache.collidepoint(position)
