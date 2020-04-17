if __name__ == "__main__":
    from oldisplay import Window
    from oldisplay.collections import COLORS
    import oldisplay.components as components

    x_max, y_max = 700, 700

    text = components.ActiveText()


    window = Window(
        background=COLORS.white,
        size=(x_max, y_max),
    )
    window.components = [

    ]
    window.open()
    window.wait_close()
