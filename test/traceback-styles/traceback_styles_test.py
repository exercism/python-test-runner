import unittest


from traceback_styles import hello


class TracebackStylesTest(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Goodbye")


if __name__ == "__main__":
    unittest.main()
