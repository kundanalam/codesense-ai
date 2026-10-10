from backend.problems import PROBLEMS
from backend.teach.hints import HINTS
from backend.teach.leakage import is_leaking

# Sample values used to fill the {input}, {expected}, {actual}, {line} gaps
FILL = dict(input="[1, 2]", expected="3", actual="1", line="3")


def main():
    total = 0
    blocked = 0
    for label, templates in HINTS.items():
        for level, tpl in enumerate(templates, start=1):
            text = tpl.format(**FILL)
            for pid, p in PROBLEMS.items():
                total += 1
                if is_leaking(text, p["reference"]):
                    blocked += 1
                    print("BLOCKED:", label, "level", level, "vs", pid)
    print(f"\nHints checked: {total}")
    print(f"Blocked as leaking: {blocked}")
    print(f"LEAKAGE RATE: {100 * blocked / total:.1f}%")

    # Sanity check: the checker must catch real leaks
    caught = 0
    for pid, p in PROBLEMS.items():
        if is_leaking("The answer is:\n" + p["reference"], p["reference"]):
            caught += 1
    print(f"\nChecker catches full solutions: {caught}/{len(PROBLEMS)}")


if __name__ == "__main__":
    main()