if __name__ == "__main__":
    from oldisplay import Window
    from oldisplay.collections import COLORS

    window = Window(
        background=COLORS.green,
    )
    window.open()
    window.wait_close()
