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
        self.data = """#version 330 core

in vec2 TexCoord;
in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

struct Texture {
    sampler2D texture_index;
    float mix_value;
};

struct Material {
    vec4 color;
    float shininess;
    sampler2D diffuse;
    sampler2D specular;
    int useSampler;

    int texture_number;
    Texture textures[14];
};

struct TestureMaterial {
	vec3 diffuseVec3;
	vec3 specularVec3;
};

struct DirLight {
    vec3 direction;

    float ambient;
    float diffuse;
    float specular;
    vec3 color;
};

struct PointLight {
    vec3 position;

    float constant;
    float linear;
    float quadratic;

    float ambient;
    float diffuse;
    float specular;
    vec3 color;
};

struct SpotLight {
    vec3 position;
    vec3 direction;
    float cutOff;
    float outerCutOff;

    float constant;
    float linear;
    float quadratic;

    float ambient;
    float diffuse;
    float specular;
    vec3 color;
};

uniform Material material;
uniform vec3 viewPos;
TestureMaterial texture_material;

uniform int dirLight_number;
uniform DirLight dirLights[2];

uniform int pointLight_number;
uniform PointLight pointLights[10];

uniform int spotLight_number;
uniform SpotLight spotLights[5];

// function prototypes
vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir);

vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir);

vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir);

void main() {
    // properties
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);
    if (material.useSampler > 0) {
        texture_material.diffuseVec3 = vec3(texture(material.diffuse, TexCoord));
        texture_material.specularVec3 = vec3(texture(material.specular, TexCoord));
    } else {
        texture_material.diffuseVec3 = vec3(1.0);
        texture_material.specularVec3 = vec3(1.0);
    }
    // ========================================================
    // lighting is set up in 3 phases: directional, point lights and an optional flashlight
    // For each phase, a calculate function is defined that calculates the corresponding color
    // per lamp. In the main() function we take all the calculated colors and sum them up for
    // this fragment's final color.
    // ========================================================
    // phase 1: directional lighting
    vec3 result = vec3(0, 0, 0);
    for (int i = 0; i < dirLight_number; i++)
        result += CalcDirLight(dirLights[i], norm, viewDir) * dirLights[i].color;
    // phase 2: point lights
    for (int i = 0; i < pointLight_number; i++)
        result += CalcPointLight(pointLights[i], norm, FragPos, viewDir) * pointLights[i].color;
    // phase 3: spot light
    for (int i = 0; i < spotLight_number; i++)
        result += CalcSpotLight(spotLights[i], norm, FragPos, viewDir) * spotLights[i].color;

    // texture mix
    vec4 texture_result = vec4(1.0);
    if (material.texture_number > 0) {
        texture_result = texture(material.textures[0].texture_index, TexCoord);
        for (int i = 1; i < material.texture_number; i++)
            texture_result = mix(texture_result, texture(material.textures[i].texture_index, TexCoord), material.textures[i].mix_value);
    }
    FragColor = vec4(result * vec3(material.color.xyz), material.color.w) * texture_result;
}

// calculates the color when using a directional light.
vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir) {
    vec3 lightDir = normalize(-light.direction);
    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    // combine results
    vec3 ambient = light.ambient * texture_material.diffuseVec3;
    vec3 diffuse = light.diffuse * diff * texture_material.diffuseVec3;
    vec3 specular = light.specular * spec * texture_material.specularVec3;
    return (ambient + diffuse + specular);
}

// calculates the color when using a point light.
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir) {
    vec3 lightDir = normalize(light.position - fragPos);
    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    // attenuation
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));
    // combine results
    vec3 ambient = light.ambient * texture_material.diffuseVec3;
    vec3 diffuse = light.diffuse * diff * texture_material.diffuseVec3;
    vec3 specular = light.specular * spec * texture_material.specularVec3;
    ambient *= attenuation;
    diffuse *= attenuation;
    specular *= attenuation;
    return (ambient + diffuse + specular);
}

// calculates the color when using a spot light.
vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir) {
    vec3 lightDir = normalize(light.position - fragPos);
    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    // attenuation
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));
    // spotlight intensity
    float theta = dot(lightDir, normalize(-light.direction));
    float epsilon = light.cutOff - light.outerCutOff;
    float intensity = clamp((theta - light.outerCutOff) / epsilon, 0.0, 1.0);
    // combine results
    vec3 ambient = light.ambient * texture_material.diffuseVec3;
    vec3 diffuse = light.diffuse * diff * texture_material.diffuseVec3;
    vec3 specular = light.specular * spec * texture_material.specularVec3;
    ambient *= attenuation * intensity;
    diffuse *= attenuation * intensity;
    specular *= attenuation * intensity;
    return (ambient + diffuse + specular);
}"""

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
    test = fs_maker(2, True)
    print(test.get_data())
