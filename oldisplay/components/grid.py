"""Objects to draw grids"""
import numpy as np
from .line import LineSet


class Grid(LineSet):
    """Grid that fills a surface"""

    def __init__(self, dx, dy, xbounds=None, ybounds=None, **kwargs):
        """Initiate a grid"""
        assert dx > 0, dy > 0
        super().__init__(lines=[], **kwargs)
        self.dx = dx
        self.dy = dy
        self.xbounds = (0, np.inf) if xbounds is None else xbounds
        self.ybounds = (0, np.inf) if ybounds is None else ybounds

    def display(self, surface, **params):
        """Display grid on surface"""

        # -- Build lines
        lines = []
        sx, sy = surface.get_size()
        x_min, x_max = self.xbounds
        y_min, y_max = self.ybounds
        x_max, y_max = min(x_max, sx), min(y_max, sy)

        # Vertical lines
        x = x_min
        while x <= x_max:
            lines.append([(x, y_min), (x, y_max)])
            x += self.dx

        # Horizontal lines
        y = y_min
        while y <= y_max:
            lines.append([(x_min, y), (x_max, y)])
            y += self.dy

        # -- Display
        self.lines = lines
        super().display(surface, **params)
