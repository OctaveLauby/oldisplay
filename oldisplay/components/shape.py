from abc import abstractmethod
from olutils import read_params

from oldisplay.collections import Color
from .component import Component


class SurfaceShape(Component):

        dft_look = {
            'color': "white",
            'outline': "black",
            'width': None,
        }

        @classmethod
        @abstractmethod
        def build_cache(cls, *args, **kwargs):
            raise NotImplementedError

        def __init__(self, args=None, kwargs=None, look=None):
            """Initiate instance of 2d-shape

            Args:
                args (tuple)    : args for shape building
                kwargs (dict)   : kwargs for shape building
                look (dict)     : aspect description
                    color (color description)   : inside color
                    outline (color description) : outline color
                    width (int)                 : width of outline
                    hovered (dict)              : aspect when mouse over shape
                    clicked (dict)              : aspect when click on shape
            """
            super().__init__()
            args = {} if args is None else args
            kwargs = {} if kwargs is None else kwargs
            look = {} if look is None else look

            # Read Looks
            hovered = look.pop('hovered', None)
            clicked = look.pop('clicked', None)
            self._look = read_params(look, self.cls.dft_look)
            self._look_h = (
                None if hovered is None
                else read_params(hovered, self._look)
            )
            self._look_c = (
                None if clicked is None
                else read_params(clicked, self._look_h or self._look)
            )
            for look in [self._look, self._look_h, self._look_c]:
                if look is None:
                    continue
                for key in ['color', 'outline']:
                    look[key] = Color.get(look[key])

            # Build elements to draw
            self._cache = self.cls.build_cache(*args, **kwargs)

        @property
        def cache(self):
            """Return surface of shape"""
            return self._cache

        @abstractmethod
        def display_(self, surface, color, outline, width):
            raise NotImplementedError

        def display_normal(self, surface, *args, **kwargs):
            """Display shape with normal aspect"""
            return self.display_(surface, **self._look)

        def display_hovered(self, surface, *args, **kwargs):
            """Display shape with hovered aspect"""
            if self._look_h is None:
                return self.display_normal(surface, *args, **kwargs)
            return self.display_(surface, **self._look_h)

        def display_clicked(self, surface, *args, **kwargs):
            """Display shape with clicked aspect"""
            if self._look_c is None:
                return self.display_hovered(surface, *args, **kwargs)
            return self.display_(surface, **self._look_c)