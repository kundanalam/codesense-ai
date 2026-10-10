from backend.problems import PROBLEMS
from backend.detect.sandbox import run_student_code
from backend.detect.ast_rules import find_misconceptions
from backend.detect.fuzz_shrink import find_minimal_failing_input


def analyze(code, problem_id):
    """Run the student's code and return a diagnosis dict."""
    problem = PROBLEMS[problem_id]
    result = run_student_code(code, problem["func"], problem["tests"])

    diagnosis = {
        "problem_id": problem_id,
        "status": result["status"],
        "error_type": None,
        "line": result.get("line"),
        "confidence": 0.0,
        "explanation": "",
        "minimal_failing_input": result.get("failed_input"),
        "expected_output": result.get("expected"),
        "actual_output": result.get("actual", result.get("message")),
    }

    if result["status"] == "correct":
        diagnosis["explanation"] = "Your code passed all tests."
    elif result["status"] == "syntax_error":
        diagnosis["explanation"] = "Python cannot read your code: " + result["message"]
    elif result["status"] == "runtime_error":
        diagnosis["explanation"] = "Your code crashed: " + result["message"]
    elif result["status"] == "timeout":
        diagnosis["explanation"] = "Your code ran too long. Check for an infinite loop."
    else:
        diagnosis["explanation"] = "Your code runs, but gives a wrong answer."

    # Find the smallest failing input (the unique feature)
    if result["status"] in ("logic_error", "runtime_error"):
        small = find_minimal_failing_input(code, problem_id)
        if small:
            diagnosis["minimal_failing_input"] = small["input"]
            diagnosis["expected_output"] = small["expected"]
            diagnosis["actual_output"] = small["actual"]

    # Name the misconception using AST rules
    if result["status"] in ("logic_error", "runtime_error", "timeout"):
        matches = find_misconceptions(code)
        if matches:
            error_type, line, explanation = matches[0]
            diagnosis["error_type"] = error_type
            diagnosis["line"] = line
            diagnosis["explanation"] = explanation
            diagnosis["confidence"] = 0.7

    return diagnosis