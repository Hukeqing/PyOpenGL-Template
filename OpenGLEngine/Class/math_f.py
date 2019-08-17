def clamp(value, value_min, value_max):
    if value_max is not None and value > value_max:
        return value_max
    if value_min is not None and value < value_min:
        return value_min
    return value
