from backend.detect.analyze import analyze

cases = {
    "comparison_as_statement": ("""def sum_list(nums):
    total = 0
    for n in nums:
        total == total + n
    return total""", "sum_list"),

    "skip_last": ("""def sum_list(nums):
    total = 0
    for i in range(len(nums) - 1):
        total += nums[i]
    return total""", "sum_list"),

    "missing_base_case": ("""def factorial(n):
    return n * factorial(n - 1)""", "factorial"),

    "modify_while_iterating": ("""def count_positive(nums):
    count = 0
    for n in nums:
        if n <= 0:
            nums.remove(n)
        else:
            count += 1
    return count""", "count_positive"),
}

for name, (code, pid) in cases.items():
    d = analyze(code, pid)
    print(name, "->", d["status"], "|", d["error_type"], "| line", d["line"],
          "| input", d["minimal_failing_input"])