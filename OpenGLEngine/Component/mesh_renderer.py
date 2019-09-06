from OpenGL.GL import *
from PIL import Image

from OpenGLEngine.Class.material import DefaultMaterial, Material
from OpenGLEngine.Component.component_manager import ComponentManager


class MeshRenderer(ComponentManager):
    """
    Texture renderer * base color
    """

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

    def __init__(self, game_object, vertex_shader, fragment_shader, material: Material = DefaultMaterial, texture_path=None,
                 texture_mix_value=None, check=True):
        super(MeshRenderer, self).__init__(game_object)
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        self.shader_program = glCreateProgram()
        self.check_error = check
        self.init_data()

        self.material = material
        self.texture = list()
        self.texture_mix_value = list()
        if isinstance(texture_path, list):
            for item in texture_path:
                self.add_texture(item)
        elif isinstance(texture_path, str):
            self.add_texture(texture_path)
        if isinstance(texture_mix_value, list):
            self.texture_mix_value.extend(texture_mix_value)
        elif isinstance(texture_mix_value, float):
            self.texture_mix_value.append(texture_mix_value)
        if (not (len(self.texture_mix_value) == len(self.texture) == 0)) and (len(self.texture_mix_value) + 1 != len(self.texture)):
            raise ValueError(
                'The lenth of texture_mix_value and texture_path must satisfy this:\nlen(self.texture_mix_value) + 1 == len(self.texture)')

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

    def add_texture(self, new_texture_path):
        self.texture.append(self.Texture(new_texture_path))

    def change_texture(self, index, new_texture_path):
        if index >= len(self.texture):
            raise IndexError('The index:' + str(index) + 'is out of range.(the lenth of texture is:' + str(len(self.texture)) + ')')
        self.texture[index] = self.Texture(new_texture_path)

    def del_texture(self, index):
        if index >= len(self.texture):
            raise IndexError('The index:' + str(index) + 'is out of range.(the lenth of texture is:' + str(len(self.texture)) + ')')
        del self.texture[index]

    def set_color(self, new_color):
        self.material = new_color

    def set_matrix(self, uniform_name, value, transpose=GL_FALSE):
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, uniform_name), 1, transpose, value)

    def use(self):
        glUseProgram(self.shader_program)

    def draw(self, light_view):
        self.use()
        # material
        glUniform4f(glGetUniformLocation(self.shader_program, 'material.color'), *self.material.color.get_value())
        glUniform1f(glGetUniformLocation(self.shader_program, 'material.ambientStrength'), self.material.ambientStrength)
        glUniform1f(glGetUniformLocation(self.shader_program, 'material.specularStrength'), self.material.specular_strength)
        glUniform1i(glGetUniformLocation(self.shader_program, 'material.shininess'), self.material.shininess)
        # texture
        if len(self.texture) > 0:
            glUniform1i(glGetUniformLocation(self.shader_program, 'texture'), 0)
            for index, item in enumerate(self.texture):
                glUniform1i(glGetUniformLocation(self.shader_program, 'texture' + str(index - 1) + '.texture'), index)
                glActiveTexture(GL_TEXTURE0 + index)
                glBindTexture(GL_TEXTURE_2D, item.texture)
        for index, item in enumerate(self.texture_mix_value):
            glUniform1f(glGetUniformLocation(self.shader_program, 'texture' + str(index) + '.mix_value'), item)
        # light
        if light_view is not None:
            glUniform3f(glGetUniformLocation(self.shader_program, 'light.position'), *(light_view[0]))
            glUniform4f(glGetUniformLocation(self.shader_program, 'light.color'), *(light_view[1].get_value()))
            glUniform3f(glGetUniformLocation(self.shader_program, 'viewPos'), *(light_view[2]))

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
