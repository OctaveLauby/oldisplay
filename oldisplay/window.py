""""Tools to build a window"""
import pygame as pg
from olutils import read_params, wait_until
from threading import Thread

from oldisplay.collections.colors import Color, COLORS



class WindowSettings:
    """Container for window display settings"""

    dft_params = {
        'name': "Application Window",
        'size': (700, 700),
        'fps': 20,
        'background': COLORS.white,
    }

    def __init__(self, **kwargs):
        """Initiate window settings

        Args:
            name (str):         name of window
            size (2-int-tuple): size of window in pixels
            fps (int):          number of frags per seconds
            background (3-int-tuple|str|Color): color of background
                @see collections.COLORS for available colors
        """
        params = read_params(kwargs, self.__class__.dft_params)
        for param, value in params.items():
            self.set(param, value)

    def set(self, param, value):
        """Set param to value"""
        if param == "name":
            assert value is None or isinstance(value, str)
            self.name = value
        elif param == "size":
            assert isinstance(value, tuple)
            self.size = value
        elif param == "fps":
            assert isinstance(value, int) and 1 < value < 200
            self.fps = value
        elif param == "background":
            if isinstance(value, str):
                value = COLORS[value]
            elif isinstance(value, tuple):
                value = Color(*value)
            assert isinstance(value, Color)
            self.background = value
        else:
            raise ValueError(f"Unknown parameter name '{param}'")


class Window:
    """Class to ease window build, display and management"""

    def __init__(self, **kwargs):
        """Initiate a window"""

        # Read window settings
        self._settings = WindowSettings(**kwargs)

        # Screen management
        self.clock = pg.time.Clock()
        self.screen = None
        self.thread = None

        self.initiated = False
        self.stop = False

    # ----------------------------------------------------------------------- #
    # Properties

    @property
    def settings(self):
        """Return setting container"""
        return self._settings

    # ----------------------------------------------------------------------- #
    # Display

    def open(self):
        """Open a window"""
        self.thread = Thread(target=self.refresh)
        self.thread.start()
        wait_until(lambda: self.initiated)

    def wait_close(self):
        """Wait for screen to be closed"""
        self.thread.join()
        self.thread = None

    # ----------------------------------------------------------------------- #
    # Refresh management

    def clean(self):
        """Clean what is on screen"""
        self.screen.fill(self.settings.background)

    def refresh(self):
        """Keep the screen updated"""
        pg.init()
        self.screen = pg.display.set_mode(self.settings.size)
        pg.display.set_caption(self.settings.name)
        self.clean()
        self.initiated = True

        self.stop = False
        while not self.stop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.stop = True
            pg.display.flip()  # Update the full display Surface to the screen
            self.clock.tick(self.settings.fps)
        self.screen = None
        pg.quit()
        self.initiated = False
