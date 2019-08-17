import glm


class Color:
    def __init__(self, r, g, b, a=1):
        self.color = glm.vec4(r, g, b, a)
        if self.color.x > 1 or self.color.y > 1 or self.color.z > 1 or self.color.w > 1:
            self.change_value()

    def change_value(self):
        self.color = glm.vec4(*[value / 255 for value in self.color])

    def set(self, r, g, b, a=1):
        self.color = glm.vec4(r, g, b, a)
        self.change_value()
    

class DefaultColor:
    white = Color(1, 1, 1, 1)
    red = Color(1, 0, 0, 1)
    green = Color(0, 1, 0, 1)
    blue = Color(0, 0, 1, 0)
