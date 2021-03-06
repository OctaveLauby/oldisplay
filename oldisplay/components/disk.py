"""Objects to draw disks and circles"""
import numpy as np
import pygame as pg

from oldisplay import align
from .component import LocatedObject
from .shape import Shape2D, ActiveShape


class Disk(LocatedObject, Shape2D):
    """Disk shape"""

    dft_location = {
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
            align (str)             : alignment with ref_pos
                'center', 'top-left', 'bot-right', 'top-center', ...
            color (color)           : inside color
            outline (color)         : outline color
            width (int)             : width of outline
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

    def display(self, surface, **params):
        """Display disk regarding given look parameters"""
        w_outline = bool(params['outline'] and params['width'])
        if params['color']:
            # When drawn with border, reduce radius so it does not poke out
            pg.draw.circle(
                surface, params['color'], self.center, self.radius - w_outline
            )
        if w_outline:
            pg.draw.circle(
                surface, params['outline'], self.center, self.radius, params['width']
            )


class ActiveDisk(Disk, ActiveShape):
    """Disk w. potential outline & look change when hovered or clicked"""

    def is_within(self, position):
        """Return whether position is within disk"""
        position = np.array(position)
        return (
            np.linalg.norm(position-self.center)
            <= self.radius
        )
