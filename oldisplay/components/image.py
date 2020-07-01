import pygame as pg

from oldisplay.components.component import LocatedObject, Component


class Image(LocatedObject, Component):

    def __init__(self, path, ref_pos, size, **kwargs):
        super().__init__(ref_pos, size, **kwargs)
        self.image = pg.transform.scale(
            pg.image.load(path),size
        )

    def update(self, surface, **params):
        """Display disk regarding given look parameters"""
        surface.blit(self.image, self.position)
