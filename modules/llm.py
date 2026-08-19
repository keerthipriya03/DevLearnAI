import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


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
{code}
```
Return ONLY valid JSON using exactly this structure:

{{
    "summary": "string",

    "issues": [
        {{
            "title": "string",
            "description": "string",
            "severity": "Low/Medium/High"
        }}
    ],

    "improvements": [
        {{
            "title": "string",
            "description": "string"
        }}
    ],

    "time_complexity": {{
        "value": "string",
        "explanation": "string"
    }},

    "space_complexity": {{
        "value": "string",
        "explanation": "string"
    }},

    "concepts": [
        "string"
    ],

    "learning_explanation": "string",

    "improved_code": "string"
}}

Rules:

- Return only JSON.
- Do not use Markdown.
- Do not add headings outside the JSON.
- Do not invent bugs.
- If there are no major issues, return an empty issues list.
- The improved_code must contain valid Python code.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    try:
        return json.loads(response.text)

    except json.JSONDecodeError:
        return {
            "error": "The AI returned an invalid response format.",
            "raw_response": response.text
        }


# python -m py_compile modules/llm.py           (to check the syntax of the code)