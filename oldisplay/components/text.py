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
    }

    def __init__(self, position, content,
                 size=None, font=None, color=None,
                 bold=False, italic=False, underline=False,
                 align=LEFT, adjust=BOTTOM):
        """Initiate params of text to display

        Args:
            position (2-int-tuple)  : position of text
            content (str)           : text displayed
            size (int)              : size of font
            font (str)              : name of font
            color (color descr)     : color of display
            bold (bool)             : use bold writing
            italic  (bool)          : use italic writing
            underline (bool)        : underline writing
            align (str)             : where position is regarding text (x-axis)
                left, center or right
            adjust (str)            : where position is regarding text (y-axis)
                bottom, center or top
        """
        super().__init__()

        # Position
        self._position = position
        self._adjust = None
        self._align = None
        self.set_adjust(adjust)
        self.set_align(align)

        # Aspect
        self._init_params = {
            'name': font if font else self.cls.dft_look['font'],
            'size': size if size else self.cls.dft_look['size'],
            'bold': bold,
            'italic': italic,
            'underline': underline,
            'color': color if color else self.cls.dft_look['color'],
            'content': content,
        }
        self._font = None
        self._surf = None

    def init(self):
        """Initiate font and surface cache, requires pygame.init()"""
        color = Color.get(self._init_params.pop('color'))
        content = self._init_params.pop('content')
        underline = self._init_params.pop('underline')

        # Initiate font
        self._font = pg.font.SysFont(**self._init_params)
        self._init_params = None
        if underline:
            self.font.set_underline(True)

        # Initiate text cache
        self._surf = self.font.render(content, True, color)

    @property
    def font(self):
        """Font of text"""
        return self._font

    @property
    def surface(self):
        """Surface of text"""
        return self._surf

    @property
    def position(self):
        """Bottom-Left position of text"""
        x, y = self._position
        dx, dy = self.surface.get_size()
        if self._align == RIGHT:
            x -= dx
        elif self._align == CENTER:
            x -= dx // 2

        if self._align == TOP:
            y += dy
        elif self._align == CENTER:
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
        surface.blit(self.surface, self.position)
