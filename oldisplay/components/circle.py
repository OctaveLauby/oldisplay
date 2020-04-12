import numpy as np
import pygame as pg

from .shape import SurfaceShape


class Circle(SurfaceShape):

    @classmethod
    def build_cache(cls, center, radius):
        """Return shape surface and outline of rectangle"""
        return (np.array(center), int(radius))

    def __init__(self, center, radius, **kwargs):
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
        super().__init__(args=(center, radius), look=kwargs)

    def display_(self, surface, color, outline, width):
        """Display circle regarding given aspect"""
        if color:
            pg.draw.circle(surface, color, *self.cache)
        if outline and width:
            pg.draw.circle(surface, outline, *self.cache, width)

    def is_within(self, position):
        """Return whether position is within circle"""
        position = np.array(position)
        return (
            np.linalg.norm(position-self.cache[0])
            <= self.cache[1]
        )
