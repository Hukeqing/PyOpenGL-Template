import glm
from OpenGLEngine.Component.component_manager import ComponentManager
from OpenGLEngine.Component.transform import Transform
from OpenGLEngine.Component.game_object import GameObject
from OpenGLEngine.Class import *
from typing import Optional, Union, Callable, List, Tuple


class Camera(ComponentManager):
    def __init__(self,
                 game_object: GameObject,
                 window: Union[Tuple[int, int], List[int]],
                 zoom: int = 45,
                 near: int = 0.3,
                 far: int = 1000):
        super(Camera, self).__init__(game_object)
        self.window_width = window[0]
        self.window_height = window[1]
        self.zoom = zoom
        self.range = (near, far)

        self.zoom_in_clock_alive = False
        self.zoom_in_clock_value = None

        self.projection = None
        self.get_projection()

    def set_zoom_in_clock(self, zoom_in: Optional[int] = None):
        self.zoom_in_clock_alive = zoom_in is not None
        self.zoom_in_clock_value = zoom_in

    def get_projection(self):
        self.projection = glm.perspective(math_f.radians(self.zoom), self.window_width * 1.0 / self.window_height, *self.range)

    def get_view_matrix(self):
        return self.get_component(Transform).get_view_matrix()

    def zoom_in(self, size: int):
        self.zoom -= size
        self.zoom_in_clock()
        self.get_projection()

    def zoom_in_clock(self):
        if self.zoom_in_clock_alive:
            self.zoom = math_f.clamp(self.zoom, *self.zoom_in_clock_value)


class OrthogonalCamera(ComponentManager):
    def __init__(self,
                 game_object: GameObject,
                 left: int,
                 right: int,
                 bottom: int,
                 up: int,
                 near: float = 0.3,
                 far: float = 1000):
        super(OrthogonalCamera, self).__init__(game_object)
        self.size = (left, right, bottom, up)
        self.range = (near, far)
        self.projection = None
        self.get_projection()

    def get_projection(self):
        self.projection = glm.ortho(*self.size, *self.range)
