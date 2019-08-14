from OpenGL.GL import *
from ctypes import c_float, c_void_p, sizeof
import numpy as np
import PIL.Image as Image
import glm


class vertices_pattern:
    """
    V 为坐标点，C 为颜色，T 为纹理坐标
    """
    pattern_type = 'VCT'

    def __init__(self, pattern):
        self.types = list()
        self.numbers = list()
        self.offset = list()
        self.count = 0
        if not isinstance(pattern, str):
            raise ValueError('Pattern Error: "' + pattern + '" is not a str')
        if len(pattern) % 2 != 0 or len(pattern) <= 0:
            raise ValueError('Pattern Error: the lenth of "' + pattern + '" is not a positive even number!')
        for index in range(0, len(pattern), 2):
            if not pattern[index] in vertices_pattern.pattern_type:
                raise ValueError('Unknown type: ' + pattern[index])
            self.types.append(pattern[index])
            self.numbers.append(int(pattern[index + 1]))
            self.offset.append(self.numbers[0] if index == 0 else (self.numbers[-1] + self.offset[-1]))
            self.count += int(pattern[index + 1])


class uniform_array_pattern:
    pattern_array_type = ['d', 'dv', 'f', 'fv', 'i', 'iv', 'u', 'uv']

    def __init__(self, pattern, variable_name, *variable_value):
        if pattern[1:] in uniform_array_pattern.pattern_array_type:
            self.uniform_function = eval('glUniform' + pattern)
            self.variable_name = variable_name
            self.variable_value = variable_value
        else:
            raise ValueError('Unknown type: ' + pattern)

    def uniform(self, shader_program):
        if len(self.variable_value) == 1:
            self.uniform_function(glGetUniformLocation(shader_program, self.variable_name), self.variable_value[0])
        elif len(self.variable_value) == 2:
            self.uniform_function(glGetUniformLocation(shader_program, self.variable_name), self.variable_value[0], self.variable_value[1])
        elif len(self.variable_value) == 3:
            self.uniform_function(glGetUniformLocation(shader_program, self.variable_name), self.variable_value[0], self.variable_value[1],
                                  self.variable_value[2])
        elif len(self.variable_value) == 4:
            self.uniform_function(glGetUniformLocation(shader_program, self.variable_name), self.variable_value[0], self.variable_value[1],
                                  self.variable_value[2], self.variable_value[3])


class Mesh:
    def __init__(self, vertices, shader_program, vertex_format=None, indices=None, draw_type=GL_POINT, texture_path=None):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.shader_program = shader_program
        self.vertex_format = vertex_format
        if indices is not None:
            self.indices = np.array(indices, dtype=np.int32)
        else:
            self.indices = None
        self.draw_type = draw_type
        self.texture_path = texture_path

        self.vao = None
        self.ebo = None
        self.texture = None
        self.init_data()

    def init_data(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)
        if self.indices is not None:
            self.ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)
        if self.vertex_format is None:
            self.vertex_format = vertices_pattern('V3')
        # 链接顶点属性
        for index, cur_type in enumerate(self.vertex_format.types):
            glVertexAttribPointer(index, self.vertex_format.numbers[index], GL_FLOAT, False, self.vertex_format.count * sizeof(c_float),
                                  c_void_p((0 if index == 0 else self.vertex_format.offset[index - 1]) * sizeof(c_float)))
            glEnableVertexAttribArray(index)
        if self.texture_path is not None:
            self.load_texture()

    def load_texture(self):
        if self.texture_path is not None:
            if isinstance(self.texture_path, list):
                self.texture = [Mesh.open_texture(path) for path in self.texture_path]
            else:
                self.texture = [Mesh.open_texture(self.texture_path)]

    def draw(self, *args):
        self.shader_program.use()
        if self.texture is not None:
            for index, item in enumerate(self.texture):
                glUniform1i(glGetUniformLocation(self.shader_program.shader_program, "texture" + str(index)), index)
                glActiveTexture(GL_TEXTURE0 + index)
                glBindTexture(GL_TEXTURE_2D, item)
        glBindVertexArray(self.vao)
        for uniform_value in args:
            uniform_value.uniform(self.shader_program)
        if self.ebo is not None:
            glDrawElements(self.draw_type, len(self.indices), GL_UNSIGNED_INT, None)
        else:
            glDrawArrays(self.draw_type, 0, len(self.vertices) // self.vertex_format.count)
        glBindVertexArray(0)

    @staticmethod
    def open_texture(texture_path):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        try:
            img = Image.open(texture_path)
        except FileNotFoundError:
            print('\33[31mFile load fail: ' + texture_path + '\33[0m')
            exit(-1)
        else:
            try:
                imgx, imgy, images = img.size[0], img.size[1], img.tobytes("raw", "RGBA", 0, -1)
            except:
                imgx, imgy, images = img.size[0], img.size[1], img.tobytes("raw", "RGBX", 0, -1)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imgx, imgy, 0, GL_RGBA, GL_UNSIGNED_BYTE, images)
            glGenerateMipmap(GL_TEXTURE_2D)
            return texture
