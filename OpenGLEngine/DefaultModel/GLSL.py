import os
from OpenGLEngine.Function.math_f import *


class vs_maker:
    def __init__(self, vertex_format='V', three_dimensional=True):
        self.data = '#version 330 core\n'
        self.vertex_format = vertex_format.upper()
        self.three_dimensional = three_dimensional
        self.init_data()

    def init_data(self):
        for index, ch in enumerate(self.vertex_format):
            self.data += 'layout (location = ' + str(index) + ') in '
            if ch == 'V':
                self.data += 'vec3 aPos;\n'
            elif ch == 'T':
                self.data += 'vec2 aTexCoord;\n'
            elif ch == 'N':
                self.data += 'vec3 aNormal;\n'

        self.data += '\n'
        self.data += 'out vec2 TexCoord;\nout vec3 FragPos;\nout vec3 Normal;\n\n'
        if self.three_dimensional:
            self.data += 'uniform mat4 model;\nuniform mat4 view;\nuniform mat4 projection;\n\n'

        # main
        self.data += 'void main()\n{\n'
        if self.three_dimensional:
            self.data += '\tgl_Position = projection * view * model * vec4(aPos, 1.0);\n'
        else:
            self.data += '\tgl_Position = vec4(aPos, 1.0);\n'
        if 'T' in self.vertex_format:
            self.data += '\tTexCoord = aTexCoord;\n'
        else:
            self.data += '\tTexCoord = vec2(0);'
        if 'N' in self.vertex_format:
            self.data += '\tFragPos = vec3(model * vec4(aPos, 1.0));\n\tNormal = mat3(transpose(inverse(model))) * aNormal;\n'
        else:
            self.data += '\tFragPos = vec3(0);\n\tNormal = vec3(0);\n'
        self.data += '}\n'


class GLSL_maker:
    no_light_fs: str = None
    light_fs: str = None
    set_max_texture_number = 14
    set_max_dir_light_number = 2
    set_max_point_light_number = 10
    set_max_spot_lights = 5

    @staticmethod
    def init_data():
        fs_path = os.path.dirname(__file__)
        try:
            with open(os.path.join(fs_path, 'no_light_fs.fs'), 'r') as f:
                GLSL_maker.no_light_fs = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("fs Shader file: light_fs.fs open error!")
        try:
            with open(os.path.join(fs_path, 'light_fs.fs'), 'r') as f:
                GLSL_maker.light_fs = f.read().replace('___set_max_dir_light_number', str(GLSL_maker.set_max_dir_light_number)).replace(
                    '___set_max_point_light_number', str(GLSL_maker.set_max_point_light_number)).replace('___set_max_spot_lights',
                                                                                                         str(GLSL_maker.set_max_spot_lights))
        except FileNotFoundError:
            raise FileNotFoundError("fs Shader file: light_fs.fs open error!")

    @staticmethod
    def get_fs(use_light: bool = True, set_texture_number: int = 14):
        set_texture_number = clamp(set_texture_number, 0, GLSL_maker.set_max_texture_number)
        if GLSL_maker.light_fs is None:
            GLSL_maker.init_data()
        if use_light:
            return GLSL_maker.light_fs.replace('___set_texture_number', str(set_texture_number))
        else:
            return GLSL_maker.no_light_fs.replace('___set_texture_number', str(set_texture_number))

    @staticmethod
    def get_vs(vertex_format: str = 'V', three_dimensional=True):
        return vs_maker(vertex_format=vertex_format, three_dimensional=three_dimensional).data


if __name__ == '__main__':
    print(GLSL_maker.get_fs())
