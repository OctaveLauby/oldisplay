if __name__ == "__main__":
    from oldisplay import Window
    from oldisplay.collections import COLORS
    from oldisplay.components import Circle, Rectangle, Text

    window = Window(
        background=COLORS.white,
    )
    window.components = [
        Rectangle(
            position=(0, 0), size=(100, 100),
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
        Circle(
            center=(350, 50), radius=50,
            color='red',
            hovered={'color': "orange", 'width': 5},
            clicked={'color': "green"},
        ),
        Text(
            (300, 200), "default text"
        ),
        Text(
            (300, 300), "arial-color-red-center",
            size=30, font="arial", align="center", color="red"
        ),

    ]
    window.open()
    window.wait_close()
