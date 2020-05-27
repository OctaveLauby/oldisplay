"""Objects to draw markers"""
from .line import LineSet


class Cross(LineSet):

    def __init__(self, center, size=1, **kwargs):
        """Initialize a set of line

        Args:
            center (2-int tuple): position of the cross
            size (int)      : size in pixels of a branch
            color (color)   : color of lines
            width (int)     : width of lines
        """
        x, y = center
        super().__init__(lines=[
            [(x-size, y), (x+size, y)], [(x, y-size), (x, y+size)]],
            **kwargs
        )
