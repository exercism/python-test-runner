import unittest
import pytest
from example_partial_failure_with_subtests_and_stdout import (
    is_criticality_balanced,
    reactor_efficiency,
    fail_safe
)


class ExamplePartialFailureWithSubtestsAndStdoutTest(unittest.TestCase):
    """Test cases for Meltdown mitigation exercise.
    """

    @pytest.mark.task(taskno=1)
    def test_is_criticality_balanced_with_passes(self):
        """Testing border cases around typical points.

        T, n == (800, 500), (625, 800), (500, 1000), etc.

        No output should be generated in the test report here, since
        passing subtests are not reported on.

        """

        test_data = ((750, 650, True), (799, 501, True), (500, 600, True),
                     (1000, 800, False), (800, 500, False), (800, 500.01, False),
                     (799.99, 500, False), (500.01, 999.99, False), (625, 800, False),
                     (625.99, 800, False), (625.01, 799.99, False), (799.99, 500.01, True),
                     (624.99, 799.99, True), (500, 1000, False), (500.01, 1000, False),
                     (499.99, 1000, True))

        for variant, data in enumerate(test_data, start=1):
            temp, neutrons_emitted, expected = data
            with self.subTest(f'variation #{variant}', temp=temp, neutrons_emitted=neutrons_emitted, expected=expected):

                # pylint: disable=assignment-from-no-return
                actual_result = is_criticality_balanced(temp, neutrons_emitted)
                failure_message = (f'Expected {expected} but calling is_criticality_balanced(temp={temp}, '
                                   f'neutrons_emitted={neutrons_emitted}) returned {actual_result}.')
                                   # f'with T={temp} and neutrons={neutrons_emitted}')
                self.assertEqual(actual_result, expected, failure_message)

    @pytest.mark.task(taskno=2)
    def test_reactor_efficiency_with_some_subtest_output(self):
        """Partial failure and output in the test report.
        This should happen for:
           - variants 5, 6, 7, 8, 10, 11, and 12.

        No output fields should be present for:
           - the parent or for variations 1, 2, 3, 4, 9 or 13.
        """

        voltage = 10
        theoretical_max_power = 10000

        # The numbers are chosen so that current == 10 x percentage
        test_data = ((1000, 'green'), (999, 'green'), (800, 'green'),
                     (799, 'orange'), (700, 'orange'), (600, 'orange'),
                     (599, 'red'), (560, 'red'), (400, 'red'), (300, 'red'),
                     (299, 'black'), (200, 'black'), (0, 'black'))

        for variant, data in enumerate(test_data, start=1):
            current, expected = data
            with self.subTest(f'variation #{variant}', voltage=voltage, current=current,
                              theoretical_max_power=theoretical_max_power, expected=expected):

                # pylint: disable=assignment-from-no-return
                actual_result = reactor_efficiency(voltage, current, theoretical_max_power)
                failure_message = (f'Expected {expected} as a result, but calling reactor_efficiency(voltage={voltage}, '
                                   f'current={current}, theoretical_max_power={theoretical_max_power}) '
                                   f'returned {actual_result} ')
                                   # f'with voltage={voltage}, current={current}, max_pow={theoretical_max_power}')
                self.assertEqual(actual_result, expected, failure_message)

    @pytest.mark.task(taskno=3)
    def test_fail_safe_with_output_truncation(self):
        """All variations of this should fail and appear in the test report.
           - All variations should have output.
           - All output should have truncation warnings.
        """

        temp = 10
        threshold = 10000
        test_data = ((399, 'LOW'), (300, 'LOW'), (1, 'LOW'),
                     (0, 'LOW'), (901, 'NORMAL'), (1000, 'NORMAL'),
                     (1099, 'NORMAL'), (899, 'LOW'), (700, 'LOW'),
                     (400, 'LOW'), (1101, 'DANGER'), (1200, 'DANGER'))

        for variant, (neutrons_per_second, expected) in enumerate(test_data, start=1):
            with self.subTest(f'variation #{variant}', temp=temp, neutrons_per_second=neutrons_per_second,
                              threshold=threshold, expected=expected):

                # pylint: disable=assignment-from-no-return
                actual_result = fail_safe(temp, neutrons_per_second, threshold)
                failure_message = (f'Expected {expected} but returned {actual_result} with T={temp}, '
                                   f'neutrons={neutrons_per_second}, threshold={threshold}')
                self.assertEqual(actual_result, expected, failure_message)
