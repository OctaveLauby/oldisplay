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

    def __init__(self, position, radius, **kwargs):
        """Initialize instance of disk

        Args:
            position (2-int-tuple)  : reference position of disk
                default is center
            radius (int)            : radius of disk in pixels
            **kwargs                : aspect & position description
                @see ActiveShape
                @see LocatedComponent
        """
        super().__init__(position, (radius*2, radius*2), **kwargs)
        self._radius = radius

    @property
    def radius(self):
        """Radius in pixels"""
        return self._radius

    def compute_position(self):
        """Compute center position on surface"""
        x, y = self.rpos
        dx, dy = self.size
        key = (x, y, dx, dy)

        try:
            return self._pos_dict[key]
        except KeyError:
            pass

        if self.h_align == LEFT:
            x += self.radius
        elif self.h_align == RIGHT:
            x -= self.radius
        if self.v_align == TOP:
            y += self.radius
        elif self.v_align == BOTTOM:
            y -= self.radius

        self._pos_dict[key] = x, y
        return x, y

    def display_(self, surface, color, outline, width):
        """Display disk regarding given aspect"""
        center = self.compute_position()
        if color:
            pg.draw.circle(surface, color, self.compute_position(), self.radius)
        if outline and width:
            pg.draw.circle(surface, outline, self.compute_position(), self.radius, width)

    def is_within(self, position):
        """Return whether position is within disk"""
        position = np.array(position)
        return (
            np.linalg.norm(position-self.compute_position())
            <= self.radius
        )
