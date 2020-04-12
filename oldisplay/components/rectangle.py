import pygame as pg

from .shape import SurfaceShape


class Rectangle(SurfaceShape):

    @classmethod
    def in_out_shape(cls, position, size):
        """Return shape surface and outline of rectangle"""
        x, y = position
        dx, dy = size
        return pg.Rect(position, size), [
            (x, y), (x+dx, y), (x+dx, y), (x+dx, y+dy), (x, y+dy)
        ]

    def __init__(self, position, size, **kwargs):
        """Initiate instance of rectangle

        Args:
            position (2-int-tuple)  : position of top-right on surface
            size (2-int-tuple)      : size of rectangle
            **kwargs                : aspect description
                color (color description)   : inside color
                outline (color description) : outline color
                width (int)                 : width of border
                hovered (dict)              : aspect when mouse hover rect
                clicked (dict)              : aspect when user click on rect
        """
        super().__init__(args=(position, size), look=kwargs)

    def display_(self, surface, color, outline, width):
        """Display rectangle regarding given aspect"""
        if color:
            pg.draw.rect(surface, color, self.shape)
        if outline and width:
            pg.draw.lines(surface, outline, True, self.outline, width)
