if __name__ == "__main__":
    from oldisplay import Window
    from oldisplay.collections import COLORS
    from oldisplay.components import Rectangle

    window = Window(
        background=COLORS.white,
    )
    window.components = [
        Rectangle(
            (0, 0), (100, 100),
            inner_color='blue'
        ),
        Rectangle(
            (100, 0), (100, 100),
            inner_color='green', border_color='purple', border_width=5
        ),
    ]
    window.open()
    window.wait_close()
