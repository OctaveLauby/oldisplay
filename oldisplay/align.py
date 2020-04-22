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


def _read_align_param(align):
    """Convert string to (h_align, v_align)

    Args:
        align (str): alignment description
            '{v_align}-{h_align}' where v_align/h_align in V_ALIGN/H_ALIGN
            '{mid_align}' where mid_align in MID_ALIGN

    Return:
        (dict): {'h_align': (str), 'v_align': (str)}
    """
    items = align.replace("_", "-").replace(" ", "-").split("-")
    if len(items) == 1:
        if items[0] in MID_ALIGN:
            return CENTER, CENTER
        raise ValueError(
            f"align param must be within {MID_ALIGN}, got '{align}'"
        )
    if len(items) == 2:
        if items[0] not in V_ALIGN:
            raise ValueError(
                f"Fist item of align param must be within {V_ALIGN}"
                f", got '{items[0]}'"
            )
        if items[1] not in H_ALIGN:
            raise ValueError(
                f"Second item of align param must be within {H_ALIGN}"
                f", got '{items[1]}'"
            )
        return {'h_align': items[1], 'v_align': items[0]}
    raise ValueError(
        f"align param must have 2 items separated with '-' char"
        f", got align"
    )


def read_align_params(kwargs, dft_kwargs, safe=False):
    """Read alignments parameters

    Args:
        kwargs (dict)       : parameters for alignment
            'h_align': (str)    -> horizontal alignment (within H_ALIGN)
            'v_align': (str)    -> vertical alignment (within V_ALIGN)
            'align': (str)      -> alignment ("{h_align}-{v_align}")
                overwrite other params
        dft_kwargs (dict)   : default parameters for alignment
            'h_align': (str)    -> horizontal alignment (within H_ALIGN)
            'v_align': (str)    -> vertical alignment (within V_ALIGN)
        safe (bool)         : raise Error if kwargs has unexpected params

    Return:
        (olutils.Param): dictionary with alignment params
            'h_align': (str)    -> horizontal alignment (within H_ALIGN)
            'v_align': (str)    -> vertical alignment (within V_ALIGN)
    """
    assert sorted(dft_kwargs.keys()) == ['h_align', 'v_align']
    if 'align' in kwargs:
        kwargs = _read_align_param(kwargs['align'])
    kwargs = read_params(kwargs, dft_kwargs, safe=safe)
    if kwargs.h_align not in H_ALIGN:
        raise ValueError(
            f"Unknown value for adjustment '{kwargs.h_align}'"
            f", must be within {H_ALIGN}"
        )
    if kwargs.v_align not in V_ALIGN:
        raise ValueError(
            f"Unknown value for adjustment '{kwargs.v_align}'"
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
