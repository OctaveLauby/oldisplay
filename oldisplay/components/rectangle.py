import pygame as pg

from .shape import ActiveLocatedShape


class ActiveRectangle(ActiveLocatedShape):
    """Rectangle w. potential outline & look change when hovered or clicked"""

    def __init__(self, position, size, **kwargs):
        """Initialize instance of rectangle

        Args:
            position (2-int-tuple)  : reference position
            size (2-int-tuple)      : size of rectangle
            **kwargs                : aspect description
                @see ActiveShape
                @see LocatedComponent
        """
        super().__init__(position, size, **kwargs)
        self.cache = pg.Rect(self.compute_position(), size)

    def display_(self, surface, color, outline, width):
        """Display rectangle regarding given aspect"""
        if color:
            pg.draw.rect(surface, color, self.cache)
        if outline and width:
            pg.draw.rect(surface, outline, self.cache, width)

    def is_within(self, position):
        """Return whether position is within rectangle"""
        return self.cache.collidepoint(position)
