import pygame as pg
from abc import ABC, abstractmethod
from olutils import read_params

LEFT = "left"
CENTER = "center"
RIGHT = "right"
H_ALIGN = [LEFT, CENTER, RIGHT]

TOP = "top"
BOTTOM = "bottom"
V_ALIGN = [BOTTOM, CENTER, TOP]


class Component(ABC):
    """Base class for components of a surface

    To Implement:

        # update
            update display

    Optional:

        # init
            additional initiation for once pygame is initialized
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

        # is_within
            Return whether a position is within component

        # display_normal
            Method to display shape

    Optional

        # init
            additional initiation for once pygame is initialized

        # display_hovered
            Method to display shape when hovered

        # display_clicked
            Method to display shape when clicked

        # act_click
            Method called after click on component

        # act_release_click
            Method called after click and release on component

        # act_release_only
            Method called after release on component (but no click on it)

        # act_release_out
            Method called after click on component and release outside
    """

    def __init__(self, **kwargs):
        """Initialize instance of active component"""
        super().__init__(**kwargs)

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


class LocatedComponent(Component):
    """Base class for located components with position management"""

    dft_loc_params = {
        'h_align': LEFT,
        'v_align': TOP,
    }

    def __init__(self, position, size, **kwargs):
        """Initialize a located component

        Args:
            position (2-int-tuple)  : reference (x, y) position
            size (2-int-tuple)      : (dx, dy) size of component in pixels
                can be None if size determined later on
            h_align (str)           : how to horizontally align comp. w. pos.
                'left', 'center' or 'right' (default is 'left')
            v_align (str)           : how to vertically align comp. w. pos.
                'bot', 'center' or 'top' (default is 'top')
        """
        super().__init__(**kwargs)
        self._rpos = position
        self._size = size

        kwargs = read_params(kwargs, self.cls.dft_loc_params, safe=False)
        if kwargs.h_align not in H_ALIGN:
            raise ValueError(
                f"Unknown value for adjustment {kwargs.h_align}"
                f", must be within {H_ALIGN}"
            )
        if kwargs.v_align not in V_ALIGN:
            raise ValueError(
                f"Unknown value for adjustment {kwargs.v_align}"
                f", must be within {V_ALIGN}"
            )
        self.h_align = kwargs.h_align
        self.v_align = kwargs.v_align

    @property
    def rpos(self):
        """Reference position"""
        return self._rpos

    @property
    def size(self):
        """Size of component"""
        return self._size

    @size.setter
    def size(self, value):
        """Set size value"""
        self._size = value

    def compute_position(self):
        """Compute top-left position on surface`"""
        x, y = self.rpos
        dx, dy = self.size

        if self.h_align == RIGHT:
            x -= dx
        elif self.h_align == CENTER:
            x -= dx // 2
        if self.v_align == BOTTOM:
            y -= dy
        elif self.v_align == CENTER:
            y += dy //2

        return x, y
