from typing import Optional

from OpenGL.GL import *

from OpenGLEngine.Built_inClass.color import Color
from OpenGLEngine.Built_inClass.vector_matrix import Vector3
from OpenGLEngine.Built_inClass.math_f import *
from OpenGLEngine.Component.component_manager import ComponentManager
from OpenGLEngine.Component.game_object import GameObject
from OpenGLEngine.Component.light import Light
from OpenGLEngine.Component.point_light import PointLight
import glm


class SpotLight(PointLight):
    def __init__(self,
                 game_object: GameObject,
                 cut_off: float = glm.cos(glm.radians(12.5)),
                 outer_cut_off: float = glm.cos(glm.radians(15.0)),
                 light_range: float = 50,
                 ambient: float = 0.1,
                 diffuse: float = 0.5,
                 specular: float = 0.5,
                 color: Optional[Color] = None):
        super(SpotLight, self).__init__(game_object=game_object, light_range=light_range, ambient=ambient, diffuse=diffuse, specular=specular,
                                        color=color)
        self.direction: Vector3 = game_object.transform.forward
        self.cut_off: float = cut_off
        self.outer_cut_off: float = outer_cut_off

    def renderer(self, shader_program, variable_name: str):
        glUniform3f(glGetUniformLocation(shader_program, variable_name + '.direction'), *self.direction)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.cutOff'), self.cut_off)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.outerCutOff'), self.outer_cut_off)
        super(SpotLight, self).renderer(shader_program=shader_program, variable_name=variable_name)
