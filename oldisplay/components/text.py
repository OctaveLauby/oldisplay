import pygame as pg
from olutils import read_params

from oldisplay.collections import Color
from oldisplay.utils import split_params
from .component import ActiveComponent, Component, LocatedObject

_font_cache = {
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
        return _font_cache[fontname]
    except KeyError:
        pass

    s1, s2 = 100, 200  # I tried a few and those give the best precision
    args = ("Text", True, (0, 0, 0))
    h1 = pg.font.SysFont(fontname, size=s1).render(*args).get_size()[1]
    h2 = pg.font.SysFont(fontname, size=s2).render(*args).get_size()[1]
    factor = (h2 - h1) / (s2 - s1)
    offset = (h1 * s2 - s1 * h2) / (s2 - s1)

    params = (factor, offset)
    _font_cache[fontname] = params
    return params


def font_size(fontname, height):
    """Return font size to use in order to get text with height in pixels"""
    factor, offset = font_sizing(fontname)
    return int(round((height - offset) / factor))


class Text(LocatedObject, Component):
    """Basic text"""

    dft_look_params = {
        'height': 12,
        'font': None,  # default system font
        'color': "black",
        'bold': False,
        'italic': False,
        'underline': False,
    }

    def __init__(self, string, ref_pos, **kwargs):
        """Initiate params of text to display

        About:
            Requires call to init method for component to be usable

        Args:
            string (str)            : text displayed
            ref_pos (2-int-tuple)   : position of text
            **kwargs                : location and aspect parameters

                # Location parameters
                h_align (str)           : where position is regarding text (x-axis)
                    left, center or right
                v_align (str)           : where position is regarding text (y-axis)
                    bottom, center or top

                # Aspect parameters
                height (int)            : height of text in pixels
                font (str)              : name of font
                color (color descr)     : color of display
                bold (bool)             : use bold writing
                italic  (bool)          : use italic writing
                underline (bool)        : underline writing
        """
        self.params = read_params(kwargs, self.cls.dft_look_params, safe=False)
        kwargs.pop('height', None)
        super().__init__(ref_pos=ref_pos, size=None, **kwargs)
        self.ref_pos

        self._string = string
        self._font = None
        self._surf = None


    def init(self):
        """Initiate font and surface cache, requires pygame.init()"""

        # Initiate font
        font = pg.font.SysFont(
            name=self.params.font,
            size=font_size(self.params.font, self.params.height),
            bold=self.params.bold,
            italic=self.params.italic,
        )
        if self.params.underline:
            font.set_underline(True)

        # Initiate text cache
        surface = font.render(
            self.string, True, Color.get(self.params.color)
        )

        # Update
        self._font, self._surf = font, surface
        self.size = self.surface.get_size()

    @property
    def string(self):
        """Text displayed (str)"""
        return self._string

    @property
    def font(self):
        """Font of text (pygame.font.Font)"""
        return self._font

    @property
    def surface(self):
        """Surface of text (pygame.Surface)"""
        return self._surf

    def update(self, surface, events=None):
        """Basic display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        surface.blit(self.surface, self.position)


class ActiveText(ActiveComponent):
    """Text with look change when hovered or clicked"""

    def __init__(self, string, ref_pos, **kwargs):
        """Initiate params of text to display

        About:
            Requires call to init method for component to be usable

        Args:
            string (str)            : text displayed
            ref_pos (2-int-tuple)   : position of text
            **kwargs                : location and look parameters

                # Location parameters
                h_align (str)           : where position is regarding text (x-axis)
                    left, center or right
                v_align (str)           : where position is regarding text (y-axis)
                    bottom, center or top

                # Look parameters
                size (int)              : size of font
                font (str)              : name of font
                color (color descr)     : color of display
                bold (bool)             : use bold writing
                italic  (bool)          : use italic writing
                underline (bool)        : underline writing
        """
        super().__init__(**kwargs)

        # Aspect params
        loc_params = read_params(
            kwargs, LocatedObject.dft_loc_params, safe=False
        )
        normal, hovered, clicked = split_params(
            kwargs, 3, dft_params=Text.dft_look_params, safe=False
        )

        # Aspect cache
        self._n_txt = Text(
                string, ref_pos, **loc_params, **normal
        )
        self._h_txt = (
            None if hovered is None
            else Text(
                string, ref_pos, **loc_params, **hovered
            )
        )
        self._c_txt = (
            None if clicked is None
            else Text(
                string, ref_pos, **loc_params, **clicked
            )
        )

    def init(self):
        """Initiate font and surface cache, requires pygame.init()"""
        self._n_txt.init()
        if self._h_txt:
            self._h_txt.init()
        if self._c_txt:
            self._c_txt.init()

    @property
    def normal_txt(self):
        """Normal text"""
        return self._n_txt

    @property
    def hover_txt(self):
        """Hovered text"""
        if self._h_txt is None:
            return self.normal_txt
        return self._h_txt

    @property
    def click_txt(self):
        """Clicked text"""
        if self._c_txt is None:
            return self.hover_txt
        return self._c_txt

    def display_normal(self, surface):
        """Basic display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        self.normal_txt.update(surface)

    def display_hovered(self, surface):
        """Hovered display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        self.hover_txt.update(surface)

    def display_clicked(self, surface):
        """Clicked display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        self.click_txt.update(surface)


    def is_within(self, position):
        """Return whether position is within hit box"""
        x, y = position
        sx, sy = self.normal_txt.position
        dx, dy = self.normal_txt.surface.get_size()
        return (sx < x < sx+dx) and (sy < y < sy+dy)
