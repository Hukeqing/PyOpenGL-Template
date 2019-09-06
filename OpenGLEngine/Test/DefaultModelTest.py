import unittest
from OpenGLEngine.DefaultModel import *


class TestDefaultModelTest(unittest.TestCase):
    def test_vs_maker(self):
        test_vs = GLSL.vs_maker('VTN', three_dimensional=True)
        self.assertEqual(test_vs.data, '''#version 330 core
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
\tgl_Position = projection * view * model * vec4(aPos, 1.0);
\tTexCoord = aTexCoord;
\tFragPos = vec3(model * vec4(aPos, 1.0));
\tNormal = mat3(transpose(inverse(model))) * aNormal;
}
''')

    def test_fs_maker(self):
        test_fs = GLSL.fs_maker(2, True)
        self.assertEqual(test_fs.data, '''#version 330 core\n
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
};\n
uniform Material material;\n
in vec2 TexCoord;
uniform sampler2D texture;
uniform Texture texture0;
in vec3 FragPos;
in vec3 Normal;
uniform vec3 viewPos;
uniform Light light;\n
void main()
{
\t// ambient
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
\tvec3 result = (ambient + diffuse + specular) * vec3(material.color.xyz);\n
\tFragColor = mix(texture(texture, TexCoord), texture(texture0.texture, TexCoord), texture0.mix_value) * vec4(result, material.color.w);
}\n''')


if __name__ == '__main__':
    unittest.main()
