import unittest
from OpenGLEngine.DefaultModel import *


class TestDefaultModelTest(unittest.TestCase):
    def test_vs_maker(self):
        test_vs = GLSL.GLSL_maker.get_vs('VTN', three_dimensional=True)
        self.assertEqual(test_vs, '''#version 330 core
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
        self.assertIsInstance(GLSL.GLSL_maker.get_fs(), str)


if __name__ == '__main__':
    unittest.main()
