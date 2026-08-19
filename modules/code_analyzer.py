import ast


def analyze_code(code):

    try:
        tree = ast.parse(code)

    except SyntaxError as e:

        return {
            "valid": False,
            "error": str(e)
        }

    functions = 0
    classes = 0
    loops = 0
    conditions = 0
    imports = 0
    function_calls = 0
    returns = 0

    for node in ast.walk(tree):

        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            functions += 1

        elif isinstance(node, ast.ClassDef):
            classes += 1

        elif isinstance(
            node,
            (ast.For, ast.While)
        ):
            loops += 1

        elif isinstance(
            node,
            (ast.If, ast.IfExp)
        ):
            conditions += 1

        elif isinstance(
            node,
            (ast.Import, ast.ImportFrom)
        ):
            imports += 1

        elif isinstance(node, ast.Call):
            function_calls += 1

        elif isinstance(node, ast.Return):
            returns += 1

    return {
        "valid": True,
        "functions": functions,
        "classes": classes,
        "loops": loops,
        "conditions": conditions,
        "imports": imports,
        "function_calls": function_calls,
        "returns": returns
    }