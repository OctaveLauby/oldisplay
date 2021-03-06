import pytest

import oldisplay.collections as lib


def test_color():
    Color = lib.colors.Color

    black = Color(0, 0, 0)
    white = Color(255, 255, 255)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)

    assert lib.COLORS.black == black
    assert lib.COLORS.white == white

    with pytest.raises(ValueError):
        Color(0, -1, 0)

    assert red + green + blue == white
    assert white - red - green - blue == black
    assert red - white == black
    assert Color(10, 0, 10) * Color(0, 10, 20) == Color(5, 5, 15)

    assert Color.get('black') is lib.COLORS.black
    assert Color.get('white') is lib.COLORS.white

    with pytest.raises(KeyError):
        Color.get('unknown')
