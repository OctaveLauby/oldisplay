if __name__ == "__main__":
    from oldisplay import components, Window, _default
    from oldisplay.collections import COLORS
    import oldisplay.components as components

    x_max, y_max = 700, 700

    window = Window(
        background=COLORS.white,
        size=(x_max, y_max),
    )
    window.components = [

        # Background
        components.Grid(
            dx=50, dy=50, color="gray", width=1,
        ),

        # Shapes
        components.ActiveRectangle(
            position=(0, 0), size=(100, 100),
            color='blue'
        ),
        components.ActiveRectangle(
            (100, 0), (100, 100),
            color=('green', 'blue'), outline='purple', width=5,
        ),
        components.ActiveRectangle(
            (200, 0), (100, 100),
            color=('red', 'orange', 'green'), width=(_default, 5),
        ),
        components.ActiveDisk(
            center=(350, 50), radius=50,
            color=('red', 'orange', 'green'), width=(_default, 5), outline=(_default, _default, 'purple')
        ),

        # Surrounding Text
        components.Text(
            "top-left", (0, 0),
            v_align="top",
        ),
        components.Text(
            "top-center", (x_max//2, 0),
            v_align="top", h_align="center"
        ),
        components.Text(
            "top-right", (x_max, 0),
            v_align="top", h_align="right"
        ),
        components.Text(
            "bot-left", (0, y_max),
            v_align="bottom"
        ),
        components.Text(
            "bot-center", (x_max//2, y_max),
            v_align="bottom", h_align="center"
        ),
        components.Text(
            "bot-right", (x_max, y_max),
            v_align="bottom", h_align="right"
        ),

        # Middle text
        components.Text(
            "arial-20-red", (300, 250), h_align="center",
            font="arial", size=20, color="red"
        ),
        components.Text(
            "candara-20-bold-italic-underline", (300, 300), h_align="center",
            font="candara", size=20,
            bold=True, italic=True, underline=True,
        ),
        components.ActiveText(
            "italic_hover-underline", (300, 350), h_align="center",
            size=20,
            font=("candara", "arial"),
            italic=True,
            underline=(False, True),

        ),
        components.ActiveText(
            "italic_click-bold", (300, 400), h_align="center",
            size=20,
            font=("candara", _default, None),
            italic=True,
            bold=(False, False, True),

        ),
        components.ActiveText(
            "italic_hover-underline_click-bold", (300, 450), h_align="center",
            size=20,
            font = ("candara", "arial"),
            underline=(_default, True),
            bold=(False, False, True),
            italic = True,
        ),

    ]
    window.open()
    window.wait_close()
