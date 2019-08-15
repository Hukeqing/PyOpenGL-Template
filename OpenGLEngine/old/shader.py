from OpenGL.GL import *


class ShaderProgram:
    def __init__(self, vertex_shader_path, fragment_shader_path):
        self.vertex_shader_path = vertex_shader_path
        self.fragment_shader_path = fragment_shader_path
        self.shader_program = glCreateProgram()
        self.init_data()

    def init_data(self):
        # vertex shader
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        ShaderProgram.compile_shader(vertex_shader, self.vertex_shader_path)

        # fragment shader
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        ShaderProgram.compile_shader(fragment_shader, self.fragment_shader_path)
        self.link_vertex_fragment_shader(vertex_shader, fragment_shader)

    def link_vertex_fragment_shader(self, vertex, fragment):
        glAttachShader(self.shader_program, vertex)
        glAttachShader(self.shader_program, fragment)
        glLinkProgram(self.shader_program)
        message = glGetProgramInfoLog(self.shader_program)
        print("program link error: ", message) if message else print('program link success')

    def set_matrix(self, uniform_name, value, transpose=GL_FALSE):
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, uniform_name), 1, transpose, value)

    def use(self):
        glUseProgram(self.shader_program)

    @staticmethod
    def un_use():
        glUseProgram(0)

    @staticmethod
    def compile_shader(shader, source):
        glShaderSource(shader, ShaderProgram.load_shader_source(source))
        glCompileShader(shader)
        ShaderProgram.check_shader_error(shader)

    @staticmethod
    def load_shader_source(shader_source):
        try:
            f = open(shader_source, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("Shader file open error!, file name: " + shader_source)
        return f.read()

    @staticmethod
    def check_shader_error(shader_source):
        message = glGetShaderInfoLog(shader_source)
        print("shader compile error: ", message) if message else print('shader compile success')
