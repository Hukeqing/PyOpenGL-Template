from typing import Optional

from OpenGL.GL import *

from OpenGLEngine.Built_inClass.color import Color
from OpenGLEngine.Built_inClass.vector_matrix import Vector3
from OpenGLEngine.Built_inClass.math_f import *
from OpenGLEngine.Component.component_manager import ComponentManager
from OpenGLEngine.Component.game_object import GameObject
from OpenGLEngine.Component.light import Light


class PointLight(ComponentManager, Light):
    ogre3D = {7: (1.0, 0.7, 1.8),
              13: (1.0, 0.35, 0.44),
              20: (1.0, 0.22, 0.20),
              32: (1.0, 0.14, 0.07),
              50: (1.0, 0.09, 0.032),
              65: (1.0, 0.07, 0.017),
              100: (1.0, 0.045, 0.0075),
              160: (1.0, 0.027, 0.0028),
              200: (1.0, 0.022, 0.0019),
              325: (1.0, 0.014, 0.0007),
              600: (1.0, 0.007, 0.0002),
              3250: (1.0, 0.0014, 0.000007)}

    def __init__(self,
                 game_object: GameObject,
                 light_range: float = 50,
                 ambient: float = 0.1,
                 diffuse: float = 0.5,
                 specular: float = 0.5,
                 color: Optional[Color] = None):
        super(PointLight, self).__init__(game_object)
        super(ComponentManager, self).__init__(ambient=ambient, diffuse=diffuse, specular=specular, color=color)
        self.position: Vector3 = game_object.transform.position
        self.range = clamp(light_range, 7, 3250)
        for dist, value in PointLight.ogre3D.items():
            if dist >= self.range:
                self.constant, self.linear, self.quadratic = value
                break
        self.light: Light = Light(ambient=ambient, diffuse=diffuse, specular=specular, color=color)

    def renderer(self, shader_program, variable_name: str):
        glUniform3f(glGetUniformLocation(shader_program, variable_name + '.position'), *self.position)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.constant'), self.constant)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.linear'), self.linear)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.quadratic'), self.quadratic)
        super(ComponentManager, self).renderer(shader_program=shader_program, variable_name=variable_name)
