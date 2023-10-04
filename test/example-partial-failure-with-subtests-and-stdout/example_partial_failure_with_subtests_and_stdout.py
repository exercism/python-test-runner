"""This example code is adapted from a student example that can be
found here on our Discord server:
https://discord.com/channels/854117591135027261/1145433700054601759

It is pulled from the "Meltdown Mitigation" concept exercise for Python.

Two issues came out of the example.
1.  The subtest "u" representing failed subtests.
    (see these lines of code in the pytest-subtests plugin for why that is being inserted:
    https://github.com/pytest-dev/pytest-subtests/blob/main/src/pytest_subtests.py#L306-L308)

2.  The dumping of the stdout of subtests into the parent test.
    See issue https://github.com/exercism/python-test-runner/issues/67 for more details.

The fix is a reverse-engineer that parses the
parent output and places it in each subtest report output field.

This was to avoid having to patch the pytest-subtests plugin or
import it into our test runner plugin to override it.

This test case ensures that the reverse-engineering works for cases where not all
failing subtests have output.
"""

def is_criticality_balanced(temperature, neutrons_emitted):

    if temperature < 800 and neutrons_emitted > 500 and temperature * neutrons_emitted < 500000:
        return True
    elif temperature > 800 and neutrons_emitted < 500 and temperature * neutrons_emitted > 500000:
        print(temperature)
        return False
    else:
        return False


def reactor_efficiency(voltage, current, theoretical_max_power):
    generated_power = voltage * current
    percentage_value = (generated_power / theoretical_max_power) * 100

    if percentage_value < percentage_value:
        print('green')
    elif 30 < percentage_value <= 60:
        print('orange')
    elif percentage_value > 60 and percentage_value <= 30:
        print('red')
    elif percentage_value < 30:
        print('black')


def fail_safe(temperature, neutrons_produced_per_second, threshold):
    """Assess and return status code for the reactor.

    :param temperature: int or float - value of the temperature in kelvin.
    :param neutrons_produced_per_second: int or float - neutron flux.
    :param threshold: int or float - threshold for category.
    :return: str - one of ('LOW', 'NORMAL', 'DANGER').

    1. 'LOW' -> `temperature * neutrons per second` < 90% of `threshold`
    2. 'NORMAL' -> `temperature * neutrons per second` +/- 10% of `threshold`
    3. 'DANGER' -> `temperature * neutrons per second` is not in the above-stated ranges
    """

    print('Ouptut Captured!!')
    print("""Id donec ultrices tincidunt arcu non. Semper feugiat nibh sed pulvinar proin gravida hendrerit. Odio ut sem nulla pharetra. Venenatis urna cursus eget nunc scelerisque viverra mauris in. Suscipit adipiscing bibendum est ultricies integer quis. Vel elit scelerisque mauris pellentesque pulvinar. Quam nulla porttitor massa id neque aliquam vestibulum morbi blandit. Ac felis donec et odio pellentesque diam. Vitae tortor condimentum lacinia quis. Enim lobortis scelerisque fermentum dui faucibus in ornare quam. Dolor sit amet consectetur adipiscing elit duis tristique sollicitudin. Orci dapibus ultrices in iaculis nunc. Magna etiam tempor orci eu. Gravida in fermentum et sollicitudin ac orci phasellus egestas tellus. Amet nisl purus in mollis nunc sed. Odio ut sem nulla pharetra diam sit amet. Mi tempus imperdiet nulla malesuada pellentesque elit. Vulputate mi sit amet mauris. Feugiat vivamus at augue eget. Et leo duis ut diam quam nulla porttitor massa. Tincidunt lobortis feugiat vivamus at.""")

