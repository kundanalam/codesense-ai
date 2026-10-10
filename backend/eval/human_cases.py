# (problem_id, true_label, buggy_code)
# Written naturally, not copied from the rule patterns.
HUMAN_CASES = [
    ("sum_list", "off_by_one_loop", """def sum_list(nums):
    total = 0
    i = 0
    while i <= len(nums):
        total += nums[i]
        i += 1
    return total"""),

    ("sum_list", "off_by_one_skip_last", """def sum_list(nums):
    total = 0
    for i in range(0, len(nums) - 1):
        total = total + nums[i]
    return total"""),

    ("sum_list", "reset_inside_loop", """def sum_list(nums):
    for n in nums:
        total = 0
        total = total + n
    return total"""),

    ("sum_list", "return_inside_loop", """def sum_list(nums):
    total = 0
    for n in nums:
        total = total + n
        return total"""),

    ("sum_list", "overwrite_instead_of_accumulate", """def sum_list(nums):
    total = 0
    for n in nums:
        total = n + 0
    return total"""),

    ("find_max", "overwrite_instead_of_accumulate", """def find_max(nums):
    biggest = nums[0]
    for n in nums:
        biggest = n
    return biggest"""),

    ("find_max", "return_inside_loop", """def find_max(nums):
    best = nums[0]
    for n in nums:
        if n > best:
            best = n
        else:
            return best
    return best"""),

    ("factorial", "missing_base_case", """def factorial(n):
    return n * factorial(n - 1)"""),

    ("factorial", "off_by_one_skip_last", """def factorial(n):
    result = 1
    for i in range(1, n):
        result *= i
    return result"""),

    ("count_vowels", "off_by_one_loop", """def count_vowels(s):
    count = 0
    for i in range(len(s) + 1):
        if s[i] in 'aeiou':
            count += 1
    return count"""),

    ("count_vowels", "comparison_instead_of_assignment", """def count_vowels(s):
    count = 0
    for ch in s:
        if ch in 'aeiou':
            count == count + 1
    return count"""),

    ("reverse_string", "overwrite_instead_of_accumulate", """def reverse_string(s):
    result = ''
    for ch in s:
        result = ch
    return result"""),

    ("average", "return_inside_loop", """def average(nums):
    total = 0
    for n in nums:
        total += n
        return total / len(nums)"""),

    ("count_positive", "modify_list_while_iterating", """def count_positive(nums):
    for n in nums:
        if n <= 0:
            nums.remove(n)
    return len(nums)"""),

    ("sum_to_n", "off_by_one_skip_last", """def sum_to_n(n):
    total = 0
    for i in range(1, n):
        total += i
    return total"""),

    ("sum_to_n", "reset_inside_loop", """def sum_to_n(n):
    for i in range(1, n + 1):
        total = 0
        total += i
    return total"""),
]