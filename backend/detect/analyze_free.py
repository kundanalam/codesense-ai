from backend.detect.safety import unsafe_reason, blocked_diagnosis
import ast
import re
import subprocess
import sys

from backend.detect.sandbox import run_student_code
from backend.detect.ast_rules import find_misconceptions
from backend.teach.hints import HINTS, get_hint


def _run_script(code):
    """Run any code as a plain script, to catch crashes and infinite loops."""
    try:
        p = subprocess.run([sys.executable, "-c", code], input="",
                           capture_output=True, text=True, timeout=3)
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    if p.returncode == 0:
        return {"status": "ok"}
    lines = p.stderr.strip().splitlines()
    last = lines[-1] if lines else "Unknown error"
    if last.startswith("EOFError"):      # code asked for input(); we cannot answer it
        return {"status": "ok"}
    where = re.findall(r'File "<string>", line (\d+)', p.stderr)
    return {"status": "runtime_error",
            "line": int(where[-1]) if where else None,
            "message": last}


def _parse(text):
    """Turn text like '[1,2,3]' or '2, 3' into a list of arguments."""
    return list(ast.literal_eval("(" + text + ",)"))


def _hints(d, has_example):
    et = d["error_type"]
    line = d["line"]
    if d["status"] == "syntax_error":
        return [
            "Python could not read your code. Look near line %s." % line,
            "Check line %s and the line just before it." % line,
            "Common causes: a missing colon, a missing bracket or quote, or wrong spacing at the start of the line.",
            "Read that line slowly, one word at a time, and compare it with a working example.",
        ]
    if d["status"] == "timeout":
        return [
            "Your code ran for too long. Is there a loop that never ends?",
            "Look at your while loops. What makes each one stop?",
            "A loop needs something inside it that moves it closer to stopping.",
            "Make sure the variable in the loop condition changes on every pass.",
        ]
    if et in HINTS:
        if has_example and d["minimal_failing_input"] is not None:
            return [get_hint(d, i) for i in range(1, 5)]
        tpl = HINTS[et]
        first = "Pick a small input and follow your code by hand. What do you expect, and what do you get?"
        return [first] + [tpl[i].format(line=line, input="", expected="", actual="")
                          for i in (1, 2, 3)]
    if d["status"] == "runtime_error":
        return [
            "Your code stopped with an error: %s" % d["actual_output"],
            "Look at line %s." % line,
            "Check the values used on that line. Are they what you expect?",
            "Print the variables just before that line to see their values.",
        ]
    if d["status"] == "logic_error":
        return [get_hint(d, i) for i in range(1, 5)]
    return []


def analyze_free(code, func=None, examples=None):
    why = unsafe_reason(code)
    if why:
        return blocked_diagnosis(why)
    d = {"status": "no_error_found", "error_type": None, "line": None,
         "confidence": 0.0, "explanation": "", "minimal_failing_input": None,
         "expected_output": None, "actual_output": None, "hints": []}

    try:
        compile(code, "student.py", "exec")
    except SyntaxError as e:
        d["status"] = "syntax_error"
        d["line"] = e.lineno
        d["error_type"] = "indentation_error" if "indent" in str(e.msg) else "syntax_error"
        d["confidence"] = 1.0
        d["explanation"] = "Python cannot read your code: " + str(e.msg)
        d["hints"] = _hints(d, False)
        return d

    has_example = bool(func and examples)
    if has_example:
        try:
            tests = [(_parse(ex["input"]), ast.literal_eval(ex["expected"]))
                     for ex in examples]
        except Exception:
            d["status"] = "bad_example"
            d["explanation"] = "Could not read your example. Write input like [1, 2, 3] and expected output like 6."
            return d
        r = run_student_code(code, func, tests)
    else:
        r = _run_script(code)

    status = r["status"]
    if status == "ok":
        status = "no_error_found"
    d["status"] = status
    d["line"] = r.get("line")
    d["minimal_failing_input"] = r.get("failed_input")
    d["expected_output"] = r.get("expected")
    d["actual_output"] = r.get("actual", r.get("message"))

    if status == "correct":
        d["explanation"] = "Your code passed all your examples."
        return d
    if status == "no_error_found":
        d["explanation"] = ("No crash found. Without an example, I cannot tell if the answer is right.")
    elif status == "runtime_error":
        d["explanation"] = "Your code crashed: " + str(r.get("message"))
    elif status == "timeout":
        d["explanation"] = "Your code ran too long. Check for an infinite loop."
    else:
        d["explanation"] = "Your code runs, but gives a wrong answer."

    matches = find_misconceptions(code)
    if status == "no_error_found":
        # The code ran fine and there is no example, so only report
        # patterns that are almost never correct.
        RELIABLE = {"comparison_instead_of_assignment",
                    "missing_base_case",
                    "modify_list_while_iterating"}
        matches = [m for m in matches if m[0] in RELIABLE]
    if matches:
        d["error_type"], d["line"], d["explanation"] = matches[0]
        d["confidence"] = 0.7
    if not d["error_type"]:
        d["error_type"] = {"runtime_error": "runtime_error", "timeout": "infinite_loop"}.get(status)
    d["hints"] = _hints(d, has_example)
    return d