from backend.detect.sandbox import run_student_code

# Each test is: ([arguments], expected_answer)
tests = [([[1, 2, 3]], 6), ([[]], 0), ([[5]], 5)]

good = """def sum_list(nums):
    t = 0
    for n in nums:
        t += n
    return t"""

off_by_one = """def sum_list(nums):
    t = 0
    for i in range(len(nums) + 1):
        t += nums[i]
    return t"""

wrong_answer = """def sum_list(nums):
    t = 0
    for n in nums:
        t = n
    return t"""

syntax_bug = """def sum_list(nums)
    return 0"""

infinite = """def sum_list(nums):
    while True:
        pass"""

for name, code in [("good", good), ("off_by_one", off_by_one),
                   ("wrong_answer", wrong_answer), ("syntax_bug", syntax_bug),
                   ("infinite", infinite)]:
    print(name, "->", run_student_code(code, "sum_list", tests))