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
            dx=50, dy=50, color="cyan", width=1,
        ),

        # Shapes
        components.Rectangle(
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
        components.Disk(
            (425, 25), 25,
            color='light grey', width=10, outline='purple',
        ),
        components.Rectangle(  # Outline width equal size/2
            (500, 0), (50, 50),
            color='red', outline='magenta', width=25,
        ),
        components.ActiveRectangle(  # Outline width greater than size/2
            (600, 0), (50, 50),
            color='red', outline='dark magenta', width=100,
        ),

        # Markers
        components.Cross(
            (100, 100), 5, color='blue'
        ),
        components.Cross(
            (150, 100), 3, color='red', width=2
        ),

        # Placed shapes
        components.Rectangle(
            (0, 150), (50, 50), v_align='bot',
            color='black'
        ),
        components.Rectangle(
            (100, 150), (50, 50), h_align='rgt',
            color='black'
        ),
        components.ActiveRectangle(
            (200, 150), (50, 50), v_align='mid', h_align='mid',
            color='black'
        ),

        # Surrounding Text
        components.Text(
            "top-left", (0, 0),
            align="top-left",
        ),
        components.Text(
            "top-center", (x_max//2, 0),
            align="top-mid"
        ),
        components.Text(
            "top-right", (x_max, 0),
            align="top-right"
        ),
        components.Text(
            "bot-left", (0, y_max),
            align="bot-lft"
        ),
        components.Text(
            "bot-center", (x_max//2, y_max),
            align="bottom-center"
        ),
        components.Text(
            "bot-right", (x_max, y_max),
            align="bot-rgt"
        ),

        # Middle text
        components.Text(
            "arial-50-red", (300, 250), h_align="center",
            font="arial", height=50, color="red"
        ),
        components.Text(
            "candara-20-bold-italic-underline", (300, 300), h_align="center",
            font="candara", height=20,
            bold=True, italic=True, underline=True,
        ),
        components.ActiveText(
            "italic_hover-underline", (300, 350), h_align="center",
            height=20,
            font=("candara", "arial"),
            italic=True,
            underline=(False, True),

        ),
        components.ActiveText(
            "italic_click-bold", (300, 400), h_align="center",
            height=20,
            font=("candara", DFT, None),
            italic=True,
            bold=(False, False, True),

        ),
        components.ActiveText(
            "italic_hover-underline_click-bold", (300, 450), h_align="center",
            height=20,
            font = ("candara", "arial"),
            underline=(DFT, True),
            bold=(False, False, True),
            italic = True,
        ),

    ]
    window.open()
    window.wait_close()
