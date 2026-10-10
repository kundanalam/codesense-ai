import inspect
from backend.detect import analyze as a
from backend.detect.ast_rules import find_misconceptions

code = """def sum_list(nums):
    total = 0
    for i in range(len(nums) - 1):
        total += nums[i]
    return total"""

print("1. Rules found:", find_misconceptions(code))
print("2. analyze.py uses rules:", "find_misconceptions(code)" in inspect.getsource(a))
print("3. File used:", a.__file__)