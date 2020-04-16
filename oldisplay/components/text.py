import pygame as pg
from olutils import read_params

from oldisplay.collections import Color
from .component import Component

TOP = "top"
BOTTOM = "bottom"
LEFT = "left"
RIGHT = "right"
CENTER = "center"
ADJUSTMENTS = [BOTTOM, CENTER, TOP]
ALIGNMENTS = [LEFT, CENTER, RIGHT]


class Text(Component):

    dft_look = {
        'size': 12,
        'font': None,  # default system font
        'color': "black",
        'bold': False,
        'italic': False,
        'underline': False,
    }

    def __init__(self, content, position, align=LEFT, adjust=BOTTOM, **kwargs):
        """Initiate params of text to display

        Args:
            content (str)           : text displayed
            position (2-int-tuple)  : position of text
            align (str)             : where position is regarding text (x-axis)
                left, center or right
            adjust (str)            : where position is regarding text (y-axis)
                bottom, center or top
            **kwargs                : aspect of text\
                size (int)              : size of font
                font (str)              : name of font
                color (color descr)     : color of display
                bold (bool)             : use bold writing
                italic  (bool)          : use italic writing
                underline (bool)        : underline writing
        """
        super().__init__()

        # Position
        self._content = content
        self._position = position
        self._adjust = None
        self._align = None
        self.set_adjust(adjust)
        self.set_align(align)

        # Aspect params
        hovered = kwargs.pop('hovered', None)
        clicked = kwargs.pop('clicked', None)
        self.params = read_params(kwargs, self.cls.dft_look)
        self._hovered = None
        self._clicked = None
        if hovered is not None:
            hovered = read_params(hovered, self.params)
        if clicked and hovered:
            clicked = read_params(clicked, hovered)
        elif clicked:
            clicked = read_params(clicked, self.params)

        # Aspect cache
        self._font = None
        self._surf = None
        self._h_txt = (
            None if hovered is None
            else Text(content, position, align=align, adjust=adjust, **hovered)
        )
        self._c_txt = (
            None if clicked is None
            else Text(content, position, align=align, adjust=adjust, **clicked)
        )


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
            self.content, True, Color.get(self.params.color)
        )

        # Update
        self._font, self._surf = font, surface
        if self.hover_txt is not None:
            self.hover_txt.init()
        if self.click_txt is not None:
            self.click_txt.init()

    @property
    def content(self):
        """Text displayed (str)"""
        return self._content

    @property
    def font(self):
        """Font of text (pygame.font.Font)"""
        return self._font

    @property
    def surface(self):
        """Surface of text (pygame.Surface)"""
        return self._surf

    @property
    def hover_txt(self):
        return self._h_txt

    @property
    def click_txt(self):
        return self._c_txt

    def compute_position(self):
        """Bottom-Left position of text (2-int-tuple)"""
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

    def is_within(self, position):
        """Return whether position is within hit box"""
        x, y = position
        sx, sy = self.compute_position()
        dx, dy = self.surface.get_size()
        return (sx < x < sx+dx) and (sy < y < sy+dy)

    def display_normal(self, surface):
        """Basic display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        surface.blit(self.surface, self.compute_position())

    def display_hovered(self, surface):
        """Hovered display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        if self.hover_txt is None:
            return self.display_normal(surface)
        surface.blit(self.hover_txt.surface, self.hover_txt.compute_position())

    def display_clicked(self, surface):
        """Clicked display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        if self.click_txt is None:
            return self.display_normal(surface)
        surface.blit(self.click_txt.surface, self.click_txt.compute_position())
