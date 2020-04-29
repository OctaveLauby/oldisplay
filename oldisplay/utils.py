"""Common util functions over project"""
from olutils import read_params, DFT


def split_params(params, n, dft_value=DFT, extend_type=tuple,
                 dft_params=None, safe=False):
    """Split an extended dict of params into n dicts of params

    Args:
        params (dict)       : extended params to split
            for a given parameter, one can give 1-to-n values within an object
            of type extend_type. Value at position i will correspond to value
            of param for i_th dictionary. If a value is default, the value
            will be replaced by the one in previous dictionary
        n (int)             : number of dict of params to build
        dft_value (object)    : default object to use as default value
            if i_th value of a param equal to default, its value is replaced
            by the one of (i-1)_th
        extend_type (type|tuple[type]): type used to extend values of params
            must be iterable type
        dft_params (dict)   : default parameters
        safe (bool)         : raise error when params are not in dft_params

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

        >>> params = {'a': 10, 'b': DFT, '?': 1}
        >>> dft_params = {'a': 1, 'b': 2, 'c': 3}
        >>> split_params(params, 3, dft_params=dft_params)
        ({'a': 10, 'b': 2, 'c': 3}, None, None)

        >>> params = {'a': 10, 'b': (DFT, 30)}
        >>> dft_params = {'a': 1, 'b': 2}
        >>> split_params(params, 3, dft_params=dft_params)
        ({'a': 10, 'b': 2}, {'a': 10, 'b': 30}, None)

        >>> params = {
        ...     'a': (10,),
        ...     'b': (DFT, 20),
        ...     'c': (30, DFT, 40),  # hovered c value will be same as normal
        ...     'd': (DFT, 40, DFT), # clicked d value will be same as hovered
        ... }
        >>> dft_params = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        >>> split_params(params, 3, dft_params=dft_params)
        (
            {'a': 10, 'b': 2, 'c': 30, 'd': 4},
            {'a': 10, 'b': 20, 'c': 30, 'd': 40},
            {'a': 10, 'b': 20, 'c': 40, 'd': 40},
        )

    Return:
        (list[Param|NoneType]): n dict of params
    """
    assert n > 0

    # Read params
    param_dicts = [{} for i in range(n)]
    for key, extend_val in params.items():
        if not isinstance(extend_val, extend_type):
            param_dicts[0][key] = extend_val
            continue

        prev_val = dft_value
        for i, val in enumerate(extend_val):
            try:
                param_dicts[i][key] = prev_val if val is dft_value else val
            except IndexError:
                raise ValueError(
                    f"Parameter '{key}' has more than n={n} values"
                )
            prev_val = val

    # Complete params
    prev_kwargs = dft_params if dft_params else param_dicts[0]
    result = []
    for kwargs in param_dicts:
        if not kwargs:
            result.append(None)
            continue
        kwargs = read_params(kwargs, prev_kwargs, safe=safe, default=dft_value)
        result.append(kwargs)
        prev_kwargs = kwargs

    return result
