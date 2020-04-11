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
            inside='blue'
        ),
        Rectangle(
            (100, 0), (100, 100),
            inside='green', border='purple', width=5,
            hovered={'inside': "blue"},
        ),
        Rectangle(
            (200, 0), (100, 100),
            inside='red', width=5,
            hovered={'inside': "orange"},
            clicked={'inside': "green"},
        ),
    ]
    window.open()
    window.wait_close()
