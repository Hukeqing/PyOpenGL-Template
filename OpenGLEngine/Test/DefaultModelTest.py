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
in vec2 TexCoord;
in vec3 FragPos;
in vec3 Normal;\n
uniform vec4 basecolor;
uniform float ambientStrength = 0.1;
uniform float specularStrength = 0.5;
uniform int shininess = 5;\n
uniform sampler2D texture0;
uniform sampler2D texture1;
uniform float mix_value0;\n
uniform vec3 viewPos=vec3(0, 0, 0);
uniform vec4 lightColor0;
uniform vec3 lightPos0;\n
void main()
{
\tvec3 ambient = ambientStrength * vec3(lightColor0.xyz);\n
\tvec3 norm = normalize(Normal);
\tvec3 lightDir = normalize(lightPos0 - FragPos);
\tfloat diff = max(dot(norm, lightDir), 0.0);
\tvec3 diffuse = diff * vec3(lightColor0.xyz);\n
\tvec3 viewDir = normalize(viewPos - FragPos);
\tvec3 reflectDir = reflect(-lightDir, norm);
\tfloat spec = pow(max(dot(viewDir, reflectDir), 0.0), (1 << shininess));
\tvec3 specular = specularStrength * spec * vec3(lightColor0.xyz);\n
\tvec3 result = (ambient + diffuse + specular) * vec3(basecolor.xyz);\n
\tFragColor = mix(texture(texture0, TexCoord), texture(texture1, TexCoord), mix_value0) * vec4(result, basecolor.w);
}
''')


if __name__ == '__main__':
    unittest.main()
