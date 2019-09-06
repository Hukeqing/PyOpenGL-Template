from typing import Optional

from OpenGL.GL import *

from OpenGLEngine.Built_inClass.color import Color, DefaultColor


class Light:
    def __init__(self, ambient: float = 0.1, diffuse: float = 0.5, specular: float = 0.5, color: Optional[Color] = None):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.color = color
        if self.color is None:
            self.color = DefaultColor.white

    def renderer(self, shader_program, variable_name: str):
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.ambient'), self.ambient)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.diffuse'), self.diffuse)
        glUniform1f(glGetUniformLocation(shader_program, variable_name + '.specular'), self.specular)
        glUniform3f(glGetUniformLocation(shader_program, variable_name + '.color'), *self.color.get_3_value())
