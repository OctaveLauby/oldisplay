from olutils import Param, read_params, DFT


def split_params(params, n, default=DFT, extend_type=tuple):
    """Split an extended dict of params into n set of params

    Args:
        params (dict)       : extended params to split
            for a given parameter, one can give 1-to-n values within an object
            of type extend_type. Value at position i will correspond to value
            of param for i_th dictionary. If a value is default, the value
            will be replaced by the one in previous dictionary
        n (int)             : number of dict of params to build
        default (object)    : default object to use as default value
            if i_th value of a param equal to default, its value is replaced
            by the one of (i-1)_th
        extend_type (type|tuple[type]): type used to extend values of params
            must be iterable type

    Examples:
        >>> params = {'a': 1, 'b': (2, 20), 'c': (3, DFT, 30)}
        >>> split_params(params, 3)
        [
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 1, 'b': 20, 'c': 3},
            {'a': 1, 'b': 20, 'c': 30},
        ]

        >>> params = {'a': 1, 'b': DFT, 'c': 3}
        >>> split_params(params, 3)
        [{'a': 1, 'b': DFT, 'c': 3}, None, None]

    Return:
        (list[Param]): n dict of params
    """
    assert n > 0

    # Read params
    param_dicts = [{} for i in range(n)]
    for key, extend_val in params.items():
        if not isinstance(extend_val, extend_type):
            param_dicts[0][key] = extend_val
            continue

        prev_val = default
        for i, val in enumerate(extend_val):
            try:
                param_dicts[i][key] = prev_val if val is default else val
            except IndexError:
                raise ValueError(
                    f"Parameter '{key}' has more than n={n} values"
                )
            prev_val = val

    # Complete params
    prev_kwargs = param_dicts[0]
    result = [prev_kwargs]
    for kwargs in param_dicts[1:]:
        if not kwargs:
            result.append(None)
            continue

        ext_kwargs = prev_kwargs.copy()
        ext_kwargs.update(kwargs)
        result.append(Param(ext_kwargs))
        prev_kwargs = ext_kwargs

    return result


def read_look(params, dft_params, safe=False, default=DFT):
    """Read params to split normal, hovered and clicked params


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
    # Split params
    normal, hovered, clicked = tuple(split_params(
        params, 3, default=default, extend_type=(list, tuple)
    ))

    # Complete with default
    normal = read_params(normal, dft_params, safe=safe)
    if hovered:
        hovered = read_params(hovered, dft_params, safe=safe)
    if clicked:
        clicked = read_params(clicked, dft_params, safe=safe)

    # Return result
    return normal, hovered, clicked


if __name__ == "__main__":
    params = {'a': 1, 'b': (2, 20), 'c': (3, DFT, 30)}
    print(split_params(params, 3))