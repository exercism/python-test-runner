import unittest


from example_partial_fail import hello


class ExamplePartialFailTest(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Goodbye")

    def test_abc(self):
        self.assertEqual(hello(), "Hello, World!")


class ExamplePartialFailOtherTest(unittest.TestCase):
    def test_dummy(self):
        self.assertEqual(hello(), "Goodbye")

    def test_hello(self):
        self.assertEqual(hello(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
