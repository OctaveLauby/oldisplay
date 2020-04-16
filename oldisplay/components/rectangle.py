import pygame as pg

from .shape import SurfaceShape


class Rectangle(SurfaceShape):

    @classmethod
    def build_cache(cls, position, size):
        """Return shape surface and outline of rectangle"""
        return pg.Rect(position, size)

    def __init__(self, position, size, **kwargs):
        """Initiate instance of rectangle

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
        super().__init__(args=(position, size), look=kwargs)

    def display_(self, surface, color, outline, width):
        """Display rectangle regarding given aspect"""
        if color:
            pg.draw.rect(surface, color, self.cache)
        if outline and width:
            pg.draw.rect(surface, outline, self.cache, width)

    def is_within(self, position):
        """Return whether position is within rectangle"""
        return self.cache.collidepoint(position)
