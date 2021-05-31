import unittest
import pytest


from example_with_config import hello


class ExampleSecondTest(unittest.TestCase):

    @pytest.mark.task(taskno=3)
    def test_hello(self):
        input_data = [1, 2, 5]
        result_data = [("Hello, World!", param) for param in input_data]
        number_of_variants = range(1, len(input_data) + 1)

        for variant, param, result in zip(number_of_variants, input_data, result_data):
            with self.subTest(f"variation #{variant}", param=param, result=result):
                self.assertEqual(hello(param), result,
                                 msg=f'Expected: {result} but got something else instead.')

    @pytest.mark.task(taskno=3)
    def test_abc(self):
        input_data = ['carrot', 'cucumber', 'grass', 'tree']
        result_data = [("Hello, World!", param) for param in input_data]
        number_of_variants = range(1, len(input_data) + 1)

        for variant, param, result in zip(number_of_variants, input_data, result_data):
            with self.subTest(f"variation #{variant}", param=param, result=result):
                self.assertEqual(hello(param), result,
                                 msg=f'Expected: {result} but got something else instead.')


class ExampleSecondOtherTest(unittest.TestCase):

    @pytest.mark.task(taskno=4)
    def test_dummy(self):
        input_data = ['frog', 'fish', 'coconut']
        result_data = [("Hello, World!", param) for param in input_data]
        number_of_variants = range(1, len(input_data) + 1)

        for variant, param, result in zip(number_of_variants, input_data, result_data):
            with self.subTest(f"variation #{variant}", param=param, result=result):
                self.assertEqual(hello(param), result,
                                 msg=f'Expected: {result} but got something else instead.')

    @pytest.mark.task(taskno=4)
    def test_hello(self):
        input_data = [23, 33, 39]
        result_data = [("Hello, World!", param) for param in input_data]
        number_of_variants = range(1, len(input_data) + 1)

        for variant, param, result in zip(number_of_variants, input_data, result_data):
            with self.subTest(f"variation #{variant}", param=param, result=result):
                self.assertEqual(hello(param), result,
                                 msg=f'Expected: {result} but got something else instead.')


if __name__ == "__main__":
    unittest.main()
