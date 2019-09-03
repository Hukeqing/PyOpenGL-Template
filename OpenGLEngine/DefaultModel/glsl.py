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


class fs_maker:
    def __init__(self, texture_number=0, light=True):
        self.data = '#version 330 core\n\nout vec4 FragColor;\n\n'
        self.texture_number = texture_number
        self.light = light
        self.init_data()

    def init_data(self):
        if self.texture_number > 0:
            self.data += 'in vec2 TexCoord;\n'
        if self.light:
            self.data += 'in vec3 FragPos;\nin vec3 Normal;\n'
        self.data += '\nuniform vec4 basecolor;\n\n'
        for index in range(self.texture_number):
            self.data += 'uniform sampler2D texture' + str(index) + ';\n'
        for index in range(self.texture_number - 1):
            self.data += 'uniform float mix_value' + str(index) + ';\n'
        self.data += '\n'
        if self.light:
            self.data += 'uniform vec4 lightColor0;\nuniform vec3 lightPos0;\n\n'
        # main
        self.data += 'void main()\n{\n'
        if self.light:
            self.data += '''\tfloat ambientStrength = 0.1;
\tvec3 ambient = ambientStrength * vec3(lightColor0.xyz);\n
\tvec3 norm = normalize(Normal);
\tvec3 lightDir = normalize(lightPos0 - FragPos);
\tfloat diff = max(dot(norm, lightDir), 0.0);
\tvec3 diffuse = diff * vec3(lightColor0.xyz);\n
\tvec3 result = (ambient + diffuse) * vec3(basecolor.xyz);\n'''
        else:
            self.data += '\tvec3 result = vec3(basecolor.xyz);\n'

        if self.texture_number == 0:
            self.data += '\tFragColor = vec4(result, basecolor.w);\n'
        elif self.texture_number == 1:
            self.data += '\tFragColor = texture(texture0, TexCoord) * vec4(result, basecolor.w);\n'
        else:
            texture_value = fs_maker.texture_make(0)
            for index in range(self.texture_number - 1):
                texture_value = fs_maker.mix_make(texture_value, fs_maker.texture_make(index + 1), index)
            self.data += '\tFragColor = ' + texture_value + ' * vec4(result, basecolor.w);\n'
        self.data += '}\n'

    @staticmethod
    def mix_make(a, b, value):
        return 'mix(' + a + ', ' + b + ', mix_value' + str(value) + ')'

    @staticmethod
    def texture_make(index):
        return 'texture(texture' + str(index) + ', TexCoord)'


def vs_test():
    test_vs = vs_maker('VTN', three_dimensional=True)
    test_fs = fs_maker(2, True)
    print('\33[32mOK\33[0m' if test_vs.data == '''#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec3 aNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 TexCoord;

out vec3 FragPos;
out vec3 Normal;

void main()
{
	gl_Position = projection * view * model * vec4(aPos, 1.0);
	TexCoord = aTexCoord;
	FragPos = vec3(model * vec4(aPos, 1.0));
	Normal = mat3(transpose(inverse(model))) * aNormal;
}
''' else '\33[31mTest on glsl.py Error: vs_maker\33[0m')
    print('\33[32mOK\33[0m' if test_fs.data == '''#version 330 core\n
out vec4 FragColor;\n
in vec2 TexCoord;
in vec3 FragPos;
in vec3 Normal;\n
uniform vec4 basecolor;\n
uniform sampler2D texture0;
uniform sampler2D texture1;
uniform float mix_value0;\n
uniform vec4 lightColor0;
uniform vec3 lightPos0;\n
void main()
{
\tfloat ambientStrength = 0.1;
\tvec3 ambient = ambientStrength * vec3(lightColor0.xyz);\n
\tvec3 norm = normalize(Normal);
\tvec3 lightDir = normalize(lightPos0 - FragPos);
\tfloat diff = max(dot(norm, lightDir), 0.0);
\tvec3 diffuse = diff * vec3(lightColor0.xyz);\n
\tvec3 result = (ambient + diffuse) * vec3(basecolor.xyz);
\tFragColor = mix(texture(texture0, TexCoord), texture(texture1, TexCoord), mix_value0) * vec4(result, basecolor.w);
}
''' else '\33[31mTest on glsl.py Error: fs_maker\33[0m')


if __name__ == '__main__':
    vs_test()
