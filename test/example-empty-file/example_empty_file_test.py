import unittest


from example_empty_file import hello


class ExampleEmptyFileTest(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Hello, World!")

    def test_abc(self):
        self.assertEqual(hello(), "Hello, World!")


class ExampleEmptyFileOtherTest(unittest.TestCase):
    def test_dummy(self):
        self.assertEqual(hello(), "Hello, World!")

    def test_hello(self):
        self.assertEqual(hello(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
