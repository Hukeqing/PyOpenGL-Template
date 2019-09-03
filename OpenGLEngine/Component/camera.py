import glm
from OpenGLEngine.Component.component_manager import ComponentManager
from OpenGLEngine.Component.transform import Transform
from OpenGLEngine.Class import *


class Camera(ComponentManager):
    def __init__(self, game_object, window, zoom=45, near=0.3, far=1000):
        super(Camera, self).__init__(game_object)
        self.window_width = window.width
        self.window_height = window.height
        self.zoom = zoom
        self.near = near
        self.far = far

        self.zoom_in_clock_alive = False
        self.zoom_in_clock_value = None

        self.projection = None
        self.get_projection()

    def set_zoom_in_clock(self, zoom_in=None):
        self.zoom_in_clock_alive = zoom_in is not None
        self.zoom_in_clock_value = zoom_in

    def get_projection(self):
        self.projection = glm.perspective(math_f.radians(self.zoom), self.window_width * 1.0 / self.window_height, self.near, self.far)

    def get_view_matrix(self):
        return self.get_component(Transform).get_view_matrix()

    def zoom_in(self, size):
        self.zoom -= size
        self.zoom_in_clock()
        self.get_projection()

    def zoom_in_clock(self):
        if self.zoom_in_clock_alive:
            self.zoom = math_f.clamp(self.zoom, *self.zoom_in_clock_value)
