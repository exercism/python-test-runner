"""Example Exercism/Python tests file"""
import unittest


from example import hello


class ExampleTest(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), 'Hello, World!')

    def test_abc(self):
        self.assertIs(True, True)


class ABCTest(unittest.TestCase):
    def test_dummy(self):
        pass

    def test_hello(self):
        pass


if __name__ == '__main__':
    unittest.main()
