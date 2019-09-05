import unittest

from OpenGLEngine.Test import *


class Test0_UnitTest(unittest.TestCase):
    def test_test(self):
        self.assertEqual(test(), 'Import all test')


if __name__ == '__main__':
    unittest.main(verbosity=2)
