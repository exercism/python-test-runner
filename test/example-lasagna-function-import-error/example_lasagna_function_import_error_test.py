import unittest
import pytest

# For this first exercise, it is really important to be clear about how we are importing names for tests.
# To that end, we are putting a try/catch around imports and throwing specific messages to help students
# decode that they need to create and title their constants and functions in a specific way.
try:
    from example_lasagna_function_import_error import (EXPECTED_BAKE_TIME,
                         bake_time_remaining,
                         preparation_time_in_minutes,
                         elapsed_time_in_minutes)

# Here, we are separating the constant import errors from the function name import errors
except ImportError as import_fail:
    message = import_fail.args[0].split('(', maxsplit=1)
    item_name = import_fail.args[0].split()[3]

    if 'EXPECTED_BAKE_TIME' in item_name:
        # pylint: disable=raise-missing-from
        raise ImportError(f'\n\nMISSING CONSTANT --> \nWe can not find or import the constant {item_name} in your'
                          " 'lasagna.py' file.\nDid you misname or forget to define it?") from None
    else:
        item_name = item_name[:-1] + "()'"
        # pylint: disable=raise-missing-from
        raise ImportError("\n\nMISSING FUNCTION --> In your 'lasagna.py' file, we can not find or import the"
                          f' function named {item_name}. \nDid you misname or forget to define it?') from None
