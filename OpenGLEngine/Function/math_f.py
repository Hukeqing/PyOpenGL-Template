import glm
import numpy as np


def ceil(value):
    if int(value) == value:
        return value
    return int(value) + 1


def clamp(value, value_min=None, value_max=None):
    if value_max is not None and value > value_max:
        return value_max
    if value_min is not None and value < value_min:
        return value_min
    return value


def clamp01(value):
    if value < 0:
        return 0
    if value > 1:
        return 1
    return value


def radians(value):
    return glm.radians(value)


def sin(*args, **kwargs):
    return np.sin(*args, **kwargs)


def cos(*args, **kwargs):
    return np.cos(*args, **kwargs)


def tan(*args, **kwargs):
    return np.tan(*args, **kwargs)


def lerp(begin, end, value):
    value = clamp(value, 0, 1)
    return begin + (end - begin) * value
