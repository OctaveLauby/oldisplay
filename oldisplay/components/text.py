import pygame as pg
from olutils import read_params

from oldisplay.collections import Color
from .component import ActiveComponent, LocatedComponent


class Text(LocatedComponent):
    """Basic text"""

    dft_look_params = {
        'size': 12,
        'font': None,  # default system font
        'color': "black",
        'bold': False,
        'italic': False,
        'underline': False,
    }

    def __init__(self, string, position, **kwargs):
        """Initiate params of text to display

        About:
            Requires call to init method for component to be usable

        Args:
            string (str)            : text displayed
            position (2-int-tuple)  : position of text
            align (str)             : where position is regarding text (x-axis)
                left, center or right
            adjust (str)            : where position is regarding text (y-axis)
                bottom, center or top
            **kwargs                : aspect of text
                size (int)              : size of font
                font (str)              : name of font
                color (color descr)     : color of display
                bold (bool)             : use bold writing
                italic  (bool)          : use italic writing
                underline (bool)        : underline writing
        """
        loc_params, look_params = read_params(
            kwargs, [self.cls.dft_loc_params, self.cls.dft_look_params]
        )
        super().__init__(position, size=None, **loc_params)
        self._string = string

        # Aspect params
        self.params = read_params(look_params, self.cls.dft_look_params)

        # Aspect cache
        self._font = None
        self._surf = None


    def init(self):
        """Initiate font and surface cache, requires pygame.init()"""

        # Initiate font
        font = pg.font.SysFont(
            name=self.params.font,
            size=self.params.size,
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
        surface.blit(self.surface, self.compute_position())


class ActiveText(ActiveComponent):
    """Text with look change when hovered or clicked"""

    def __init__(self, string, position, hovered=None, clicked=None, **kwargs):
        """Initiate params of text to display

        About:
            Requires call to init method for component to be usable

        Args:
            string (str)            : text displayed
            position (2-int-tuple)  : position of text
            h_align (str)           : where position is regarding text (x-axis)
                left, center or right
            v_align (str)           : where position is regarding text (y-axis)
                bottom, center or top
            hovered (dict)          : aspect of text when hovered
            clicked (dict)          : aspect of text when clicked
            **kwargs                : aspect of text
                size (int)              : size of font
                font (str)              : name of font
                color (color descr)     : color of display
                bold (bool)             : use bold writing
                italic  (bool)          : use italic writing
                underline (bool)        : underline writing

        """
        loc_params, look_params = read_params(
            kwargs, [Text.dft_loc_params, Text.dft_look_params]
        )
        super().__init__()

        # Aspect params
        if hovered is not None:
            hovered = read_params(hovered, look_params)
        if clicked and hovered:
            clicked = read_params(clicked, hovered)
        elif clicked:
            clicked = read_params(clicked, look_params)

        # Aspect cache
        self._n_txt = Text(
                string, position, **loc_params, **look_params
        )
        self._h_txt = (
            None if hovered is None
            else Text(
                string, position, **loc_params, **hovered
            )
        )
        self._c_txt = (
            None if clicked is None
            else Text(
                string, position, **loc_params, **clicked
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
        sx, sy = self.normal_txt.compute_position()
        dx, dy = self.normal_txt.surface.get_size()
        return (sx < x < sx+dx) and (sy < y < sy+dy)
