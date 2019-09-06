from OpenGLEngine.Built_inClass import *
from OpenGL.GL import *
from PIL import Image
from typing import Optional, List, Tuple, Union


class Texture:
    def __init__(self, texture_path: str):
        self.texture_path = texture_path
        self.texture = self.open_texture()

    def open_texture(self):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        try:
            img = Image.open(self.texture_path)
        except FileNotFoundError:
            print('\33[31mFile load fail: ' + self.texture_path + '\33[0m')
            exit(-1)
        else:
            try:
                img_x, img_y, image = img.size[0], img.size[1], img.tobytes("raw", "RGBA", 0, -1)
            except:
                img_x, img_y, image = img.size[0], img.size[1], img.tobytes("raw", "RGBX", 0, -1)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_x, img_y, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
            glGenerateMipmap(GL_TEXTURE_2D)
            return texture


class Material:

    def __init__(self, color: Color, shininess: float, textures: Optional[List[Tuple[str, float]]] = None, diffuse: Optional[str] = None,
                 specular: Optional[str] = None):
        self.color = color
        self.shininess = shininess
        self.textures = textures
        if self.textures is not None:
            # TODO... a /= (a + b); b /= (a + b)
            self.textures = [(Texture(texture_path=item[0]), item[1]) for item in textures]
        self.diffuse = diffuse
        if self.diffuse is not None:
            self.diffuse = Texture(texture_path=self.diffuse)
        self.specular = specular
        if self.specular is not None:
            self.specular = Texture(texture_path=self.specular)

    def renderer(self, shader_program):
        # material
        glUniform4f(glGetUniformLocation(shader_program, 'material.color'), *self.color.get_value())
        glUniform1f(glGetUniformLocation(shader_program, 'material.shininess'), self.shininess)

        # texture
        glUniform1i(glGetUniformLocation(shader_program, 'material.texture_number'), len(self.textures))
        for index, item in enumerate(self.textures):
            glUniform1f(glGetUniformLocation(shader_program, 'material.textures[' + str(index) + '].mix_value'), item[1])
            glUniform1i(glGetUniformLocation(shader_program, 'material.textures[' + str(index) + '].texture_index'), index + 2)
            glActiveTexture(GL_TEXTURE0 + index + 2)
            glBindTexture(GL_TEXTURE_2D, item[0].texture)
        # diffuse and specular
        if self.diffuse is not None or self.specular is not None:
            glUniform1i(glGetUniformLocation(shader_program, 'material.useSampler'), 1)

            if self.diffuse is not None:
                glUniform1i(glGetUniformLocation(shader_program, 'material.diffuse'), 0)
                glActiveTexture(GL_TEXTURE0 + 0)
                glBindTexture(GL_TEXTURE_2D, self.diffuse.texture)
            else:
                glUniform1i(glGetUniformLocation(shader_program, 'material.diffuse'), 0)
                glActiveTexture(GL_TEXTURE0 + 0)
                glBindTexture(GL_TEXTURE_2D, self.specular.texture)

            if self.specular is not None:
                glUniform1i(glGetUniformLocation(shader_program, 'material.specular'), 1)
                glActiveTexture(GL_TEXTURE0 + 1)
                glBindTexture(GL_TEXTURE_2D, self.specular.texture)
            else:
                glUniform1i(glGetUniformLocation(shader_program, 'material.specular'), 1)
                glActiveTexture(GL_TEXTURE0 + 1)
                glBindTexture(GL_TEXTURE_2D, self.diffuse.specular)

        else:
            glUniform1i(glGetUniformLocation(shader_program, 'material.useSampler'), 0)


DefaultMaterial = Material(color=DefaultColor.white, shininess=5)
