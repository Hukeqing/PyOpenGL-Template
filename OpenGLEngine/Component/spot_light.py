from typing import Optional

import glm
from OpenGL.GL import *

from OpenGLEngine.Class.color import Color
from OpenGLEngine.Class.vector_matrix import Vector3
from OpenGLEngine.Component.game_object import GameObject
from OpenGLEngine.Component.point_light import PointLight


class SpotLight(PointLight):
    def __init__(self,
                 game_object: GameObject,
                 cut_off: Optional[float] = None,
                 outer_cut_off: Optional[float] = None,
                 light_range: Optional[float] = None,
                 ambient: Optional[float] = None,
                 diffuse: Optional[float] = None,
                 specular: Optional[float] = None,
                 color: Optional[Color] = None):
        super(SpotLight, self).__init__(game_object=game_object, light_range=light_range, ambient=ambient, diffuse=diffuse, specular=specular,
                                        color=color)
        self.direction: Vector3 = game_object.transform.forward
        self.cut_off: float = glm.cos(glm.radians(12.5)) if cut_off is None else glm.cos(glm.radians(cut_off))
        self.outer_cut_off: float = glm.cos(glm.radians(15.0)) if outer_cut_off is None else glm.cos(glm.radians(outer_cut_off))

    def renderer(self, shader_program, variable_name: str):
        glUniform3f(glGetUniformLocation(shader_program, variable_name + '.direction'), *self.direction)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.cutOff'), self.cut_off)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.outerCutOff'), self.outer_cut_off)
        super(SpotLight, self).renderer(shader_program=shader_program, variable_name=variable_name)
