if __name__ == "__main__":
    from oldisplay import Window
    from oldisplay.collections import COLORS
    import oldisplay.components as components

    x_max, y_max = 700, 700

    window = Window(
        background=COLORS.white,
        size=(x_max, y_max),
    )
    window.components = [
        components.Grid(
            dx=50, dy=50, color="gray", width=1,
        ),
        components.ActiveRectangle(
            position=(0, 0), size=(100, 100),
            color='blue'
        ),
        components.ActiveRectangle(
            (100, 0), (100, 100),
            color='green', outline='purple', width=5,
            hovered={'color': "blue"},
        ),
        components.ActiveRectangle(
            (200, 0), (100, 100),
            color='red',
            hovered={'color': "orange", 'width': 5},
            clicked={'color': "green"},
        ),
        components.ActiveDisk(
            center=(350, 50), radius=50,
            color='red',
            hovered={'color': "orange", 'width': 5},
            clicked={'color': "green"},
        ),
        components.Text("top-left", (0, 0), adjust="top"),
        components.Text("top-center", (x_max//2, 0), adjust="top", align="center"),
        components.Text("top-right", (x_max, 0), adjust="top", align="right"),
        components.Text("bot-left", (0, y_max), adjust="bottom"),
        components.Text("bot-center", (x_max//2, y_max), adjust="bottom", align="center"),
        components.Text("bot-right", (x_max, y_max), adjust="bottom", align="right"),
        components.Text(
            "arial-20-red", (300, 250), align="center",
            font="arial", size=20, color="red"
        ),
        components.Text(
            "candara-20-bold-italic-underline",
            (300, 300), align="center",
            font="candara", size=20, bold=True, italic=True, underline=True,
        ),
        components.ActiveText(
            "italic_hover-underline",
            (300, 350), align="center",
            size=20, font="candara", italic=True,
            hovered={'font': "arial", 'underline':True}

        ),
        components.ActiveText(
            "italic_click-bold",
            (300, 400), align="center",
            size=20,  font="candara", italic=True,
            clicked={'font': None, 'bold':True}

        ),
        components.ActiveText(
            "italic_hover-underline_click-bold",
            (300, 450), align="center",
            size=20,  font = "candara", italic = True,
            hovered={'font': "arial", 'underline':True},
            clicked={'font': None, 'bold':True},
        ),

    ]
    window.open()
    window.wait_close()
