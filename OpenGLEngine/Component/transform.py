import glm
import numpy as np

from OpenGLEngine.Component.component_manager import ComponentManager
from OpenGLEngine.Class import *


class Transform(ComponentManager):
    def __init__(self, game_object, position=None, rotation=None, scale=None):
        super(Transform, self).__init__(game_object)
        self.position = position
        self.rotation = rotation
        self.scale = scale

        if self.position is None:
            self.position = glm.vec3(0, 0, 0)
        elif isinstance(self.position, Vector3):
            self.position = glm.vec3(self.position.get_value())
        else:
            self.position = glm.vec3(*self.position)

        if self.rotation is None:
            self.rotation = glm.vec3(0, 0, 0)
        elif isinstance(self.rotation, Vector3):
            self.rotation = glm.vec3(self.rotation.get_value())
        else:
            self.rotation = glm.vec3(*self.rotation)

        if self.scale is None:
            self.scale = glm.vec3(1, 1, 1)
        elif isinstance(self.scale, Vector3):
            self.scale = glm.vec3(self.scale.get_value())
        else:
            self.scale = glm.vec3(*self.scale)

        self.glm_forward = None
        self.glm_left = None
        self.glm_up = None
        self.forward = None
        self.left = None
        self.up = None
        self.get_forward()

        self.position_lock_alive = (False, False, False)
        self.position_lock_x = None
        self.position_lock_y = None
        self.position_lock_z = None

        self.rotation_lock_alive = (False, False, False)
        self.rotation_lock_x = None
        self.rotation_lock_y = None
        self.rotation_lock_z = None

    def set_position_clock(self, x_clock=None, y_clock=None, z_clock=None):
        self.position_lock_alive = (x_clock, y_clock, z_clock)
        self.position_lock_x = x_clock
        self.position_lock_y = y_clock
        self.position_lock_z = z_clock

    def set_rotation_clock(self, x_clock=None, y_clock=None, z_clock=None):
        self.rotation_lock_alive = (x_clock, y_clock, z_clock)
        self.rotation_lock_x = x_clock
        self.rotation_lock_y = y_clock
        self.rotation_lock_z = z_clock

    def translate(self, vector3):
        self.position += vector3
        self.position_clock()

    def rotate(self, vector3):
        self.rotation += vector3
        self.rotation_lock()
        self.get_forward()

    def position_clock(self):
        if self.position_lock_alive[0]:
            self.position.x = math_f.clamp(self.position.x, *self.position_lock_x)
        if self.position_lock_alive[1]:
            self.position.y = math_f.clamp(self.position.y, *self.position_lock_y)
        if self.position_lock_alive[2]:
            self.position.z = math_f.clamp(self.position.z, *self.position_lock_z)

    def rotation_lock(self):
        if self.rotation_lock_alive[0]:
            self.rotation.x = math_f.clamp(self.rotation.x, *self.rotation_lock_x)
        if self.rotation_lock_alive[1]:
            self.rotation.y = math_f.clamp(self.rotation.y, *self.rotation_lock_y)
        if self.rotation_lock_alive[2]:
            self.rotation.z = math_f.clamp(self.rotation.z, *self.rotation_lock_z)

    def get_forward(self):
        self.glm_forward = glm.vec3(0)
        self.glm_forward.x = -np.sin(glm.radians(self.rotation.y))
        self.glm_forward.y = np.sin(glm.radians(self.rotation.x))
        self.glm_forward.z = np.cos(glm.radians(self.rotation.x)) * np.cos(glm.radians(self.rotation.y))
        # self.forward.x = np.cos(glm.radians(self.rotation.x)) * np.cos(glm.radians(self.rotation.y))
        # self.forward.y = np.sin(glm.radians(self.rotation.x))
        # self.forward.z = np.cos(glm.radians(self.rotation.x)) * np.sin(glm.radians(self.rotation.y))

        self.glm_forward = glm.normalize(self.glm_forward)
        self.glm_left = glm.normalize(glm.cross(glm.vec3(0, 1, 0), self.glm_forward))
        self.glm_up = glm.normalize(glm.cross(self.glm_forward, self.glm_left))

        self.forward = Vector3(self.glm_forward)
        self.left = Vector3(self.glm_left)
        self.up = Vector3(self.glm_up)

    def get_view_matrix(self):
        self.get_forward()
        return glm.lookAt(self.position, self.position + self.glm_forward, self.glm_up)
