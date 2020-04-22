import numpy as np
import pygame as pg

from .component import LEFT, RIGHT, TOP, BOTTOM, CENTER
from .shape import ActiveLocatedShape


class ActiveDisk(ActiveLocatedShape):
    """Disk w. potential outline & look change when hovered or clicked"""

    dft_loc_params = {
        'h_align': CENTER,
        'v_align': CENTER,
    }

    def __init__(self, ref_pos, radius, **kwargs):
        """Initialize instance of disk

        Args:
            ref_pos (2-int-tuple)   : reference position of disk
                default is center
            radius (int)            : radius of disk in pixels
            **kwargs                : aspect & position description
                @see ActiveShape
                @see LocatedComponent
        """
        super().__init__(ref_pos, (radius*2, radius*2), **kwargs)
        self._radius = radius
        self._pos_func = self.compute_center

    @property
    def center(self):
        """Center of disk"""
        return self.position

    @property
    def radius(self):
        """Radius in pixels"""
        return self._radius

    def compute_center(self):
        """Compute center position on surface"""
        x, y = self.ref_pos
        if self.h_align == LEFT:
            x += self.radius
        elif self.h_align == RIGHT:
            x -= self.radius
        if self.v_align == TOP:
            y += self.radius
        elif self.v_align == BOTTOM:
            y -= self.radius
        return x, y

    def display_(self, surface, color, outline, width):
        """Display disk regarding given aspect"""
        if color:
            pg.draw.circle(surface, color, self.center, self.radius)
        if outline and width:
            pg.draw.circle(surface, outline, self.center, self.radius, width)

    def is_within(self, position):
        """Return whether position is within disk"""
        position = np.array(position)
        return (
            np.linalg.norm(position-self.center)
            <= self.radius
        )
