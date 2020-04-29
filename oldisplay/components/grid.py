"""Objects to draw grids"""
from .line import LineSet


class Grid(LineSet):
    """Grid that fills a surface"""

    def __init__(self, dx, dy, **kwargs):
        """Initiate a grid"""
        assert dx > 0, dy > 0
        super().__init__(lines=[], **kwargs)
        self.dx = dx
        self.dy = dy

    def display(self, surface, **params):
        """Display grid on surface"""

        # -- Build lines
        lines = []
        sx, sy = surface.get_size()

        # Vertical lines
        x = 0
        while x <= sx:
            lines.append([(x, 0), (x, sy)])
            x += self.dx

        # Horizontal lines
        y = 0
        while y <= sy:
            lines.append([(0, y), (sx, y)])
            y += self.dy

        # -- Display
        self.lines = lines
        super().display(surface, **params)
