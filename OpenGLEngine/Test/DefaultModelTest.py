import unittest
from OpenGLEngine.DefaultModel import *


class TestDefaultModelTest(unittest.TestCase):
    def test_vs_maker(self):
        self.assertIsInstance(GLSL.GLSL_maker.get_vs(), str)

    def test_fs_maker(self):
        self.assertIsInstance(GLSL.GLSL_maker.get_fs(), str)


if __name__ == '__main__':
    unittest.main()
