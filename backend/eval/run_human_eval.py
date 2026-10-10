import sys
from importlib import import_module
from collections import defaultdict
from backend.detect.analyze import analyze

MODULE = sys.argv[1] if len(sys.argv) > 1 else "human_cases"
HUMAN_CASES = import_module("backend.eval." + MODULE).HUMAN_CASES


def main():
    ok = 0
    total = 0
    by_label = defaultdict(lambda: [0, 0])
    for pid, label, code in HUMAN_CASES:
        d = analyze(code, pid)
        if d["status"] == "correct":
            print("SKIPPED (not a real bug):", pid, label)
            continue
        total += 1
        by_label[label][1] += 1
        got = d["error_type"]
        if got == label:
            ok += 1
            by_label[label][0] += 1
        else:
            print(f"MISS  {pid:15s} true={label:32s} predicted={got}")
    print()
    for label, (c, t) in sorted(by_label.items()):
        print(f"{label:35s}{c}/{t}")
    print(f"\nACCURACY: {ok}/{total}  ({100 * ok / max(total, 1):.0f}%)")


if __name__ == "__main__":
    main()