import unittest
import pytest


from example_partial_failure_with_subtests import hello


class ExamplePartialFailureWithSubtestsTest(unittest.TestCase):

    @pytest.mark.task(taskno=1)
    def test_hello(self):
        input_data = [1, 2, 5, 10]
        result_data = [("Hello, World!", param) for param in input_data]

        for variant, (param, result) in enumerate(zip(input_data, result_data), start=1):
            with self.subTest(f"variation #{variant}", param=param, result=result):
                self.assertEqual(hello(param), result,
                                 msg=f'Expected: {result} but got something else instead.')

    @pytest.mark.task(taskno=1)
    def test_abc(self):
        input_data = ['frog', 'fish', 'coconut', 'pineapple', 'carrot', 'cucumber', 'grass', 'tree']
        result_data = [("Hello, World!", param) for param in input_data]

        for variant, (param, result) in enumerate(zip(input_data, result_data), start=1):
            with self.subTest(f"variation #{variant}", param=param, result=result):
                self.assertEqual(hello(param), result,
                                 msg=f'Expected: {result} but got something else instead.')

class ExamplePartialFailureWithSubtestsOtherTest(unittest.TestCase):

    @pytest.mark.task(taskno=2)
    def test_dummy(self):
        input_data = ['frog', 'fish', 'coconut', 'pineapple', 'carrot', 'cucumber', 'grass', 'tree']
        result_data = [("Hello, World!", param) for param in input_data]

        for variant, (param, result) in enumerate(zip(input_data, result_data), start=1):
            with self.subTest(f"variation #{variant}", param=param, result=result):
                self.assertEqual(hello(param), result,
                                 msg=f'Expected: {result} but got something else instead.')


    @pytest.mark.task(taskno=2)
    def test_hello(self):
        input_data = [15, 23, 33, 39]
        result_data = [("Hello, World!", param) for param in input_data]

        for variant, (param, result) in enumerate(zip(input_data, result_data), start=1):
            with self.subTest(f"variation #{variant}", param=param, result=result):
                self.assertEqual(hello(param), result,
                                 msg=f'Expected: {result} but got something else instead.')
