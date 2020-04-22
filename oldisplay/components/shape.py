from abc import abstractmethod
from olutils import read_params

from oldisplay.collections import Color
from oldisplay.utils import read_look
from .component import Component, ActiveComponent, LocatedComponent


class ActiveShape(ActiveComponent):
    """Base class for 2d shapes with look change when hovered or clicked

    Handle an outline and look changes when hovered or clicked

    To Implement:

        # display_
            Method to display shape given args=(surface, color, outline, width)
    """

    dft_look_params = {
        'color': "white",
        'outline': "black",
        'width': None,
    }

    def __init__(self, **kwargs):
        """Initialize instance of 2d-shape

        About:
            For a given parameter, one can give 1-to-3 values within a tuple
            or a list to precise normal, hovered and/or clicked look

        Args:
            color (color|tuple)     : inside color
            outline (color|tuple)   : outline color
            width (int|tuple)       : width of outline
        """
        super().__init__(**kwargs)

        # Read Looks
        looks = read_look(kwargs, self.cls.dft_look_params, safe=False)
        for look in looks:
            if look is None:
                continue
            for key in ['color', 'outline']:
                look[key] = Color.get(look[key])
        self._look, self._look_h, self._look_c = looks

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


class ActiveLocatedShape(LocatedComponent, ActiveShape):

    def __init__(self, ref_pos, size, **kwargs):
        """Initialize instance of rectangle

        Args:
            ref_pos (2-int-tuple)   : reference position in pixels
            size (2-int-tuple)      : size of shape in pixels
            **kwargs                : location and look parameters
                @see LocatedComponent
                @see ActiveShape
        """
        super().__init__(ref_pos=ref_pos, size=size, **kwargs)


class LinearShape(Component):
    """Base class for linear shapes

    To Implement:

        # update
            Method to display shape
    """

    dft_look = {
        'color': "black",
        'width': 2,
    }

    def __init__(self, **kwargs):
        """Initiate a linear shape

        Args:
            **kwargs    : aspect of shape
                color (color)   : color of lines
                width (int)     : width of lines
        """
        super().__init__(**kwargs)
        look = read_params(kwargs, self.cls.dft_look)
        self.color = Color.get(look.color)
        self.width = look.width
