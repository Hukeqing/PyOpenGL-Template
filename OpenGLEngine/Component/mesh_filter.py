from OpenGL.GL import *
from ctypes import c_float, c_void_p, sizeof
import numpy as np
from OpenGLEngine.Component.component_manager import Component_Manager


class vertices_pattern:
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


class MeshFilter(Component_Manager):
    def __init__(self, game_object, vertices, vertex_format=None, indices=None, draw_type=GL_POINT):
        super(MeshFilter, self).__init__(game_object)
        self.vertices = np.array(vertices, dtype=np.float32)
        self.vertex_format = vertex_format
        if indices is not None:
            self.indices = np.array(indices, dtype=np.int32)
        else:
            self.indices = None
        self.draw_type = draw_type

        self.vao = None
        self.ebo = None
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

    def draw(self):
        glBindVertexArray(self.vao)
        if self.ebo is not None:
            glDrawElements(self.draw_type, len(self.indices), GL_UNSIGNED_INT, None)
        else:
            glDrawArrays(self.draw_type, 0, len(self.vertices) // self.vertex_format.count)
        glBindVertexArray(0)
