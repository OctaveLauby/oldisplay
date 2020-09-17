"""Objects to draw grids"""
import numpy as np
from logzero import logger

from .line import LineSet



class Grid(LineSet):
    """Grid that fills a surface

    Attributes:
        start (tuple)   : start position of grid
        dx (int)        : number of pixels b/w consecutive vertical lines
        dy (int)        : number of pixels b/w consecutive horizontal lines
        row_nb (int)    : number of horizontal rows
        col_nb (int)    : number of vertical columns
        only_inside (bool): only inner lines are drawn
    """

    def __init__(self, start, dx, dy, col_nb, row_nb,
                 only_inside=False, **kwargs):
        """Initiate an instance of grid

        Careful as dx is the width of a column and dy the height of a row
        """
        super().__init__(lines=[], **kwargs)
        self.start = start
        self.dx = dx
        self.dy = dy
        self.row_nb = row_nb
        self.col_nb = col_nb
        self.only_inside = only_inside

    def init(self, surface):
        self.lines = self.build_lines()
        logger.debug(
            f"Grid initialized with {self.row_nb}x{self.col_nb}={self.cell_nb}"
            f" cells ({len(self.lines)} lines)"
        )

    @property
    def cell_nb(self):
        """Number of positions in grid"""
        return self.row_nb * self.col_nb

    @property
    def x_min(self):
        return self.start[0]

    @property
    def x_max(self):
        return self.x_min + self.dx * self.col_nb

    @property
    def x_bounds(self):
        return self.x_min, self.x_max

    @property
    def y_min(self):
        return self.start[1]

    @property
    def y_max(self):
        return self.y_min + self.dy * self.row_nb

    @property
    def y_bounds(self):
        return self.y_min, self.y_max

    def build_lines(self):
        """Build lines of grid"""
        assert self.dx > 0 and self.dy > 0
        assert self.col_nb > 0 and self.row_nb > 0

        inner = int(self.only_inside)
        lines = []

        y_min, y_max = self.y_bounds
        for i in range(inner, self.row_nb - inner):
            x = self.x_min+i*self.dx
            lines.append([(x, y_min), (x, y_max)])

        x_min, x_max = self.x_bounds
        for j in range(inner, self.col_nb - inner):
            y = self.y_min + j * self.dy
            lines.append([(x_min, y), (x_max, y)])

        return lines

    def ij_enum(self, items):
        """Enumerate items with i,j cell-positions"""
        if len(items) > self.cell_nb:
            logger.waring(
                f"There are more items ({len(items)}) than the number of cells"
                f" ({self.cell_nb}), last items will be skipped"
            )
        for k, item in enumerate(items):
            j = k % self.col_nb
            i = k // self.col_nb
            if i >= self.row_nb:
                break
            yield (i, j), item

    def xy_enum(self, items):
        """Enumerate items with x,y cell-positions (top-left)"""
        x0, y0 = self.start
        for (i, j), item in self.ij_enum(items):
            yield (x0+j*self.dx, y0+i*self.dy), item



class FillingGrid(Grid):
    """Grid that fills a surface"""

    def __init__(self, dx, dy, x_bounds=None, y_bounds=None, **kwargs):
        """Initiate a grid

        Args:
            dx (int): nb of pixels b/w 2 vertical lines
            dy (int): nb of pixels b/w 2 horizontal lines
            x_bounds (2-int-tuple)  : x-boundaries of grid
            y_bounds (2-int-tuple)  : y-boundaries of grid
            only_inside (bool)      : draw only inner lines
        """

        super().__init__(
            start=None, dx=dx, dy=dy, col_nb=None, row_nb=None, **kwargs
        )
        self._x_bounds = (0, np.inf) if x_bounds is None else x_bounds
        self._y_bounds = (0, np.inf) if y_bounds is None else y_bounds
        self.surf_size_cache = None

    def init(self, surface, *args, **kwargs):
        """Initiate grid indicators regarding surface available"""
        sx, sy = surface.get_size()
        if self.surf_size_cache == (sx, sy):
            return
        x_min, x_max = self._x_bounds
        y_min, y_max = self._y_bounds
        x_max, y_max = min(x_max, sx), min(y_max, sy)

        assert x_max >= x_min, f"x_min={x_min} > x_max={x_max}"
        assert y_max >= y_min, f"y_min={y_min} > y_max={y_max}"
        assert (x_max-x_min) >= self.dx, "grid dx must be smaller than grid x-span"
        assert (y_max-y_min) >= self.dy, "grid dy must be smaller than grid y-span"

        row_nb = (y_max-y_min) // self.dy
        col_nb = (x_max-x_min) // self.dx

        self.start = (x_min, x_max)
        self.row_nb = row_nb
        self.col_nb = col_nb
        super().init(surface, *args, **kwargs)


# TODO: implement BoardGrid
# # class BoardGrid(Grid):
# #     """Grid defined by the number of columns and rows"""
