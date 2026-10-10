from backend.detect.analyze_free import analyze_free

code = """def total(nums):
    t = 0
    for i in range(len(nums) - 1):
        t += nums[i]
    return t"""

print("--- no example ---")
d = analyze_free(code)
print(d["status"], "|", d["error_type"], "| line", d["line"])
print(d["hints"])

print("--- with example ---")
d = analyze_free(code, "total", [{"input": "[1, 2, 3]", "expected": "6"}])
print(d["status"], "|", d["error_type"], "| line", d["line"])
print(d["hints"][0])

print("--- syntax error ---")
d = analyze_free("def f(x)\n    return x")
print(d["status"], "| line", d["line"])