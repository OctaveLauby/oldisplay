import pygame as pg
from logzero import logger

FONTS = pg.font.get_fonts()


class FontManager:

    font_sizing_cache = {
        # fontname: (height factor, height offset)
    }
    font_cache = {}

    @classmethod
    def sizing_params(cls, fontname):
        """Return factor and offset to compute text size in pixels from front size

        About:
            When loading a font one must precise a size that does not match the
            actual height in pixels the text will have. The difference depends on
            the font.

        Return:
            (2-float-tuple): factor and offset of the given font so that
                height (in pixels) = factor * size (of font) + offset
        """
        try:
            return cls.font_sizing_cache[fontname]
        except KeyError:
            pass

        if (fontname is not None) and (fontname not in FONTS):
            logger.warning(f"Unknown font {fontname}, using default")
            fontname = None

        s1, s2 = 100, 200  # I tried a few and those give the best precision
        args = ("Text", True, (0, 0, 0))
        h1 = pg.font.SysFont(fontname, size=s1).render(*args).get_size()[1]
        h2 = pg.font.SysFont(fontname, size=s2).render(*args).get_size()[1]
        factor = (h2 - h1) / (s2 - s1)
        offset = (h1 * s2 - s1 * h2) / (s2 - s1)

        params = (factor, offset)
        cls.font_sizing_cache[fontname] = params
        return params

    @classmethod
    def compute_size(cls, fontname, height):
        """Return font size to use in order to get text with height in pixels"""
        factor, offset = cls.sizing_params(fontname)
        return int(round((height - offset) / factor))

    @classmethod
    def get(cls, **params):
        """Font of text (pygame.font.Font)"""
        key = (
            params['font'],
            params['height'],
            params['bold'],
            params['italic'],
            params['underline'],
        )
        try:
            return cls.font_cache[key]
        except KeyError:
            pass

        font = pg.font.SysFont(
            name=params['font'],
            size=cls.compute_size(params['font'], params['height']),
            bold=params['bold'],
            italic=params['italic'],
        )
        if params['underline']:
            font.set_underline(True)

        cls.font_cache[key] = font
        return font
