from oldisplay import utils

DFT = utils.DFT


def test_split_params():
    params = {'a': 1, 'b': (2, 20), 'c': (3, DFT, 30)}
    assert utils.split_params(params, 3) == [
        {'a': 1, 'b': 2, 'c': 3},
        {'a': 1, 'b': 20, 'c': 3},
        {'a': 1, 'b': 20, 'c': 30},
    ]

    params = {'a': 1, 'b': DFT, 'c': 3}
    assert utils.split_params(params, 3) == [
        {'a': 1, 'b': DFT, 'c': 3}, None, None
    ]

    params = {'a': 1, 'b': (2, 20), 'c': 3}
    assert utils.split_params(params, 3) == [
        {'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 20, 'c': 3}, None
    ]

    params = {'a': 10, 'b': DFT, '?': 1}
    dft_params = {'a': 1, 'b': 2, 'c': 3}
    assert utils.split_params(params, 3, dft_params=dft_params) ==  [
        {'a': 10, 'b': 2, 'c': 3}, None, None
    ]

    params = {'a': 10, 'b': (DFT, 30)}
    dft_params = {'a': 1, 'b': 2}
    assert utils.split_params(params, 3, dft_params=dft_params) ==  [
        {'a': 10, 'b': 2}, {'a': 10, 'b': 30}, None
    ]

    params = {
        'a': (10,),
        'b': (DFT, 20),
        'c': (30, DFT, 40),  # hovered c value will be same as normal
        'd': (DFT, 40, DFT),  # clicked d value will be same as hovered
    }
    dft_params = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    assert utils.split_params(params, 3, dft_params=dft_params) ==  [
        {'a': 10, 'b': 2, 'c': 30, 'd': 4},
        {'a': 10, 'b': 20, 'c': 30, 'd': 40},
        {'a': 10, 'b': 20, 'c': 40, 'd': 40},
    ]