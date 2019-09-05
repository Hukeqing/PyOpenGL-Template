import glm


class Data:
    def __init__(self, mode):
        self.mode = mode
        self.function = glm.vec1
        if mode[0] == 'v':
            self.function = eval('glm.vec' + mode[1])
        if mode[0] == 'm':
            self.function = eval('glm.mat' + mode[1:])

    def __call__(self, *args, **kwargs):
        return self.function(*args)

    @staticmethod
    def distance(p0, p1):
        return glm.distance(p0, p1)

    @staticmethod
    def normalize(v):
        return glm.normalize(v)

    @staticmethod
    def cross(v0, v1):
        return glm.cross(v0, v1)

    @staticmethod
    def lookAt(p, v0, v1):
        return glm.lookAt(p, v0, v1)


Vector3 = Data(mode='v3')
Matrix4 = Data(mode='m4')
