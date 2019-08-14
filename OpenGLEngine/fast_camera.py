import glm
from OpenGLEngine.Component.mathF import clamp
from OpenGLEngine.Component.gameobject import GameObject


class Camera(GameObject):
    def __init__(self, window, position=glm.vec3(0, 0, 0), rotation=glm.vec3(0, 0, 0), zoom=45, near=0.3, far=1000):
        self.window_width = window.width
        self.window_height = window.height
        super(Camera, self).__init__(position=position, rotation=rotation)
        self.zoom = zoom
        self.near = near
        self.far = far

        self.zoom_in_clock_alive = False
        self.zoom_in_clock_value = None

        self.projection = None
        self.get_perspective()

    def set_zoom_in_clock(self, zoom_in=None):
        self.zoom_in_clock_alive = zoom_in is not None
        self.zoom_in_clock_value = zoom_in

    def get_perspective(self):
        self.projection = glm.perspective(glm.radians(self.zoom), self.window_width * 1.0 / self.window_height, self.near, self.far)

    def get_view_matrix(self):
        return self.transfrom.get_view_matrix()

    def zoom_in(self, size):
        self.zoom -= size
        self.zoom_in_clock()
        self.get_perspective()

    def zoom_in_clock(self):
        if self.zoom_in_clock_alive:
            self.zoom = clamp(self.zoom, *self.zoom_in_clock_value)
