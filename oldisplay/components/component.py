import pygame as pg
from abc import ABC, abstractmethod


class Component(ABC):
    """Base class for components of a surface

    To Implement:

        # update
            update display
    """

    def init(self):
        """Additional initiation to do once pygame is initialized"""
        pass

    @abstractmethod
    def update(self, surface, events=None):
        """Update display on surface"""
        pass


class DynamicComponent(Component):
    """Base for components of a surface

    To Implement:

        # is_within
            Return whether a position is within component

        # display_normal
            Method to display shape given args=(surface, color, outline, width)
    """

    def __init__(self):
        """Initiate instance of component"""
        super().__init__()

        self._enabled = True
        self._visible = True

        # Mouse tracking
        self.clicked = False
        self.hovered = False

    def init(self):
        """Additional initiation to do once pygame is initialized"""
        pass

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

    # ----------------------------------------------------------------------- #
    # Component management

    def _check_event(self, event):
        """The button needs to be passed events from your program event loop."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.clicked = True
                self.act_click()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.clicked and self.hovered:
                self.act_release_click()
            elif self.hovered:
                self.act_release_only()
            elif self.clicked:
                self.act_release_out()
            self.clicked = False

    def _check_hover(self):
        """Return whether mouse is within component"""
        self.hovered = self.is_within(pg.mouse.get_pos())
        return self.hovered

    def _display(self, surface):
        """Display component if visible"""
        if self.clicked:
            func = self.display_clicked
        elif self.hovered:
            func = self.display_hovered
        else:
            func = self.display_normal
        return func(surface)

    def update(self, surface, events=None):
        """Refresh component state"""
        events = [] if events is None else events

        # Mouse / Event tracking
        if not self.enabled:
            self.clicked = False
            self.hovered = False
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
