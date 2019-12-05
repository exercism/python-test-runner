"""Example Exercism/Python tests file"""
import unittest


from example import hello


class ExampleTest(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), 'Hello, World!')

    def test_abc(self):
        self.assertIs(True, True)


if __name__ == '__main__':
    unittest.main()
