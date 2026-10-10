import random
from backend.problems import PROBLEMS
from backend.detect.sandbox import run_student_code

# What kind of input each problem takes. Add a line here for every new problem.
INPUT_KIND = {
    "sum_list": "list",
    "find_max": "nonempty_list",
    "factorial": "small_int",
    "count_vowels": "string",
    "reverse_string": "string",
    "average": "nonempty_list",
    "count_positive": "list",
    "sum_to_n": "small_int",
}

ALPHABET = "abcdeiou"


def _get_reference(problem):
    ns = {}
    exec(problem["reference"], ns)   # our own trusted code, so safe to run here
    return ns[problem["func"]]


def _random_args(kind, rng):
    if kind == "small_int":
        return [rng.randint(0, 8)]
    if kind == "string":
        n = rng.randint(0, 5)
        return ["".join(rng.choice(ALPHABET) for _ in range(n))]
    low = 1 if kind == "nonempty_list" else 0
    n = rng.randint(low, 5)
    return [[rng.randint(-5, 10) for _ in range(n)]]


def _smaller_versions(args, kind):
    """Yield inputs that are strictly simpler than args, simplest first."""
    if kind == "small_int":
        for k in range(args[0]):
            yield [k]
        return

    if kind == "string":
        s = args[0]
        for i in range(len(s)):            # remove one character
            yield [s[:i] + s[i + 1:]]
        for i, ch in enumerate(s):         # replace one character with 'b'
            if ch != "b":
                yield [s[:i] + "b" + s[i + 1:]]
        return

    lst = args[0]
    # 1. remove one element
    for i in range(len(lst)):
        cand = lst[:i] + lst[i + 1:]
        if kind == "nonempty_list" and not cand:
            continue
        yield [cand]
    # 2. replace one element with 0
    for i, x in enumerate(lst):
        if x != 0:
            yield [lst[:i] + [0] + lst[i + 1:]]
    # 3. move one element halfway towards 0
    for i, x in enumerate(lst):
        if abs(x) > 1:
            yield [lst[:i] + [int(x / 2)] + lst[i + 1:]]


def _fails(code, func, args, ref):
    try:
        expected = ref(*args)
    except Exception:
        return False
    res = run_student_code(code, func, [(args, expected)], timeout=1)
    return res["status"] != "correct"


def find_minimal_failing_input(code, problem_id, tries=40, seed=0):
    """Return a dict describing the smallest failing input, or None."""
    problem = PROBLEMS[problem_id]
    func = problem["func"]
    kind = INPUT_KIND[problem_id]
    ref = _get_reference(problem)
    rng = random.Random(seed)   # fixed seed = same result every run

    tests = []
    for _ in range(tries):
        args = _random_args(kind, rng)
        tests.append((args, ref(*args)))

    first = run_student_code(code, func, tests)
    if first["status"] not in ("logic_error", "runtime_error"):
        return None
    args = first.get("failed_input")
    if args is None:
        return None

    # Shrink until no simpler input still fails
    improved = True
    while improved:
        improved = False
        for cand in _smaller_versions(args, kind):
            if _fails(code, func, cand, ref):
                args = cand
                improved = True
                break

    expected = ref(*args)
    final = run_student_code(code, func, [(args, expected)])
    return {
        "input": args,
        "expected": expected,
        "actual": final.get("actual", final.get("message")),
        "status": final["status"],
    }