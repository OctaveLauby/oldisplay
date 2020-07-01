"""Objects to draw text"""
import pygame as pg

from oldisplay.collections import Color, FontManager
from .component import LocatedObject
from .shape import ActiveShape, Shape2D


class Text(LocatedObject, Shape2D):
    """Basic text"""

    dft_look = {
        'height': 12,
        'font': None,  # default system font
        'color': "black",
        'bold': False,
        'italic': False,
        'underline': False,
    }
    par_conv = {'color': Color.get}

    surf_cache = {}  # TODO: move it to instance

    def __init__(self, string, ref_pos, rotate=None, **kwargs):
        """Initiate params of text to display

        About:
            Requires call to init method for component to be usable

        Args:
            string (str)            : text displayed
            ref_pos (2-int-tuple)   : position of text
            rotate (float)          : rotation of text in degrees
            align (str)             : alignment with ref_pos
                'center', 'top-left', 'bot-right', 'top-center', ...

            # Aspect parameters
            height (int)            : height of text in pixels
            font (str)              : name of font
                @see pygame.font.get_fonts()
            color (color descr)     : color of display
            bold (bool)             : use bold writing
            italic  (bool)          : use italic writing
            underline (bool)        : underline writing
        """
        super().__init__(ref_pos=ref_pos, size=None, **kwargs)
        self._string = string
        self._rotate = rotate
        self._surfaces = {}

    def init(self):
        """Initiate font and surface cache, requires pygame.init()"""
        self.size = self.get_surf().get_size()

    @property
    def string(self):
        """Text displayed (str)"""
        return self._string

    @property
    def rotate(self):
        """Return rotation of text in degrees"""
        return self._rotate

    def get_surf(self, params=None):
        """Surface of text (pygame.Surface)"""
        params = self.params if params is None else params
        font = FontManager.get(**params)
        color = Color.get(params['color'])
        key = (font, color)
        try:
            return self._surfaces[key]
        except KeyError:
            pass
        surf = font.render(self.string, True, color)
        if self.rotate:
            surf = pg.transform.rotate(surf, self.rotate)
        self._surfaces[key] = surf
        return surf

    def get_pos(self, params=None):
        """Position of text"""
        params = self.params if params is None else params
        size = self.get_surf(params).get_size()
        return self.cls.position_func(
            self.ref_pos, size, self.h_align, self.v_align
        )

    def display(self, surface, **params):
        """Basic display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        surf = self.get_surf(params=params)
        position = self.get_pos(params=params)
        surface.blit(surf, position)


class ActiveText(Text, ActiveShape):
    """Text with look change when hovered or clicked"""

    def is_within(self, position):
        """Return whether position is within hit box"""
        x, y = position
        sx, sy = self.position
        dx, dy = self.size
        return (sx < x < sx+dx) and (sy < y < sy+dy)
