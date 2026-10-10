from backend.problems import PROBLEMS

# (problem_id, true_label, text_to_replace, replacement)
MUTATIONS = [
    # ---- sum_list ----
    ("sum_list", "off_by_one_loop",
     "    for n in nums:\n        total += n\n",
     "    for i in range(len(nums) + 1):\n        total += nums[i]\n"),
    ("sum_list", "off_by_one_skip_last",
     "    for n in nums:\n        total += n\n",
     "    for i in range(len(nums) - 1):\n        total += nums[i]\n"),
    ("sum_list", "return_inside_loop",
     "        total += n\n", "        total += n\n        return total\n"),
    ("sum_list", "reset_inside_loop",
     "    for n in nums:\n", "    for n in nums:\n        total = 0\n"),
    ("sum_list", "overwrite_instead_of_accumulate",
     "        total += n\n", "        total = n\n"),
    ("sum_list", "comparison_instead_of_assignment",
     "        total += n\n", "        total == total + n\n"),

    # ---- find_max ----
    ("find_max", "off_by_one_loop",
     "    for n in nums:\n        if n > best:\n            best = n\n",
     "    for i in range(len(nums) + 1):\n        if nums[i] > best:\n            best = nums[i]\n"),
    ("find_max", "return_inside_loop",
     "            best = n\n", "            best = n\n        return best\n"),
    ("find_max", "overwrite_instead_of_accumulate",
     "    for n in nums:\n        if n > best:\n            best = n\n",
     "    for n in nums:\n        best = n\n"),

    # ---- factorial ----
    ("factorial", "missing_base_case",
     "def factorial(n):\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result\n",
     "def factorial(n):\n    return n * factorial(n - 1)\n"),
    ("factorial", "return_inside_loop",
     "        result *= i\n", "        result *= i\n        return result\n"),
    ("factorial", "reset_inside_loop",
     "        result *= i\n", "        result = 1\n        result *= i\n"),

    # ---- count_vowels ----
    ("count_vowels", "off_by_one_loop",
     "    for ch in s:\n        if ch in 'aeiou':\n",
     "    for i in range(len(s) + 1):\n        if s[i] in 'aeiou':\n"),
    ("count_vowels", "return_inside_loop",
     "            count += 1\n", "            count += 1\n            return count\n"),
    ("count_vowels", "reset_inside_loop",
     "    for ch in s:\n", "    for ch in s:\n        count = 0\n"),
    ("count_vowels", "comparison_instead_of_assignment",
     "            count += 1\n", "            count == count + 1\n"),

    # ---- reverse_string ----
    ("reverse_string", "off_by_one_loop",
     "    for ch in s:\n        result = ch + result\n",
     "    for i in range(len(s) + 1):\n        result = s[i] + result\n"),
    ("reverse_string", "return_inside_loop",
     "        result = ch + result\n", "        result = ch + result\n        return result\n"),
    ("reverse_string", "overwrite_instead_of_accumulate",
     "        result = ch + result\n", "        result = ch\n"),

    # ---- average ----
    ("average", "return_inside_loop",
     "        total += n\n", "        total += n\n        return total / len(nums)\n"),
    ("average", "reset_inside_loop",
     "    for n in nums:\n", "    for n in nums:\n        total = 0\n"),
    ("average", "comparison_instead_of_assignment",
     "        total += n\n", "        total == total + n\n"),
    ("average", "overwrite_instead_of_accumulate",
     "        total += n\n", "        total = n\n"),

    # ---- count_positive ----
    ("count_positive", "return_inside_loop",
     "            count += 1\n", "            count += 1\n            return count\n"),
    ("count_positive", "reset_inside_loop",
     "    for n in nums:\n", "    for n in nums:\n        count = 0\n"),
    ("count_positive", "comparison_instead_of_assignment",
     "            count += 1\n", "            count == count + 1\n"),
    ("count_positive", "modify_list_while_iterating",
     "        if n > 0:\n            count += 1\n",
     "        if n <= 0:\n            nums.remove(n)\n        else:\n            count += 1\n"),
    ("count_positive", "off_by_one_skip_last",
     "    for n in nums:\n        if n > 0:\n",
     "    for i in range(len(nums) - 1):\n        if nums[i] > 0:\n"),

    # ---- sum_to_n ----
    ("sum_to_n", "return_inside_loop",
     "        total += i\n", "        total += i\n        return total\n"),
    ("sum_to_n", "reset_inside_loop",
     "    for i in range(1, n + 1):\n", "    for i in range(1, n + 1):\n        total = 0\n"),
    ("sum_to_n", "comparison_instead_of_assignment",
     "        total += i\n", "        total == total + i\n"),
    ("sum_to_n", "overwrite_instead_of_accumulate",
     "        total += i\n", "        total = i\n"),
]


def build_cases():
    """Return a list of (problem_id, true_label, buggy_code)."""
    cases = []
    for pid, label, old, new in MUTATIONS:
        ref = PROBLEMS[pid]["reference"]
        if old not in ref:
            raise ValueError(f"Mutation text not found in {pid}: {old!r}")
        cases.append((pid, label, ref.replace(old, new, 1)))
    return cases