from abc import abstractmethod
from olutils import read_params

from oldisplay.collections import Color
from oldisplay.utils import split_params
from .component import ActiveComponent, Component


def apply_conversions(params, param_conv):
    if params is None:
        return
    for key, func in param_conv.items():
        val = params[key]
        params[key] = func(val)


class Shape(Component):
    """Base class for linear shapes

    To Specify:
        * dft_look      class attribute that gives default display kwargs
        * par_conv      convertions to apply on parameters

    To Implement:
        * display       display shape on surface given display kwargs
        (*) init        additional initiation once pygame is initialized
    """
    dft_look = {}
    par_conv = {}  # TODO: metaclass to ensure par_conv keys are within dft_look

    def __init__(self, **kwargs):
        """Initiate a linear shape

        Args:
            **kwargs    : aspect of shape
                @see self.__class__.dft_look
        """
        super().__init__(**kwargs)
        look = read_params(kwargs, self.cls.dft_look, safe=False)
        apply_conversions(look, self.cls.par_conv)
        self._params = look

    @property
    def params(self):
        """Parameters for display"""
        return self._params

    def update(self, surface, events=None):
        """Update display of shape on surface"""
        return self.display(surface, **self.params)

    @abstractmethod
    def display(self, surface, **params):
        raise NotImplementedError


class Shape1D(Shape):
    """Base class for linear shapes"""
    dft_look = {
        'color': "black",
        'width': 2,
    }
    par_conv = {'color': Color.get}


class Shape2D(Shape):
    """Base class for 2d shapes"""
    dft_look = {
        'color': "white",
        'outline': "black",
        'width': None,
    }
    par_conv = {'color': Color.get, 'outline': Color.get}


class ActiveShape(ActiveComponent, Shape):
    """Base class for active shapes w. potential look change when hovered or clicked

    To Implement:
        * is_within     return whether a position is within component
        * display       display shape on surface given display kwargs
        (*) init                additional initiation once pygame is initialized
        (*) act_click           called after click on component
        (*) act_release_click   called after click and release on component
        (*) act_release_only    called after release on component (but no click on it)
        (*) act_release_out     called after click on component and release outside
    """

    def __init__(self, **kwargs):
        """Initiate active shape"""
        normal, hovered, clicked = split_params(
            kwargs, 3, dft_params=self.cls.dft_look
        )
        for params in [normal, hovered, clicked]:
            apply_conversions(params, self.par_conv)
        kwargs.update(normal)
        super().__init__(**kwargs)
        self._params = normal
        self._params_h = hovered
        self._params_c = clicked

    @property
    def params_n(self):
        """Parameters for normal display"""
        return self._params

    @property
    def params_h(self):
        """Parameters for hovered display"""
        if self._params_h is None:
            return self.params_n
        return self._params_h

    @property
    def params_c(self):
        """Parameters for clicked display"""
        if self._params_c is None:
            return self.params_h
        return self._params_c

    def display_normal(self, surface):
        """Basic display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        return self.display(surface, **self.params_n)

    def display_hovered(self, surface):
        """Display when mouse passes over the hit box

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        return self.display(surface, **self.params_h)

    def display_clicked(self, surface):
        """Display when user click on component

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        return self.display(surface, **self.params_c)
