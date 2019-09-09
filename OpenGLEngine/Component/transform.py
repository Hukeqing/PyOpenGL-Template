from OpenGLEngine.Component.component_manager import ComponentManager
from OpenGLEngine.Built_inClass import *
from typing import Optional


class Transform(ComponentManager):
    def __init__(self,
                 game_object,
                 position: Optional[Vector3] = None,
                 rotation: Optional[Vector3] = None,
                 scale: Optional[Vector3] = None):
        super(Transform, self).__init__(game_object)
        self.position = Vector3(0, 0, 0) if position is None else position
        self.rotation = Vector3(0, 0, 0) if rotation is None else rotation
        self.scale = Vector3(0, 0, 0) if scale is None else scale

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
        self.forward = Vector3(0)
        self.forward.x = -math_f.sin(math_f.radians(self.rotation.y))
        self.forward.y = math_f.sin(math_f.radians(self.rotation.x))
        self.forward.z = math_f.cos(math_f.radians(self.rotation.x)) * math_f.cos(math_f.radians(self.rotation.y))
        # self.forward.x = np.cos(glm.radians(self.rotation.x)) * np.cos(glm.radians(self.rotation.y))
        # self.forward.y = np.sin(glm.radians(self.rotation.x))
        # self.forward.z = np.cos(glm.radians(self.rotation.x)) * np.sin(glm.radians(self.rotation.y))

        self.forward = Vector3.normalize(self.forward)
        self.left = Vector3.normalize(Vector3.cross(Vector3(0, 1, 0), self.forward))
        self.up = Vector3.normalize(Vector3.cross(self.forward, self.left))

    def get_view_matrix(self):
        self.get_forward()
        return Vector3.lookAt(self.position, self.position + self.forward, self.up)
