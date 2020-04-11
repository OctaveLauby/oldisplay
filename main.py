if __name__ == "__main__":
    from oldisplay import Window
    from oldisplay.collections import COLORS
    from oldisplay.components import Rectangle

    window = Window(
        background=COLORS.white,
    )
    window.components = [
        Rectangle((0, 0), (100, 100), 'blue'),
        Rectangle((100, 0), (100, 100), 'green', 'purple', 5),
    ]
    window.open()
    window.wait_close()
