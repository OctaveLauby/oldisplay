import numpy as np
import pygame as pg

from oldisplay import align
from .component import LocatedObject
from .shape import Shape2D, ActiveShape


class Disk(LocatedObject, Shape2D):

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
                @see LocatedObject
                @see Shape2D
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

    def display(self, surface, color, outline, width):
        """Display disk regarding given aspect"""
        w_outline = bool(outline and width)
        if color:
            # When drawn with border, reduce radius so it does not poke out
            pg.draw.circle(surface, color, self.center, self.radius - w_outline)
        if w_outline:
            pg.draw.circle(surface, outline, self.center, self.radius, width)


class ActiveDisk(Disk, ActiveShape):
    """Disk w. potential outline & look change when hovered or clicked"""

    def is_within(self, position):
        """Return whether position is within disk"""
        position = np.array(position)
        return (
            np.linalg.norm(position-self.center)
            <= self.radius
        )
