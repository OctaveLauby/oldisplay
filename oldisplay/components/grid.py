"""Objects to draw grids"""
import numpy as np
from logzero import logger

from .line import LineSet


class Grid(LineSet):
    """Grid that fills a surface

    Attributes:
        dx (int)        : number of pixels b/w consecutive vertical lines
        dy (int)        : number of pixels b/w consecutive horizontal lines
        xbounds (int)   : bounds of vertical lines within surface
        ybounds (int)   : bounds of horizontal lines within surface
        i_max (int)     : number of horizontal lines
        j_max (int)     : number of vertical columns
        cell_nb (int)   : number of cells of grid
        only_inside (bool): only inner lines are drawn
    """

    def __init__(self, dx, dy, xbounds=None, ybounds=None,
                 only_inside=False, **kwargs):
        """Initiate a grid

        Args:
            dx (int): nb of pixels b/w 2 vertical lines
            dy (int): nb of pixels b/w 2 horizontal lines
            xbounds (2-int-tuple)   : x-boundaries of grid
            ybounds (2-int-tuple)   : y-boundaries of grid
            only_inside (bool)      : draw only inner lines
        """
        assert dx > 0, dy > 0
        super().__init__(lines=[], **kwargs)
        self.dx = dx
        self.dy = dy
        self._xbounds = (0, np.inf) if xbounds is None else xbounds
        self._ybounds = (0, np.inf) if ybounds is None else ybounds
        self.only_inside = only_inside

        # To be computed regarding the surface
        self.surf_size = None
        self.xbounds = None
        self.ybounds = None
        self.i_max = None
        self.j_max = None
        self.cell_nb = None

    def init(self, surface, *args, **kwargs):
        """Initiate grid indicators regarding surface available"""
        sx, sy = surface.get_size()
        if self.surf_size == (sx, sy):
            return
        x_min, x_max = self._xbounds
        y_min, y_max = self._ybounds
        x_max, y_max = min(x_max, sx), min(y_max, sy)

        assert x_max >= x_min, "x-min bound must smaller than surface x-size"
        assert y_max >= y_min, "y-min bound must smaller than surface y-size"
        assert (x_max-x_min) >= self.dx, "grid dx must be smaller than grid x-span"
        assert (y_max-y_min) >= self.dy, "grid dy must be smaller than grid y-span"

        i_max = (y_max-y_min) // self.dy
        j_max = (x_max-x_min) // self.dx
        cell_nb = i_max * j_max

        self.xbounds = (x_min, x_max)
        self.ybounds = (y_min, y_max)
        self.i_max = i_max
        self.j_max = j_max
        self.cell_nb = cell_nb

        logger.debug(
            f"Grid initialized with {self.i_max}x{self.j_max}={self.cell_nb} cells"
        )

    @property
    def start(self):
        """(x, y) position where grid starts on surface"""
        return self.xbounds[0], self.ybounds[0]

    def display(self, surface, **params):
        """Display grid on surface"""
        self.init(surface)  # Re-initiate indicators in case surface changed
        x_min, x_max = self.xbounds
        y_min, y_max = self.ybounds

        # -- Build lines
        lines = []

        # Vertical lines
        x = x_min
        while x <= x_max:
            if self.only_inside and x in [x_min, x_max]:
                pass
            else:
                lines.append([(x, y_min), (x, y_max)])
            x += self.dx

        # Horizontal lines
        y = y_min
        while y <= y_max:
            if self.only_inside and y in [y_min, y_max]:
                pass
            else:
                lines.append([(x_min, y), (x_max, y)])
            y += self.dy

        # -- Display
        self.lines = lines
        super().display(surface, **params)

    def ij_enum(self, items):
        """Enumerate items with i,j cell-positions"""
        if len(items) > self.cell_nb:
            logger.waring(
                f"There are more items ({len(items)}) than the number of cells"
                f" ({self.cell_nb}), last items will be skipped"
            )
        for k, item in enumerate(items):
            j = k % self.j_max
            i = k // self.j_max
            if i >= self.i_max:
                break
            yield (i, j), item


    def xy_enum(self, items):
        """Enumerate items with x,y cell-positions (top-left)"""
        x0, y0 = self.start
        for (i, j), item in self.ij_enum(items):
            yield (x0+j*self.dx, y0+i*self.dy), item
