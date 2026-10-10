# 4 hint levels for each misconception.
# Level 1 = nudge, 2 = location, 3 = concept, 4 = near-solution (in words only).
# {input}, {expected}, {actual} and {line} are filled in automatically.

HINTS = {
    "off_by_one_loop": [
        "Try your function with {input}. You expected {expected}, but what happened?",
        "Look at line {line}. Check where your loop starts and where it stops.",
        "A list with 3 items has positions 0, 1 and 2. There is no position 3. Make sure your loop never asks for a position that does not exist.",
        "Your loop goes one step further than the list allows. Reduce the end of the loop by one.",
    ],
    "off_by_one_skip_last": [
        "Try your function with {input}. You expected {expected}, but you got {actual}.",
        "Look at line {line}. Count how many times your loop runs, and compare it with how many items there are.",
        "range(3) gives 0, 1, 2, so it stops before 3. If you stop too early, the last item is never used.",
        "Your loop ends one step too soon, so the last item is skipped. Make the loop reach the final item.",
    ],
    "return_inside_loop": [
        "Try your function with {input}. You expected {expected}, but you got {actual}. Does your code only look at the first item?",
        "Look at line {line}. Where does the return sit compared to the loop?",
        "A return ends the whole function immediately. If it is inside a loop, the loop only runs once.",
        "Move the return so it happens after the loop has finished, not during it.",
    ],
    "reset_inside_loop": [
        "Try your function with {input}. You expected {expected}, but you got {actual}. Is your running total being lost?",
        "Look at line {line}. A variable is given its starting value there. How often does that line run?",
        "Anything set inside a loop is set again on every pass. A starting value should be set once, before the loop.",
        "Move the line that sets the starting value to before the loop begins.",
    ],
    "overwrite_instead_of_accumulate": [
        "Try your function with {input}. You expected {expected}, but you got {actual}. Is only the last item counted?",
        "Look at line {line}. Does the new value keep what the variable had before?",
        "Using = replaces the old value. To build up a result, you must combine the old value with the new item.",
        "Change the line so it adds to the existing value instead of replacing it.",
    ],
    "comparison_instead_of_assignment": [
        "Try your function with {input}. You expected {expected}, but you got {actual}. Does the variable ever change?",
        "Look at line {line}. Is that line storing a value, or only checking something?",
        "A single = stores a value. A double == only asks a question (true or false) and stores nothing.",
        "Use the single-equals operator, or +=, so the result is actually stored.",
    ],
    "missing_base_case": [
        "Try your function with {input}. What happens when it reaches the smallest case? Does it ever stop?",
        "Look at line {line}. Your function calls itself. Where does it decide to stop calling itself?",
        "A function that calls itself needs a stopping rule, otherwise it runs forever. The stop is called the base case.",
        "Add a check at the start of the function: for the smallest input, return a fixed answer without calling itself.",
    ],
    "modify_list_while_iterating": [
        "Try your function with {input}. You expected {expected}, but you got {actual}. Are some items being skipped?",
        "Look at line {line}. You are changing the list while the loop is walking through it.",
        "When you remove an item, the remaining items shift position, and the loop skips the one that moves into the gap.",
        "Do not change the list you are looping over. Count or collect results in a separate variable instead.",
    ],
}

GENERIC = [
    "Try your function with {input}. You expected {expected}, but you got {actual}. What is different?",
    "Trace your code by hand on {input}, one line at a time. Write down each variable's value.",
    "Compare your hand trace with the expected answer. At which line do they first disagree?",
    "Check the line where the values first disagree. Think about what that line should do instead.",
]


def get_hint(diagnosis, level):
    """Return the hint text for level 1-4."""
    level = max(1, min(4, level))
    templates = HINTS.get(diagnosis.get("error_type"), GENERIC)
    inp = diagnosis.get("minimal_failing_input")
    if isinstance(inp, list) and len(inp) == 1:
        inp = inp[0]          # show [1, 0] instead of [[1, 0]]
    return templates[level - 1].format(
        input=inp,
        expected=diagnosis.get("expected_output"),
        actual=diagnosis.get("actual_output"),
        line=diagnosis.get("line"),
    )