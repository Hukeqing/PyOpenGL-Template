import os


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
        if self.three_dimensional:
            self.data += 'uniform mat4 model;\nuniform mat4 view;\nuniform mat4 projection;\n\n'

        if 'T' in self.vertex_format:
            self.data += 'out vec2 TexCoord;\n\n'
        if self.three_dimensional:
            self.data += 'out vec3 FragPos;\nout vec3 Normal;\n\n'

        # main
        self.data += 'void main()\n{\n'
        if self.three_dimensional:
            self.data += '\tgl_Position = projection * view * model * vec4(aPos, 1.0);\n'
        else:
            self.data += '\tgl_Position = vec4(aPos, 1.0);\n'
        if 'T' in self.vertex_format:
            self.data += '\tTexCoord = aTexCoord;\n'
        if 'N' in self.vertex_format:
            self.data += '\tFragPos = vec3(model * vec4(aPos, 1.0));\n\tNormal = mat3(transpose(inverse(model))) * aNormal;\n'

        self.data += '}\n'


class GLSL_maker:
    fs_path = os.path.dirname(__file__)
    try:
        with open(os.path.join(fs_path, 'no_light_fs.fs'), 'r') as f:
            no_light_fs = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("fs Shader file: light_fs.fs open error!")
    try:
        with open(os.path.join(fs_path, 'light_fs.fs'), 'r') as f:
            light_fs = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("fs Shader file: light_fs.fs open error!")

    @staticmethod
    def get_fs(use_light: bool = True):
        if use_light:
            return GLSL_maker.light_fs
        else:
            return GLSL_maker.no_light_fs

    @staticmethod
    def get_vs(vertex_format: str = 'V', three_dimensional=True):
        return vs_maker(vertex_format=vertex_format, three_dimensional=three_dimensional).data


if __name__ == '__main__':
    print(GLSL_maker.get_fs())
