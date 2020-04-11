import pygame as pg
from olutils import Param, read_params

from oldisplay.collections import Color
from .component import Component



class RectangleHitbox():

    def __init__(self, position, size):
        x, y = position
        dx, dy = size
        self.x_min = x
        self.x_max = x + dx
        self.y_min = y
        self.y_max = y + dy

    def is_within(self, position):
        return (
            self.x_min <= position[0] <= self.x_max
            and self.y_min <= position[1] <= self.y_max
        )


class Rectangle(Component):

    dft_look = {
        'inside': "white",
        'border': "black",
        'width': 2,
    }

    def __init__(self, position, size, **kwargs):
        """Initiate instance of rectangle

        Args:
            position (2-int-tuple)  : position of top-right on surface
            size (2-int-tuple)      : size of rectangle
            **kwargs                : aspect description
                inside (color description)
                border (color description)
                width (int)
                hover_look
        """
        super().__init__()
        self.hitbox = RectangleHitbox(position, size)

        # Read Looks
        hovered = kwargs.pop('hovered', None)
        clicked = kwargs.pop('clicked', None)
        self.look = read_params(kwargs, self.cls.dft_look)
        self.look_h = (
            None if hovered is None
            else read_params(hovered, self.look)
        )
        self.look_c = (
            None if clicked is None
            else read_params(clicked, self.look_h if self.look_h else self.look)
        )
        for look in [self.look, self.look_h, self.look_c]:
            if look is None:
                continue
            for key in ['inside', 'border']:
                look[key] = Color.get(look[key])

        # Build elements to draw
        self.rect = pg.Rect(position, size) if self.look.inside else None
        if self.look_h or self.look_c:
            x, y = position
            dx, dy = size
            self.outline = [
                [(x, y), (x + dx, y)],
                [(x + dx, y), (x + dx, y + dy)],
                [(x + dx, y + dy), (x, y + dy)],
                [(x, y + dy), (x, y)],
            ]
        else:
            self.outline = []
            self.disable()

    def is_within(self, position):
        return self.hitbox.is_within(position)

    def display_(self, surface, inside, border, width):
        if self.rect:
            pg.draw.rect(surface, inside, self.rect)
        for p1, p2 in self.outline:
            pg.draw.line(surface, border, p1, p2, width)

    def display_normal(self, surface, *args, **kwargs):
        return self.display_(
            surface,
            self.look.inside,
            self.look.border,
            self.look.width,
        )

    def display_hovered(self, surface, *args, **kwargs):
        if self.look_h is None:
            return self.display_normal(surface, *args, **kwargs)
        return self.display_(
            surface,
            self.look_h.inside,
            self.look_h.border,
            self.look_h.width,
        )

    def display_clicked(self, surface, *args, **kwargs):
        if self.look_c is None:
            return self.display_hovered(surface, *args, **kwargs)
        return self.display_(
            surface,
            self.look_c.inside,
            self.look_c.border,
            self.look_c.width,
        )
