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
            color='blue'
        ),
        Rectangle(
            (100, 0), (100, 100),
            color='green', outline='purple', width=5,
            hovered={'color': "blue"},
        ),
        Rectangle(
            (200, 0), (100, 100),
            color='red',
            hovered={'color': "orange", 'width': 5},
            clicked={'color': "green"},
        ),
    ]
    window.open()
    window.wait_close()
