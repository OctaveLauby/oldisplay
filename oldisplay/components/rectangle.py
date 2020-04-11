import pygame as pg

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

    def __init__(self, position, size, inner_color='white',
                 border_color='black', border_width=2):
        super().__init__()
        self.hitbox = RectangleHitbox(position, size)

        if inner_color:
            self.inner_c = Color.get(inner_color)
            self.rect = pg.Rect(position, size)
        else:
            self.inner_c = None
            self.rect = None

        if border_color and border_width:
            self.outer_c = Color.get(border_color)
            self.outer_w = border_width
            x, y = position
            dx, dy = size
            self.outline = [
                [(x, y), (x + dx, y)],
                [(x + dx, y), (x + dx, y + dy)],
                [(x + dx, y + dy), (x, y + dy)],
                [(x, y + dy), (x, y)],
            ]
        else:
            self.outer_c = None
            self.outer_w = None
            self.outline = []

    def is_within(self, position):
        return self.hitbox.is_within(position)

    def display_normal(self, surface):
        if self.rect:
            pg.draw.rect(surface, self.inner_c, self.rect)
        for p1, p2 in self.outline:
            pg.draw.line(surface, self.outer_c, p1, p2, self.outer_w)
