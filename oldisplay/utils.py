from olutils import Param, read_params, DFT


def read_look(params, dft_params, safe=False, default=DFT):
    """Read params to return normal, hovered and clicked look


    Args:
        params (dict)       : look parameters
            for a given parameter, one can give 1-to-3 values within a tuple
            or a list to precise normal, hovered and/or clicked look
        dft_params (dict)   : default look parameters
        safe (bool)         : raise error when params has unexpected params
        default (object)    : value to replace with dft value
            default used for on hovered value will be replaced by normal value
            default used for on clicked value will be replaced by hovered value

    Examples:
        >>> params = {'a': 10, 'b': DFT, '?': 1}
        >>> dft_params = {'a': 1, 'b': 2, 'c': 3}
        >>> read_look(params, dft_params)
        ({'a': 10, 'b': 2, 'c': 3}, None, None)

        >>> params = {'a': 10, 'b': (DFT, 30)}
        >>> dft_params = {'a': 1, 'b': 2}
        >>> read_look(params, dft_params)
        ({'a': 10, 'b': 2}, {'a': 10, 'b': 30}, None)

        >>> params = {
        ...     'a': (10,),
        ...     'b': (DFT, 20),
        ...     'c': (30, DFT, 40),  # hovered c value will be same as normal
        ...     'd': (DFT, 40, DFT), # clicked d value will be same as hovered
        ... }
        >>> dft_params = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        >>> read_look(params, dft_params)
        (
            {'a': 10, 'b': 2, 'c': 30, 'd': 4},
            {'a': 10, 'b': 20, 'c': 30, 'd': 40},
            {'a': 10, 'b': 20, 'c': 40, 'd': 40},
        )

    Return:
        (3-dict-tuple) parameters for normal, hovered and clicked look
            hovered and clicked params can be None
    """
    # Ensure params has all key
    params = read_params(params, dft_params, safe=safe, default=default)

    # Gather params for normal, hovered and clicked look
    normal = {}
    hovered = {}
    clicked = {}
    for key, val in params.items():
        if isinstance(val, (list, tuple)):
            if len(val) < 1 or len(val) > 3:
                raise ValueError(
                    f"Expecting 1-to-3 values for param '{key}', one for"
                    f" normal look, hovered look (opt.) & clicked look (opt.)"
                    f": got {len(val)} values"
                )
            if len(val) >= 1:
                normal[key] = dft_params[key] if val[0] is default else val[0]
            if len(val) >= 2:
                hovered[key] = normal[key] if val[1] is default else val[1]
            if len(val) >= 3:
                clicked[key] = hovered[key] if val[2] is default else val[2]
        else:
            normal[key] = val

    # Ensure each set has all params
    normal = Param(normal)

    if hovered:
        hovered = read_params(hovered, normal)
    else:
        hovered = None

    if hovered and clicked:
        clicked = read_params(clicked, hovered)
    elif clicked:
        clicked = read_params(clicked, normal)
    else:
        clicked = None

    # Return result
    return normal, hovered, clicked
