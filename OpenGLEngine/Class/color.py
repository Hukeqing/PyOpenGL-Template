class Color:
    def __init__(self, r=1, g=1, b=1, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        if self.r > 1 or self.g > 1 or self.b > 1 or self.a > 1:
            self.mode = True
        else:
            self.mode = False

    def get_value(self):
        if self.mode:
            return self.r / 255, self.g / 255, self.b / 255, self.a / 255
        else:
            return self.r, self.g, self.b, self.a


class DefaultColor:
    white = Color(1, 1, 1, 1)
    black = Color(0, 0, 0, 1)
    red = Color(1, 0, 0, 1)
    green = Color(0, 1, 0, 1)
    blue = Color(0, 0, 1, 0)
