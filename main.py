if __name__ == "__main__":
    from oldisplay import Window
    from oldisplay.collections import COLORS
    from oldisplay.components import Circle, Rectangle, Text

    x_max, y_max = 700, 700

    window = Window(
        background=COLORS.white,
        size=(x_max, y_max),
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
        Text("top-left", (0, 0), adjust="top"),
        Text("top-center", (x_max//2, 0), adjust="top", align="center"),
        Text("top-right", (x_max, 0), adjust="top", align="right"),
        Text("bot-left", (0, y_max), adjust="bottom"),
        Text("bot-center", (x_max//2, y_max), adjust="bottom", align="center"),
        Text("bot-right", (x_max, y_max), adjust="bottom", align="right"),
        Text(
            "arial-20-red", (300, 250), align="center",
            font="arial", size=20, color="red"
        ),
        Text(
            "candara-20-bold-italic-underline",
            (300, 300), align="center",
            font="candara", size=20, bold=True, italic=True, underline=True,
        ),
        Text(
            "italic_hover-underline",
            (300, 350), align="center",
            size=20, font="candara", italic=True,
            hovered={'font': "arial", 'underline':True}

        ),
        Text(
            "italic_click-bold",
            (300, 400), align="center",
            size=20,  font="candara", italic=True,
            clicked={'font': None, 'bold':True}

        ),
        Text(
            "italic_hover-underline_click-bold",
            (300, 450), align="center",
            size=20,  font = "candara", italic = True,
            hovered={'font': "arial", 'underline':True},
            clicked={'font': None, 'bold':True},
        ),

    ]
    window.open()
    window.wait_close()
