def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def calculate(a, b):
    result = add(a, b)

    for i in range(3):
        result = multiply(result, 2)

    return result