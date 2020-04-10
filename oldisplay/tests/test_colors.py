import pytest

import oldisplay.colors as lib


def test_Color():
    Color = lib.Color

    black = Color(0, 0, 0)
    white = Color(255, 255, 255)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)

    with pytest.raises(ValueError):
        Color(0, -1, 0)

    assert red + green + blue == white
    assert white - red - green - blue == black
    assert red - white == black
    assert Color(10, 0, 10) * Color(0, 10, 20) == Color(5, 5, 15)
