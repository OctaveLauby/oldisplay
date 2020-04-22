if __name__ == "__main__":
    from oldisplay import components, Window, DFT
    from oldisplay.collections import COLORS

    x_max, y_max = 700, 700

    window = Window(
        background=COLORS.white,
        size=(x_max, y_max),
    )
    window.components = [

        # Background
        components.Grid(
            dx=50, dy=50, color="red", width=1,
        ),

        # Shapes
        components.ActiveRectangle(
            ref_pos=(0, 0), size=(50, 50),
            color='blue'
        ),
        components.ActiveRectangle(
            (100, 0), (50, 50),
            color=('green', 'blue'), outline='purple', width=10,
        ),
        components.ActiveRectangle(
            (200, 0), (50, 50),
            color=('red', 'orange', 'green'), width=(DFT, 3),
        ),
        components.ActiveDisk(
            ref_pos=(325, 25), radius=25,
            color=('red', 'orange', 'green'), width=(DFT, 3), outline=(DFT, DFT, 'purple')
        ),
        components.ActiveDisk(
            (425, 25), 25,
            color='cyan', width=10, outline='purple',
        ),
        components.ActiveRectangle(  # Outline width equal size/2
            (500, 0), (50, 50),
            color='red', outline='cyan', width=25,
        ),
        components.ActiveRectangle(  # Outline width greater than size/2
            (600, 0), (50, 50),
            color='red', outline='cyan', width=100,
        ),

        # Placed shapes
        components.ActiveRectangle(
            (0, 150), (50, 50), v_align='bottom',
            color='black'
        ),
        components.ActiveRectangle(
            (100, 150), (50, 50), h_align='right',
            color='black'
        ),
        components.ActiveRectangle(
            (200, 150), (50, 50), v_align='center', h_align='center',
            color='black'
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
            font=("candara", DFT, None),
            italic=True,
            bold=(False, False, True),

        ),
        components.ActiveText(
            "italic_hover-underline_click-bold", (300, 450), h_align="center",
            size=20,
            font = ("candara", "arial"),
            underline=(DFT, True),
            bold=(False, False, True),
            italic = True,
        ),

    ]
    window.open()
    window.wait_close()
