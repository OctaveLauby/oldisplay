import numpy as np
import pygame as pg

from .shape import DynamicShape


class DynamicDisk(DynamicShape):
    """Disk w. potential outline & look change when hovered or clicked"""

    @classmethod
    def build_cache(cls, center, radius):
        """Return shape surface and outline of rectangle"""
        return (np.array(center), int(radius))

    def __init__(self, center, radius, **kwargs):
        """Initiate instance of disk

        Args:
            center (2-int-tuple)    : center of disk
            radius (int)            : radius of disk in pixels
            **kwargs                : aspect description
                color (color description)   : inside color
                outline (color description) : outline color
                width (int)                 : width of border
                hovered (dict)              : aspect when mouse hover rect
                clicked (dict)              : aspect when user click on rect
        """
        super().__init__(args=(center, radius), look=kwargs)

    def display_(self, surface, color, outline, width):
        """Display disk regarding given aspect"""
        if color:
            pg.draw.circle(surface, color, *self.cache)
        if outline and width:
            pg.draw.circle(surface, outline, *self.cache, width)

    def is_within(self, position):
        """Return whether position is within disk"""
        position = np.array(position)
        return (
            np.linalg.norm(position-self.cache[0])
            <= self.cache[1]
        )
