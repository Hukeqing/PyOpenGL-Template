import glm
import numpy as np


def clamp(value, value_min, value_max):
    if value_max is not None and value > value_max:
        return value_max
    if value_min is not None and value < value_min:
        return value_min
    return value


def radians(value):
    return glm.radians(value)


def sin(*args, **kwargs):
    return np.sin(*args, **kwargs)


def cos(*args, **kwargs):
    return np.cos(*args, **kwargs)


def tan(*args, **kwargs):
    return np.tan(*args, **kwargs)
