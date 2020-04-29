import pygame as pg
from abc import ABC, abstractmethod

from oldisplay import align


class Component(ABC):
    """Base class for components of a surface

    To Implement:
        *   update      update display
        (*) init        additional initiation once pygame is initialized
    """

    def __init__(self, **kwargs):
        """Initialize component

        Args:
            **kwargs        : to handle diamond problem
        """
        pass

    def init(self):
        """Additional initiation to do once pygame is initialized"""
        pass

    @abstractmethod
    def update(self, surface, events=None):
        """Update display on surface"""
        pass

    # ----------------------------------------------------------------------- #
    # Utils

    @property
    def cls(self):
        """Class of component"""
        return self.__class__

    @property
    def clsname(self):
        """Class name of component"""
        return self.cls.__name__

    def __str__(self):
        return f"<{self.clsname} {id(self)}>"


class ActiveComponent(Component):
    """Base for components of a surface

    To Implement:
        *   is_within           whether a position is within component
        *   display_normal      display shape
        (*) init                additional initiation once pygame is initialized
        (*) display_hovered     display shape when hovered
        (*) display_clicked     display shape when clicked
        (*) act_click           called after click on component
        (*) act_release_click   called after click and release on component
        (*) act_release_only    called after release on component (but no click on it)
        (*) act_release_out     called after click on component and release outside
    """

    def __init__(self, **kwargs):
        """Initialize instance of active component"""
        super().__init__(**kwargs)

        self._enabled = True
        self._visible = True

        # Mouse tracking
        self.is_clicked = False
        self.is_hovered = False

    # ----------------------------------------------------------------------- #
    # Component activation

    @property
    def enabled(self):
        """Whether interactions are enabled"""
        return self._enabled

    @property
    def visible(self):
        """Whether component should be displayed"""
        return self._visible

    def enable(self):
        """Allow interactions with component"""
        self._enabled = True

    def disable(self):
        """Deactivate interactions with component"""
        self._enabled = False

    # ----------------------------------------------------------------------- #
    # Component management

    def _check_event(self, event):
        """The button needs to be passed events from your program event loop."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_clicked = True
                self.act_click()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.is_clicked and self.is_hovered:
                self.act_release_click()
            elif self.is_hovered:
                self.act_release_only()
            elif self.is_clicked:
                self.act_release_out()
            self.is_clicked = False

    def _check_hover(self):
        """Return whether mouse is within component"""
        self.is_hovered = self.is_within(pg.mouse.get_pos())
        return self.is_hovered

    def _display(self, surface):
        """Display component if visible"""
        if self.is_clicked:
            func = self.display_clicked
        elif self.is_hovered:
            func = self.display_hovered
        else:
            func = self.display_normal
        return func(surface)

    def update(self, surface, events=None):
        """Refresh component state"""
        events = [] if events is None else events

        # Mouse / Event tracking
        if not self.enabled:
            self.is_clicked = False
            self.is_hovered = False
        else:
            self._check_hover()
            for event in events:
                self._check_event(event)

        # Display
        if self.visible:
            self._display(surface)


    # ----------------------------------------------------------------------- #
    # ---- To implement

    @abstractmethod
    def is_within(self, position):
        """Return whether position is within hit box"""
        raise NotImplementedError

    # ---- Display

    @abstractmethod
    def display_normal(self, surface):
        """Basic display of element

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        raise NotImplementedError

    def display_hovered(self, surface):
        """Display when mouse passes over the hit box

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        return self.display_normal(surface)

    def display_clicked(self, surface):
        """Display when user click on component

        Args:
            surface (pygame.Surface): surface to draw on (can be a screen)
        """
        return self.display_hovered(surface)

    # ---- Actions

    def act_click(self):
        """Action when user click on component"""
        pass

    def act_release_click(self):
        """Action when user release click on component"""
        pass

    def act_release_only(self):
        """Action when user release click on component but didn't click it"""
        pass

    def act_release_out(self):
        """Action when user release click out of component after clicking it"""
        pass


class LocatedObject(object):
    """Base class for located objects"""

    dft_location = {
        'h_align': align.LEFT,
        'v_align': align.TOP,
    }
    position_func = align.compute_top_left

    def __init__(self, ref_pos, size, **kwargs):
        """Initialize a located component

        Args:
            ref_pos (2-int-tuple)   : reference (x, y) position
            size (2-int-tuple)      : (dx, dy) size of component in pixels
                can be None if size determined later on
            align (str)             : alignment with ref_pos
                'center', 'top-left', 'bot-right', 'top-center', ...
        """
        super().__init__(**kwargs)
        self._pos = None
        self._ref_pos = ref_pos
        self.size = size

        kwargs = align.read_align_params(
            kwargs, self.__class__.dft_location, safe=False
        )
        self.h_align = kwargs.h_align
        self.v_align = kwargs.v_align

    @property
    def position(self):
        """Utility position"""
        if self._pos is None:
            self._pos = self.__class__.position_func(
                self.ref_pos, self.size, self.h_align, self.v_align
            )
        return self._pos

    @property
    def ref_pos(self):
        """Reference position"""
        return self._ref_pos

    @ref_pos.setter
    def ref_pos(self, value):
        """Reference position"""
        self._ref_pos = value
        self._pos = None

    @property
    def size(self):
        """Size of component"""
        return self._size

    @size.setter
    def size(self, value):
        """Set size value"""
        self._size = value
        self._pos = None
