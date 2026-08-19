import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key
)


def generate_code_review(
    code,
    ast_analysis,
    explanation_level
):

    prompt = f"""
You are DevLearn AI, an AI-powered
coding tutor and code review assistant.

Your task is to analyze the given Python code
and help the user understand and improve it.

Explanation level:
{explanation_level}

AST structural analysis:
{ast_analysis}

Source code:

```python
def find_max(numbers):
    maximum = numbers[0]

    for i in range(len(numbers)):
        if numbers[i] > maximum:
            maximum = numbers[i]

    return maximum
```

Provide:

1. SUMMARY
Explain what the code does.
2. POTENTIAL ISSUES
Identify bugs, edge cases, or possible problems.
If there are no obvious issues, say so.
3. CODE EXPLANATION
Explain how the code works.
4. IMPROVEMENTS
Suggest meaningful improvements.
5. TIME COMPLEXITY
Provide the estimated time complexity and explain why.
6. SPACE COMPLEXITY
Provide the estimated space complexity and explain why.
7. CONCEPTS
List the important programming concepts used.
8. LEARNING EXPLANATION
Explain the code according to the selected difficulty level.

Be accurate.
Do not invent bugs that are not supported by the code.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# python -m py_compile modules/llm.py           (to check the syntax of the code)