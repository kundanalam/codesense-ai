import ast

BLOCKED_MODULES = {"os", "sys", "subprocess", "socket", "shutil", "pathlib",
                   "requests", "urllib", "http", "ctypes", "importlib",
                   "multiprocessing", "threading", "signal", "builtins"}
BLOCKED_CALLS = {"open", "exec", "eval", "compile", "__import__",
                 "globals", "locals", "getattr", "setattr", "breakpoint"}


def unsafe_reason(code):
    """Return a short reason if the code looks unsafe, else None."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None          # syntax errors are reported normally
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in BLOCKED_MODULES:
                    return "importing '%s'" % a.name
        if isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in BLOCKED_MODULES:
                return "importing from '%s'" % node.module
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in BLOCKED_CALLS):
            return "using '%s'" % node.func.id
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            return "using '%s'" % node.attr
    return None


def blocked_diagnosis(reason, problem_id=None):
    return {
        "problem_id": problem_id, "status": "runtime_error",
        "error_type": "blocked_for_safety", "line": None, "confidence": 1.0,
        "explanation": "This tutor does not run code that is " + reason
                       + ". Remove it and try again.",
        "minimal_failing_input": None, "expected_output": None,
        "actual_output": None, "hints": [],
    }