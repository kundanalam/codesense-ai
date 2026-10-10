PROBLEMS = {
    "sum_list": {
        "title": "Sum of a list",
        "description": "Write a function sum_list(nums) that returns the sum of all numbers in the list. An empty list returns 0.",
        "func": "sum_list",
        "starter_code": "def sum_list(nums):\n    # your code here\n",
        "tests": [
            ([[1, 2, 3]], 6),
            ([[]], 0),
            ([[5]], 5),
            ([[-2, 4]], 2),
            ([[10, 20, 30, 40]], 100),
        ],
        "reference": (
            "def sum_list(nums):\n"
            "    total = 0\n"
            "    for n in nums:\n"
            "        total += n\n"
            "    return total\n"
        ),
    },
    "find_max": {
        "title": "Largest number in a list",
        "description": "Write a function find_max(nums) that returns the largest number in a non-empty list.",
        "func": "find_max",
        "starter_code": "def find_max(nums):\n    # your code here\n",
        "tests": [
            ([[1, 5, 3]], 5),
            ([[7]], 7),
            ([[-4, -1, -9]], -1),
            ([[2, 2, 2]], 2),
            ([[0, 10, 4]], 10),
        ],
        "reference": (
            "def find_max(nums):\n"
            "    best = nums[0]\n"
            "    for n in nums:\n"
            "        if n > best:\n"
            "            best = n\n"
            "    return best\n"
        ),
    },
    "factorial": {
        "title": "Factorial",
        "description": "Write a function factorial(n) that returns n! (factorial(0) is 1).",
        "func": "factorial",
        "starter_code": "def factorial(n):\n    # your code here\n",
        "tests": [
            ([0], 1),
            ([1], 1),
            ([3], 6),
            ([5], 120),
            ([6], 720),
        ],
        "reference": (
            "def factorial(n):\n"
            "    result = 1\n"
            "    for i in range(1, n + 1):\n"
            "        result *= i\n"
            "    return result\n"
        ),
    },
        "count_vowels": {
        "title": "Count vowels",
        "description": "Write a function count_vowels(s) that returns how many vowels (a, e, i, o, u) are in the lowercase string s.",
        "func": "count_vowels",
        "starter_code": "def count_vowels(s):\n    # your code here\n",
        "tests": [
            (["hello"], 2),
            ([""], 0),
            (["sky"], 0),
            (["aeiou"], 5),
            (["banana"], 3),
        ],
        "reference": (
            "def count_vowels(s):\n"
            "    count = 0\n"
            "    for ch in s:\n"
            "        if ch in 'aeiou':\n"
            "            count += 1\n"
            "    return count\n"
        ),
    },
    "reverse_string": {
        "title": "Reverse a string",
        "description": "Write a function reverse_string(s) that returns the string s reversed.",
        "func": "reverse_string",
        "starter_code": "def reverse_string(s):\n    # your code here\n",
        "tests": [
            (["abc"], "cba"),
            ([""], ""),
            (["a"], "a"),
            (["hello"], "olleh"),
            (["ab"], "ba"),
        ],
        "reference": (
            "def reverse_string(s):\n"
            "    result = ''\n"
            "    for ch in s:\n"
            "        result = ch + result\n"
            "    return result\n"
        ),
    },
    "average": {
        "title": "Average of a list",
        "description": "Write a function average(nums) that returns the average of a non-empty list of numbers.",
        "func": "average",
        "starter_code": "def average(nums):\n    # your code here\n",
        "tests": [
            ([[1, 2]], 1.5),
            ([[2, 4, 6]], 4.0),
            ([[5]], 5.0),
            ([[-3, 3]], 0.0),
            ([[10, 20, 30, 40]], 25.0),
        ],
        "reference": (
            "def average(nums):\n"
            "    total = 0\n"
            "    for n in nums:\n"
            "        total += n\n"
            "    return total / len(nums)\n"
        ),
    },
    "count_positive": {
        "title": "Count positive numbers",
        "description": "Write a function count_positive(nums) that returns how many numbers in the list are greater than 0.",
        "func": "count_positive",
        "starter_code": "def count_positive(nums):\n    # your code here\n",
        "tests": [
            ([[1, -2, 3]], 2),
            ([[]], 0),
            ([[0, 0]], 0),
            ([[5]], 1),
            ([[-1, -2]], 0),
        ],
        "reference": (
            "def count_positive(nums):\n"
            "    count = 0\n"
            "    for n in nums:\n"
            "        if n > 0:\n"
            "            count += 1\n"
            "    return count\n"
        ),
    },
    "sum_to_n": {
        "title": "Sum from 1 to n",
        "description": "Write a function sum_to_n(n) that returns 1 + 2 + ... + n. For n = 0 it returns 0.",
        "func": "sum_to_n",
        "starter_code": "def sum_to_n(n):\n    # your code here\n",
        "tests": [
            ([0], 0),
            ([1], 1),
            ([4], 10),
            ([5], 15),
            ([10], 55),
        ],
        "reference": (
            "def sum_to_n(n):\n"
            "    total = 0\n"
            "    for i in range(1, n + 1):\n"
            "        total += i\n"
            "    return total\n"
        ),
    },
}