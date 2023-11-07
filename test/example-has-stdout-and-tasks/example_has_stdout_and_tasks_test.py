import unittest
import pytest


from example_has_stdout_and_tasks import hello, must_truncate


class ExampleHasStdoutAndTasksTest(unittest.TestCase):

    @pytest.mark.task(taskno=1)
    def test_hello(self):
        self.assertEqual(hello(), "Hello, World!")

    @pytest.mark.task(taskno=2)
    def test_abc(self):
        self.assertEqual(hello(), "Hello, World!")

    @pytest.mark.task(taskno=3)
    def test_truncation(self):
        self.assertEqual(must_truncate(), "Hello, World!")


class ExampleHasStdoutAndTasksOtherTest(unittest.TestCase):

    @pytest.mark.task(taskno=4)
    def test_dummy(self):
        self.assertEqual(hello(), "Hello, World!")

    @pytest.mark.task(taskno=5)
    def test_hello(self):
        self.assertEqual(hello(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
