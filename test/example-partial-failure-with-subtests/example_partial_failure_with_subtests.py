"""Example Exercism/Python solution file"""


def hello(param):
    if isinstance(param, int):
        print("User output is captured!")
        return ("Hello, World!")
    else:
        print("User output is captured!")
        return ("Hello, World!", param)

