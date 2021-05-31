import unittest
import pytest


from example_with_config import hello


class ExampleFirstTest(unittest.TestCase):

    @pytest.mark.task(taskno=1)
    def test_hello(self):
        self.assertEqual(hello('Hi'), ("Hello, World!", 'Hi'))

    @pytest.mark.task(taskno=1)
    def test_abc(self):
        self.assertEqual(hello(13), ("Hello, World!", 13))


class ExampleFirstOtherTest(unittest.TestCase):

    @pytest.mark.task(taskno=2)
    def test_dummy(self):
        self.assertEqual(hello('Banana'), ("Hello, World!", "Banana"))

    @pytest.mark.task(taskno=2)
    def test_hello(self):
        self.assertEqual(hello(42), ("Hello, World!", 42))


if __name__ == "__main__":
    unittest.main()
