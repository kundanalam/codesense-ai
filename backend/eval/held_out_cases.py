HUMAN_CASES = [
    ("sum_list", "off_by_one_loop", """def sum_list(nums):
    total = 0
    n = len(nums)
    for i in range(n + 1):
        total += nums[i]
    return total"""),

    ("count_vowels", "reset_inside_loop", """def count_vowels(s):
    for ch in s:
        count = 0
        if ch in 'aeiou':
            count += 1
    return count"""),

    ("reverse_string", "return_inside_loop", """def reverse_string(s):
    result = ''
    for ch in s:
        result = ch + result
        return result
    return result"""),

    ("sum_to_n", "off_by_one_skip_last", """def sum_to_n(n):
    total = 0
    for i in range(n):
        total += i
    return total"""),

    ("factorial", "missing_base_case", """def factorial(n):
    if n == 5:
        return 1
    return n * factorial(n - 1)"""),

    ("average", "overwrite_instead_of_accumulate", """def average(nums):
    total = 0
    for n in nums:
        total = n
    return total / len(nums)"""),

    ("count_positive", "comparison_instead_of_assignment", """def count_positive(nums):
    count = 0
    for n in nums:
        if n > 0:
            count == count + 1
    return count"""),

    ("count_positive", "modify_list_while_iterating", """def count_positive(nums):
    for n in nums:
        if n <= 0:
            nums.pop(nums.index(n))
    return len(nums)"""),

    ("sum_list", "reset_inside_loop", """def sum_list(nums):
    i = 0
    while i < len(nums):
        total = 0
        total += nums[i]
        i += 1
    return total"""),

    ("find_max", "return_inside_loop", """def find_max(nums):
    best = nums[0]
    for n in nums:
        if n > best:
            best = n
        return best"""),

    ("sum_to_n", "off_by_one_loop", """def sum_to_n(n):
    total = 0
    for i in range(1, n + 2):
        total += i
    return total"""),

    ("reverse_string", "off_by_one_skip_last", """def reverse_string(s):
    result = ''
    i = 0
    while i < len(s) - 1:
        result = s[i] + result
        i += 1
    return result"""),
]