from modules.llm import generate_code_review


code = """
def find_max(numbers):

    maximum = numbers[0]

    for i in range(len(numbers)):

        if numbers[i] > maximum:
            maximum = numbers[i]

    return maximum
"""


ast_analysis = {
    "valid": True,
    "functions": 1,
    "classes": 0,
    "loops": 1,
    "conditions": 1,
    "imports": 0,
    "function_calls": 2,
    "returns": 1
}


explanation_level = "Beginner"


result = generate_code_review(
    code,
    ast_analysis,
    explanation_level
)


print(type(result))
print(result)