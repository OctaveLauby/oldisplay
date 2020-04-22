from olutils import read_params

LEFT = "left"
LFT_ALIGN = [LEFT, "lft"]

CENTER = "center"
MID_ALIGN = [CENTER, "middle", "mid"]

RIGHT = "right"
RGT_ALIGN = [RIGHT, "rgt"]

TOP = "top"
TOP_ALIGN = [TOP]

BOTTOM = "bottom"
BOT_ALIGN = [BOTTOM, "bot"]

H_ALIGN = [*LFT_ALIGN, *MID_ALIGN, *RGT_ALIGN]
V_ALIGN = [*TOP_ALIGN, *MID_ALIGN, *BOT_ALIGN]


def read_align_params(kwargs, dft_kwargs, safe=False):
    """Read alignments parameters"""
    assert sorted(dft_kwargs.keys()) == ['h_align', 'v_align']
    kwargs = read_params(kwargs, dft_kwargs, safe=safe)
    if kwargs.h_align not in H_ALIGN:
        raise ValueError(
            f"Unknown value for adjustment {kwargs.h_align}"
            f", must be within {H_ALIGN}"
        )
    if kwargs.v_align not in V_ALIGN:
        raise ValueError(
            f"Unknown value for adjustment {kwargs.v_align}"
            f", must be within {V_ALIGN}"
        )
    return kwargs


def compute_center(ref_pos, size, h_align, v_align):
    """Compute center position"""
    x, y = ref_pos
    dx, dy = size
    if h_align == LEFT:
        x += dx // 2
    elif h_align == RIGHT:
        x -= dx // 2
    if v_align == TOP:
        y += dy // 2
    elif v_align == BOTTOM:
        y -= dy // 2
    return x, y

def compute_top_left(ref_pos, size, h_align, v_align):
    """Compute top-left position"""
    x, y = ref_pos
    dx, dy = size
    if h_align in RGT_ALIGN:
        x -= dx
    elif h_align in MID_ALIGN:
        x -= dx // 2
    if v_align in BOT_ALIGN:
        y -= dy
    elif v_align in MID_ALIGN:
        y -= dy //2
    return x, y
