import unittest


from example_has_stdout import hello


class ExampleHasStdoutTest(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Hello, World!")

    def test_abc(self):
        self.assertEqual(hello(), "Hello, World!")


class ExampleHasStdoutOtherTest(unittest.TestCase):
    def test_dummy(self):
        self.assertEqual(hello(), "Hello, World!")

    def test_hello(self):
        self.assertEqual(hello(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
