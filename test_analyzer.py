# creating for testing the code(code_analyzer.py)
from modules.code_analyzer import analyze_code

# code = """
# import math
# def calculate(x):
#     for i in range(10):
#         if x > i:
#             print(x)
#     return x
# """

code = """
def calculate(x)
    return x
"""

result = analyze_code(code)
print(result)