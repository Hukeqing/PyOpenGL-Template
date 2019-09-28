from typing import Optional

from OpenGL.GL import *

from OpenGLEngine.Class.color import Color
from OpenGLEngine.Class.vector_matrix import Vector3
from OpenGLEngine.Component.component_manager import ComponentManager
from OpenGLEngine.Component.game_object import GameObject
from OpenGLEngine.Component.light import Light


class DirectionLight(ComponentManager, Light):
    def __init__(self,
                 game_object: GameObject,
                 ambient: Optional[float] = None,
                 diffuse: Optional[float] = None,
                 specular: Optional[float] = None,
                 color: Optional[Color] = None):
        super(DirectionLight, self).__init__(game_object)
        super(ComponentManager, self).__init__(ambient=ambient, diffuse=diffuse, specular=specular, color=color)
        self.direction: Vector3 = game_object.transform.forward

    def renderer(self, shader_program, variable_name: str):
        glUniform3f(glGetUniformLocation(shader_program, variable_name + '.direction'), *self.direction)
        super(ComponentManager, self).renderer(shader_program=shader_program, variable_name=variable_name)
