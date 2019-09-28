from typing import Optional

from OpenGL.GL import *

from OpenGLEngine.Class.color import Color, DefaultColor


class Light:
    def __init__(self,
                 ambient: Optional[float] = None,
                 diffuse: Optional[float] = None,
                 specular: Optional[float] = None,
                 color: Optional[Color] = None):
        self.ambient: float = 0.1 if ambient is None else ambient
        self.diffuse = 0.5 if diffuse is None else diffuse
        self.specular = 0.5 if specular is None else specular
        self.color = DefaultColor.white if color is None else color

    def renderer(self, shader_program, variable_name: str):
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.ambient'), self.ambient)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.diffuse'), self.diffuse)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.specular'), self.specular)
        glUniform3f(glGetUniformLocation(shader_program, variable_name + '.color'), *self.color.get_3_value())
