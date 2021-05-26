"""Example Exercism/Python solution file"""


def hello(param):
    if isinstance(param, int):
        return ("Hello, World!")
    else:
        return ("Hello, World!", param)

