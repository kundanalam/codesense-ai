from backend.detect.analyze import analyze

cases = {
    "off_by_one": ("""def sum_list(nums):
    total = 0
    for i in range(len(nums) + 1):
        total += nums[i]
    return total""", "sum_list"),

    "return_in_loop": ("""def sum_list(nums):
    total = 0
    for n in nums:
        total += n
        return total""", "sum_list"),

    "reset_in_loop": ("""def sum_list(nums):
    for n in nums:
        total = 0
        total += n
    return total""", "sum_list"),

    "overwrite": ("""def find_max(nums):
    best = 0
    for n in nums:
        best = n
    return best""", "find_max"),
}

for name, (code, pid) in cases.items():
    d = analyze(code, pid)
    print(name, "->", d["status"], "|", d["error_type"], "| line", d["line"])