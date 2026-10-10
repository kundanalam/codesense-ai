HUMAN_CASES = [
    ("find_max", "overwrite_instead_of_accumulate", """def find_max(nums):
    m = nums[0]
    for x in nums:
        m = x
    return m"""),

    ("count_vowels", "reset_inside_loop", """def count_vowels(s):
    for ch in s:
        count = 0
        if ch in 'aeiou':
            count += 1
    return count"""),

    # add 10 more here in the same format
]