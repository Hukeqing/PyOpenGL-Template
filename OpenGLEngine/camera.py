import glm
import numpy as np


class Camera:
    def __init__(self, window, position=glm.vec3(0, 0, 0), rotation=glm.vec3(0, 0, 0), zoom=45, near=0.3, far=1000, move_speed=1, rotate_speed=60):
        self.window_width = window.width
        self.window_height = window.height
        self.position = position
        self.rotation = rotation
        self.zoom = zoom
        self.near = near
        self.far = far

        self.forward = None
        self.up = None
        self.right = None
        self.get_forward()

        self.move_speed = move_speed
        self.rotate_speed = rotate_speed

        self.projection = None
        self.get_perspective()

    def get_perspective(self):
        self.projection = glm.perspective(glm.radians(self.zoom), self.window_width * 1.0 / self.window_height, 0.1, 1000)

    def get_view_matrix(self):
        self.get_forward()
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def translate(self, vector3):
        self.position += vector3 * self.move_speed

    def rotate(self, vector3):
        self.rotation += vector3 * self.rotate_speed

    def rotation_lock(self):
        pass

    def get_forward(self):
        self.rotation_lock()
        self.forward = glm.vec3(0)
        self.forward.x = -np.sin(glm.radians(self.rotation.y))
        self.forward.y = np.sin(glm.radians(self.rotation.x))
        self.forward.z = np.cos(glm.radians(self.rotation.x)) * np.cos(glm.radians(self.rotation.y))
        self.forward = glm.normalize(self.forward)
        self.right = -glm.normalize(glm.cross(glm.vec3(0, 1, 0), self.forward))
        self.up = -glm.normalize(glm.cross(self.forward, self.right))
