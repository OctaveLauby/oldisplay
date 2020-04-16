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

        # Aspect
        self.params = read_params(kwargs, self.cls.dft_look)
        self._font = None
        self._surf = None

    def init(self):
        """Initiate font and surface cache, requires pygame.init()"""

        # Initiate font
        self._font = pg.font.SysFont(
            name=self.params.font,
            size=self.params.size,
            bold=self.params.bold,
            italic=self.params.italic,
        )
        if self.params.underline:
            self.font.set_underline(True)

        # Initiate text cache
        self._surf = self.font.render(
            self.content, True, Color.get(self.params.color)
        )

    @property
    def content(self):
        return self._content

    @property
    def font(self):
        """Font of text"""
        return self._font

    @property
    def surface(self):
        """Surface of text"""
        return self._surf

    def compute_position(self):
        """Bottom-Left position of text"""
        x, y = self._position
        dx, dy = self.surface.get_size()


        if self._align == RIGHT:
            x -= dx
        elif self._align == CENTER:
            x -= dx // 2

        if self._adjust == TOP:
            y += dy
        elif self._adjust == CENTER:
            y += dy //2

        return x, y

    def set_adjust(self, adjust):
        """Set kind of adjustment (bottom, center or top)"""
        if adjust not in ADJUSTMENTS:
            raise ValueError(
                f"Unknown value for adjustment {adjust}"
                f", must be within {ADJUSTMENTS}"
            )
        self._adjust = adjust

    def set_align(self, align):
        """Set kind of alignment (left, center or right)"""
        if align not in ALIGNMENTS:
            raise ValueError(
                f"Unknown value for alignment {align}"
                f", must be within {ALIGNMENTS}"
            )
        self._align = align



    def is_within(self, position):
        """Return whether position is within hit box"""
        x, y = position
        sx, sy = self.surface.get_offset()
        dx, dy = self.surface.get_size()
        return (sx < x < sx+dx) and (sy < y < sy+dy)

    def display_normal(self, surface):
        """Basic display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        surface.blit(self.surface, self.compute_position())
