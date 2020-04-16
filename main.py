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
            "default text",
            (300, 200),
        ),
        Text(
            "arial-color-red-center",
            (300, 300),
            size=30, font="arial", align="center", color="red"
        ),
        Text(
            "candara-bold-italic-underline",
            (300, 400),
            size=30, font="candara", bold=True, italic=True, underline=True,
        ),

    ]
    window.open()
    window.wait_close()
