import glm
import math


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get_value(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        res = Vector3(self.x, self.y, self.z)
        if isinstance(other, int) or isinstance(other, float):
            res.x += other
            res.y += other
            res.z += other
        elif isinstance(other, Vector3):
            res.x += other.x
            res.y += other.y
            res.z += other.z
        elif isinstance(other, glm.vec3):
            res.x += other.x
            res.y += other.y
            res.z += other.z
            print('error!!!!')
        else:
            raise TypeError('unsupported operand type(s) for +: "Vector3" and "' + type(other) + '"')
        return res

    def __sub__(self, other):
        res = Vector3(self.x, self.y, self.z)
        if isinstance(other, int) or isinstance(other, float):
            res.x -= other
            res.y -= other
            res.z -= other
        elif isinstance(other, Vector3):
            res.x -= other.x
            res.y -= other.y
            res.z -= other.z
        else:
            raise TypeError('unsupported operand type(s) for -: "Vector3" and "' + type(other) + '"')
        return res

    def __mul__(self, other):
        res = Vector3(self.x, self.y, self.z)
        if isinstance(other, int) or isinstance(other, float):
            res.x *= other
            res.y *= other
            res.z *= other
        else:
            raise TypeError('unsupported operand type(s) for *: "Vector3" and "' + type(other) + '"')
        return res

    def __truediv__(self, other):
        res = Vector3(self.x, self.y, self.z)
        if isinstance(other, int) or isinstance(other, float):
            res.x /= other
            res.y /= other
            res.z /= other
        else:
            raise TypeError('unsupported operand type(s) for /: "Vector3" and "' + type(other) + '"')
        return res

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __iadd__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x += other
            self.y += other
            self.z += other
        elif isinstance(other, Vector3):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        else:
            raise TypeError('unsupported operand type(s) for +: "Vector3" and "' + type(other) + '"')

    def __isub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x -= other
            self.y -= other
            self.z -= other
        elif isinstance(other, Vector3):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        else:
            raise TypeError('unsupported operand type(s) for -: "Vector3" and "' + type(other) + '"')

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise TypeError('unsupported operand type(s) for *: "Vector3" and "' + type(other) + '"')

    def __itruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
            self.z /= other
        else:
            raise TypeError('unsupported operand type(s) for /: "Vector3" and "' + type(other) + '"')

    def __neg__(self):
        res = Vector3(self.x, self.y, self.z)
        res.x = -res.x
        res.y = -res.y
        res.z = -res.z
        return res

    def __abs__(self):
        res = Vector3(self.x, self.y, self.z)
        res.x = abs(res.x)
        res.y = abs(res.y)
        res.z = abs(res.z)
        return res

    @staticmethod
    def normalize(value):
        res = Vector3(value.x, value.y, value.z)
        lenth = math.sqrt(res.x * res.x + res.y * res.y + res.z * res.z)
        res.x /= lenth
        res.y /= lenth
        res.z /= lenth
        return res

    @staticmethod
    def cross(a, b):
        res = Vector3()
        res.x = a.y * b.z - a.z * b.y
        res.y = a.z * b.x - a.x * b.z
        res.z = a.x * b.y - a.y * b.x
        return res
