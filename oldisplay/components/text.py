"""Objects to draw text"""
import pygame as pg

from oldisplay.collections import Color
from .component import LocatedObject
from .shape import ActiveShape, Shape2D

_FONT_SIZING_CACHE = {
    # fontname: (height factor, height offset)
}

def font_sizing(fontname):
    """Return factor and offset to compute text size in pixels from front size

    About:
        When loading a font one must precise a size that does not match the
        actual height in pixels the text will have. The difference depends on
        the font.

    Return:
        (2-float-tuple): factor and offset of the given font so that
            height (in pixels) = factor * size (of font) + offset
    """
    try:
        return _FONT_SIZING_CACHE[fontname]
    except KeyError:
        pass

    s1, s2 = 100, 200  # I tried a few and those give the best precision
    args = ("Text", True, (0, 0, 0))
    h1 = pg.font.SysFont(fontname, size=s1).render(*args).get_size()[1]
    h2 = pg.font.SysFont(fontname, size=s2).render(*args).get_size()[1]
    factor = (h2 - h1) / (s2 - s1)
    offset = (h1 * s2 - s1 * h2) / (s2 - s1)

    params = (factor, offset)
    _FONT_SIZING_CACHE[fontname] = params
    return params


def font_size(fontname, height):
    """Return font size to use in order to get text with height in pixels"""
    factor, offset = font_sizing(fontname)
    return int(round((height - offset) / factor))


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

    font_cache = {}
    surf_cache = {}  # TODO: move it to instance

    @classmethod
    def get_font(cls, **params):
        """Font of text (pygame.font.Font)"""
        key = (
            params['font'],
            params['height'],
            params['bold'],
            params['italic'],
            params['underline'],
        )
        try:
            return cls.font_cache[key]
        except KeyError:
            pass

        font = pg.font.SysFont(
            name=params['font'],
            size=font_size(params['font'], params['height']),
            bold=params['bold'],
            italic=params['italic'],
        )
        if params['underline']:
            font.set_underline(True)

        cls.font_cache[key] = font
        return font

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
        font = self.cls.get_font(**params)
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
