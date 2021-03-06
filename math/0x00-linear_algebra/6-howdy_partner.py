#!/usr/bin/env python3
"""Is a function that concatenates two arrays"""


def cat_arrays(arr1, arr2):
    """Is a function that concatenates two arrays"""
    import numpy as np
    array_1 = np.array(arr1)
    array_2 = np.array(arr2)

    arra_3 = np.concatenate((array_1, array_2), axis=0).tolist()

    return arra_3
