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
        """Initiate font"""
        color = Color.get(self._init_params.pop('color'))
        content = self._init_params.pop('content')
        underline = self._init_params.pop('underline')

        # Initiate font
        self._font = pg.font.SysFont(**self._init_params)
        self._init_params = None
        if underline:
            self._font.set_underline()

        # Initiate text cache
        self._surf = self._font.render(content, True, color)

    @property
    def surface(self):
        return self._surf

    @property
    def position(self):
        # TODO: manage adjust and align
        return self._position

    def get_aspect(self):
        return {
            # 'font': self.font.name,  # TODO: find way to get font name
            'size': self.font.get_height(),
            'bold': self.font.get_bold(),
            'italic': self.font.get_italic(),
            'underline': self.font.get_underline(),
        }

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
        # TODO: implement is within for text and add hovered color
        pass

    def display_normal(self, surface):
        """Basic display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        surface.blit(self.surface, self.position)
