from typing import Optional, List, Tuple, Union

from OpenGL.GL import *
from PIL import Image

from OpenGLEngine.Built_inClass import *


class TextureWrapping:
    repeat = GL_REPEAT
    mirrored_repeat = GL_MIRRORED_REPEAT
    clamp_to_edge = GL_CLAMP_TO_EDGE
    clamp_to_border = GL_CLAMP_TO_BORDER


class Texture:
    def __init__(self, texture_path: str,
                 texture_wrapping_filtering=None):
        self.texture_path = texture_path
        self.texture_wrapping_filtering = [1] if texture_wrapping_filtering is None else texture_wrapping_filtering
        self.texture_wrapping_filtering = list(texture_wrapping_filtering)
        del self.texture_wrapping_filtering[0]
        if len(self.texture_wrapping_filtering) == 0:
            self.texture_wrapping_filtering.append((GL_REPEAT, GL_REPEAT))
            self.texture_wrapping_filtering.append((GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR))
        elif len(self.texture_wrapping_filtering) == 1:
            self.texture_wrapping_filtering.append((GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR))

        self.texture = self.open_texture()

    def open_texture(self):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        if self.texture_wrapping_filtering[0][0] == GL_CLAMP_TO_BORDER:
            glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, self.texture_wrapping_filtering[0][1])
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.texture_wrapping_filtering[0][0])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.texture_wrapping_filtering[0][1])

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.texture_wrapping_filtering[1][0])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.texture_wrapping_filtering[1][1])

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
    def __init__(self, color: Color = None,
                 shininess: float = None,
                 textures: Optional[Union[str, tuple, list]] = None,
                 diffuse: Optional[Union[str, tuple, list]] = None,
                 specular: Optional[Union[str, tuple, list]] = None):
        self.color = DefaultColor.white if color is None else color
        self.shininess = 32 if shininess is None else shininess
        if textures is not None:
            if isinstance(textures, str):
                textures = [(textures, 1)]
            self.textures: list = [[Texture(item[0], item[1:]), 0] for item in textures if item[1] > 0]
            textures_value = [item[1] for item in textures if item[1] > 0]
            textures_sum = sum(textures_value)
            textures_value = list(map(lambda x: x / textures_sum, textures_value))
            self.textures[-1][1] = textures_value[-1]
            self.textures[0][1] = textures_value[0]
            index = len(textures_value) - 2
            while index > 0:
                self.textures[index][1] = (textures_value[index] * self.textures[index + 1][1]) / (
                        (1 - self.textures[index + 1][1]) * textures_value[index + 1])
                index -= 1
        else:
            self.textures = None
        self.diffuse = (diffuse, 0) if isinstance(diffuse, str) else diffuse
        if self.diffuse is not None:
            self.diffuse = Texture(self.diffuse[0], self.diffuse[1:])
        self.specular = (specular, 0) if isinstance(specular, str) else specular
        if self.specular is not None:
            self.specular = Texture(self.specular[0], self.specular[1:])

    def renderer(self, shader_program):
        # material
        glUniform4f(glGetUniformLocation(shader_program, 'material.color'), *self.color.get_value())
        glUniform1f(glGetUniformLocation(shader_program, 'material.shininess'), self.shininess)

        # texture
        if self.textures is not None:
            glUniform1i(glGetUniformLocation(shader_program, 'material.texture_number'), len(self.textures))
            for index, item in enumerate(self.textures):
                glUniform1f(glGetUniformLocation(shader_program, 'material.textures[' + str(index) + '].mix_value'), item[1])
                glUniform1i(glGetUniformLocation(shader_program, 'material.textures[' + str(index) + '].texture_index'), index + 2)
                glActiveTexture(GL_TEXTURE0 + index + 2)
                glBindTexture(GL_TEXTURE_2D, item[0].texture)
        # diffuse and specular
        if self.diffuse is not None or self.specular is not None:
            glUniform1i(glGetUniformLocation(shader_program, 'material.useSampler'), True)

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
            glUniform1i(glGetUniformLocation(shader_program, 'material.useSampler'), False)


DefaultMaterial = Material()
