from backend.detect.analyze import analyze

cases = {
    "find_max returns first": ("""def find_max(nums):
    return nums[0]""", "find_max"),

    "find_max overwrite": ("""def find_max(nums):
    best = 0
    for n in nums:
        best = n
    return best""", "find_max"),

    "factorial range(n)": ("""def factorial(n):
    result = 1
    for i in range(n):
        result *= i
    return result""", "factorial"),

    "sum off by one": ("""def sum_list(nums):
    total = 0
    for i in range(len(nums) + 1):
        total += nums[i]
    return total""", "sum_list"),
}

for name, (code, pid) in cases.items():
    d = analyze(code, pid)
    print(name)
    print("   input:", d["minimal_failing_input"],
          "| expected:", d["expected_output"],
          "| actual:", d["actual_output"])