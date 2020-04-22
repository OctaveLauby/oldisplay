import numpy as np
import pygame as pg

from oldisplay import align
from .shape import ActiveLocatedShape


class ActiveDisk(ActiveLocatedShape):
    """Disk w. potential outline & look change when hovered or clicked"""

    dft_loc_params = {
        'h_align': align.CENTER,
        'v_align': align.CENTER,
    }
    position_func = align.compute_center

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

    @property
    def center(self):
        """Center of disk"""
        return self.position

    @property
    def radius(self):
        """Radius in pixels"""
        return self._radius

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
