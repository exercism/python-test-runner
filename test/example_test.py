import unittest


from example import hello


class ExampleTest(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), 'Hello, World!')


if __name__ == '__main__':
    unittest.main()
