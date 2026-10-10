from backend.problems import PROBLEMS
from backend.detect.sandbox import run_student_code

for pid, p in PROBLEMS.items():
    result = run_student_code(p["reference"], p["func"], p["tests"])
    print(pid, "->", result["status"])