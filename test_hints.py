from backend.detect.analyze import analyze
from backend.teach.hints import get_hint

code = """def sum_list(nums):
    total = 0
    for i in range(len(nums) - 1):
        total += nums[i]
    return total"""

d = analyze(code, "sum_list")
print("Mistake found:", d["error_type"])
for level in range(1, 5):
    print(f"Level {level}:", get_hint(d, level))