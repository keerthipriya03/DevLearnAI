# # creating for testing the code(code_analyzer.py)
# from modules.code_analyzer import analyze_code

# # code = """
# # import math
# # def calculate(x):
# #     for i in range(10):
# #         if x > i:
# #             print(x)
# #     return x
# # """

# code = """
# def calculate(x)
#     return x
# """

# result = analyze_code(code)
# print(result)

from modules.code_analyzer import (
    extract_functions,
    get_function_source
)


code = """
def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def calculate(a, b):

    result = add(a, b)

    return multiply(result, 2)
"""


# Test function extraction
result = extract_functions(code)

print("=== FUNCTIONS ===")
print(result)


# Test source extraction
print("\n=== calculate() ===")

function_code = get_function_source(
    code,
    "calculate"
)

print(function_code)