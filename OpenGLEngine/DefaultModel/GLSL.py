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
    fs_base = '''#version 330 core\n
out vec4 FragColor;\n
struct Material {
\tvec4 color;
\tfloat ambientStrength;
\tfloat specularStrength;
\tint shininess;
};\n
struct Light {
\tvec4 color;
\tvec3 position;
};\n
struct Texture {
\tsampler2D texture;
\tfloat mix_value;
};

uniform Material material;
'''
    fs_texture_base = '''in vec2 TexCoord;
uniform sampler2D texture;'''
    fs_light_base = '''in vec3 FragPos;
in vec3 Normal;
uniform vec3 viewPos;
uniform Light light;
'''
    fs_light_main = '''\t// ambient
\tvec3 ambient = material.ambientStrength * vec3(light.color.xyz);\n
\t// diffuse
\tvec3 norm = normalize(Normal);
\tvec3 lightDir = normalize(light.position - FragPos);
\tfloat diff = max(dot(norm, lightDir), 0.0);
\tvec3 diffuse = diff * vec3(light.color.xyz);\n
\t// specular
\tvec3 viewDir = normalize(viewPos - FragPos);
\tvec3 reflectDir = reflect(-lightDir, norm);
\tfloat spec = pow(max(dot(viewDir, reflectDir), 0.0), (1 << material.shininess));
\tvec3 specular = material.specularStrength * spec * vec3(light.color.xyz);\n
\t// Phong Shading result
\tvec3 result = (ambient + diffuse + specular) * vec3(material.color.xyz);
'''

    def __init__(self, texture_number=0, light=True):
        self.data = fs_maker.fs_base
        self.texture_number = texture_number
        self.light = light
        self.init_data()

    def init_data(self):
        self.init_variable()
        self.add_code('void main()\n{')
        self.init_main()
        self.add_code('}\n')

    def add_code(self, code: str, indent: int = 0):
        self.data += '\n' + ('\t' * indent) + code

    def init_variable(self):
        if self.texture_number > 0:
            self.add_code(fs_maker.fs_texture_base, indent=0)
            for index in range(self.texture_number - 1):
                self.add_code('uniform Texture texture' + str(index) + ';', indent=0)
        if self.light:
            self.add_code(fs_maker.fs_light_base, indent=0)

    def init_main(self):
        if self.light:
            self.add_code(fs_maker.fs_light_main, 0)
        else:
            self.add_code('vec3 result = vec3(material.color.xyz);', 1)
        if self.texture_number == 0:
            self.add_code('FragColor = vec4(result, material.color.w);', 1)
        elif self.texture_number == 1:
            self.add_code('FragColor = texture(texture, TexCoord) * vec4(result, material.color.w);', 1)
        else:
            texture_value = 'texture(texture, TexCoord)'
            for index in range(self.texture_number - 1):
                texture_value = fs_maker.mix_make(texture_value, fs_maker.texture_make(index), index)
            texture_value = 'FragColor = ' + texture_value + ' * vec4(result, material.color.w);'
            self.add_code(texture_value, 1)

    def get_data(self):
        return self.data

    @staticmethod
    def mix_make(a, b, value):
        return 'mix(' + a + ', ' + b + ', texture' + str(value) + '.mix_value)'

    @staticmethod
    def texture_make(index):
        return 'texture(texture' + str(index) + '.texture, TexCoord)'


if __name__ == '__main__':
    test = fs_maker(0, False)
    print(test.get_data())
