import glm
import numpy as np

from OpenGLEngine.Component import mathF
from OpenGLEngine.Component.component_manager import Component_Manager


class Transform(Component_Manager):
    def __init__(self, game_object, position=glm.vec3(0, 0, 0), rotation=glm.vec3(0, 0, 0), scale=glm.vec3(1, 1, 1)):
        super(Transform, self).__init__(game_object)
        self.position = position
        self.rotation = rotation
        self.scale = scale

        self.forward = None
        self.up = None
        self.right = None
        self.get_forward()

        self.position_lock_alive = glm.vec3(False, False, False)
        self.position_lock_x = None
        self.position_lock_y = None
        self.position_lock_z = None

        self.rotation_lock_alive = glm.vec3(False, False, False)
        self.rotation_lock_x = None
        self.rotation_lock_y = None
        self.rotation_lock_z = None

    def set_position_clock(self, x_clock=None, y_clock=None, z_clock=None):
        self.position_lock_alive = glm.vec3(x_clock is not None, y_clock is not None, z_clock is not None)
        self.position_lock_x = x_clock
        self.position_lock_y = y_clock
        self.position_lock_z = z_clock

    def set_rotation_clock(self, x_clock=None, y_clock=None, z_clock=None):
        self.rotation_lock_alive = glm.vec3(x_clock is not None, y_clock is not None, z_clock is not None)
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
            self.position.x = mathF.clamp(self.position.x, *self.position_lock_x)
        if self.position_lock_alive[1]:
            self.position.y = mathF.clamp(self.position.y, *self.position_lock_y)
        if self.position_lock_alive[2]:
            self.position.z = mathF.clamp(self.position.z, *self.position_lock_z)

    def rotation_lock(self):
        if self.rotation_lock_alive[0]:
            self.rotation.x = mathF.clamp(self.rotation.x, *self.rotation_lock_x)
        if self.rotation_lock_alive[1]:
            self.rotation.y = mathF.clamp(self.rotation.y, *self.rotation_lock_y)
        if self.rotation_lock_alive[2]:
            self.rotation.z = mathF.clamp(self.rotation.z, *self.rotation_lock_z)

    def get_forward(self):
        self.forward = glm.vec3(0)
        self.forward.x = -np.sin(glm.radians(self.rotation.y))
        self.forward.y = np.sin(glm.radians(self.rotation.x))
        self.forward.z = np.cos(glm.radians(self.rotation.x)) * np.cos(glm.radians(self.rotation.y))
        self.forward = glm.normalize(self.forward)
        self.right = -glm.normalize(glm.cross(glm.vec3(0, 1, 0), self.forward))
        self.up = -glm.normalize(glm.cross(self.forward, self.right))

    def get_view_matrix(self):
        self.get_forward()
        return glm.lookAt(self.position, self.position + self.forward, self.up)
