import unittest

from example_with_longer_name import example_f


class ExampleWithLongerNameTest(unittest.TestCase):
    def test_sanity(self):
        self.assertIs(example_f(), True)
