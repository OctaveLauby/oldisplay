import pygame as pg
from olutils import read_params

from oldisplay.collections import Color
from .component import ActiveComponent, Component

TOP = "top"
BOTTOM = "bottom"
LEFT = "left"
RIGHT = "right"
CENTER = "center"
ADJUSTMENTS = [BOTTOM, CENTER, TOP]
ALIGNMENTS = [LEFT, CENTER, RIGHT]



class Text(Component):
    """Basic text"""

    dft_look = {
        'size': 12,
        'font': None,  # default system font
        'color': "black",
        'bold': False,
        'italic': False,
        'underline': False,
    }

    def __init__(self, string, position, align=LEFT, adjust=BOTTOM, **kwargs):
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
        super().__init__()

        # Position
        self._string = string
        self._position = position
        self._adjust = None
        self._align = None
        self.set_adjust(adjust)
        self.set_align(align)

        # Aspect params
        self.params = read_params(kwargs, self.cls.dft_look)

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

    def compute_position(self):
        """Top-Left position of text (2-int-tuple)"""
        x, y = self._position
        dx, dy = self.surface.get_size()
        if self._align == RIGHT:
            x -= dx
        elif self._align == CENTER:
            x -= dx // 2

        if self._adjust == BOTTOM:
            y -= dy
        elif self._adjust == CENTER:
            y += dy //2
        return x, y

    def set_adjust(self, adjust):
        """Set kind of adjustment ('bottom', 'center' or 'top')"""
        if adjust not in ADJUSTMENTS:
            raise ValueError(
                f"Unknown value for adjustment {adjust}"
                f", must be within {ADJUSTMENTS}"
            )
        self._adjust = adjust

    def set_align(self, align):
        """Set kind of alignment ('left', 'center' or 'right')"""
        if align not in ALIGNMENTS:
            raise ValueError(
                f"Unknown value for alignment {align}"
                f", must be within {ALIGNMENTS}"
            )
        self._align = align

    def update(self, surface, events=None):
        """Basic display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        surface.blit(self.surface, self.compute_position())


class ActiveText(ActiveComponent):
    """Text with look change when hovered or clicked"""

    def __init__(self, string, position, align=LEFT, adjust=BOTTOM,
                 hovered=None, clicked=None, **kwargs):
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
        super().__init__()

        # Aspect params
        normal = read_params(kwargs, Text.dft_look)
        if hovered is not None:
            hovered = read_params(hovered, normal)
        if clicked and hovered:
            clicked = read_params(clicked, hovered)
        elif clicked:
            clicked = read_params(clicked, normal)

        # Aspect cache
        self._n_txt = Text(
                string, position, align=align, adjust=adjust, **normal
        )
        self._h_txt = (
            None if hovered is None
            else Text(
                string, position, align=align, adjust=adjust, **hovered
            )
        )
        self._c_txt = (
            None if clicked is None
            else Text(
                string, position, align=align, adjust=adjust, **clicked
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
