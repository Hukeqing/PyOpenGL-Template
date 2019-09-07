from OpenGL.GL import *

from OpenGLEngine.Class.material import DefaultMaterial, Material
from OpenGLEngine.Component.component_manager import ComponentManager


class MeshRenderer(ComponentManager):
    """
    Texture renderer * base color
    """

    def __init__(self,
                 game_object,
                 vertex_shader: str,
                 fragment_shader: str,
                 material: Material = None,
                 check: bool = True):
        super(MeshRenderer, self).__init__(game_object)
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        self.shader_program = glCreateProgram()
        self.check_error = check
        self.init_data()

        self.material = DefaultMaterial if material is None else material

    def init_data(self):
        # vertex shader
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        if self.check_error:
            MeshRenderer.compile_shader(vertex_shader, self.vertex_shader)

        # fragment shader
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        if self.check_error:
            MeshRenderer.compile_shader(fragment_shader, self.fragment_shader)
        self.link_vertex_fragment_shader(vertex_shader, fragment_shader)

    def link_vertex_fragment_shader(self, vertex, fragment):
        glAttachShader(self.shader_program, vertex)
        glAttachShader(self.shader_program, fragment)
        glLinkProgram(self.shader_program)
        message = glGetProgramInfoLog(self.shader_program)
        print(self.game_object.name + "'s program link error: ", message) if message else print(self.game_object.name + "'s program link success")

    def set_matrix(self, uniform_name, value, transpose=GL_FALSE):
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, uniform_name), 1, transpose, value)

    def use(self):
        glUseProgram(self.shader_program)

    def draw(self, light_tuple, view_position):
        self.use()
        glUniform3f(glGetUniformLocation(self.shader_program, 'viewPos'), *view_position)

        # light
        direction_light: list = light_tuple[0]
        point_light: list = light_tuple[1]
        spot_light: list = light_tuple[2]
        glUniform1i(glGetUniformLocation(self.shader_program, 'dirLight_number'), len(direction_light))
        glUniform1i(glGetUniformLocation(self.shader_program, 'pointLight_number'), len(point_light))
        glUniform1i(glGetUniformLocation(self.shader_program, 'spotLight_number'), len(spot_light))
        for index, light in enumerate(direction_light):
            light = light.get_component('DirectionLight')
            light.renderer(shader_program=self.shader_program, variable_name='dirLights[' + str(index) + ']')

        for index, light in enumerate(point_light):
            light = light.get_component('PointLight')
            light.renderer(shader_program=self.shader_program, variable_name='pointLights[' + str(index) + ']')

        for index, light in enumerate(spot_light):
            light = light.get_component('SpotLight')
            light.renderer(shader_program=self.shader_program, variable_name='spotLights[' + str(index) + ']')

        # material
        self.material.renderer(self.shader_program)

    @staticmethod
    def un_use():
        glUseProgram(0)

    @staticmethod
    def compile_shader(shader, shader_code):
        # glShaderSource(shader, MeshRenderer.load_shader_source(source))
        glShaderSource(shader, shader_code)
        glCompileShader(shader)
        # print(shader_code)
        MeshRenderer.check_shader_error(shader)

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
