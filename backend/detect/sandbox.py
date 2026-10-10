import subprocess
import sys
import json

# This small program runs in a separate process, so a student's
# infinite loop or crash cannot break your main program.
RUNNER = r'''
import sys, json
payload = json.loads(sys.stdin.read())

try:
    compiled = compile(payload["code"], "student.py", "exec")
except SyntaxError as e:
    print(json.dumps({"status": "syntax_error", "line": e.lineno, "message": e.msg}))
    sys.exit(0)

ns = {}
try:
    exec(compiled, ns)
    fn = ns[payload["func"]]
except Exception as e:
    print(json.dumps({"status": "runtime_error", "line": None, "message": repr(e)}))
    sys.exit(0)

for args, expected in payload["tests"]:
    try:
        out = fn(*args)
    except Exception as e:
        tb = e.__traceback__
        line = None
        while tb:
            if tb.tb_frame.f_code.co_filename == "student.py":
                line = tb.tb_lineno
            tb = tb.tb_next
        print(json.dumps({"status": "runtime_error", "line": line,
                          "message": repr(e), "failed_input": args}, default=repr))
        sys.exit(0)
    if out != expected:
        print(json.dumps({"status": "logic_error", "failed_input": args,
                          "expected": expected, "actual": out}, default=repr))
        sys.exit(0)

print(json.dumps({"status": "correct"}))
'''


def run_student_code(code, func_name, tests, timeout=2):
    """Run student code against tests. Returns a dict with a 'status'."""
    payload = json.dumps({"code": code, "func": func_name, "tests": tests})
    try:
        p = subprocess.run(
            [sys.executable, "-c", RUNNER],
            input=payload, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}

    if not p.stdout.strip():
        return {"status": "runtime_error", "line": None, "message": p.stderr[-300:]}
    return json.loads(p.stdout.strip().splitlines()[-1])