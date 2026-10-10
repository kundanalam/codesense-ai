from collections import defaultdict
from backend.eval.mutations import build_cases
from backend.detect.analyze import analyze


def main():
    cases = build_cases()
    stats = defaultdict(lambda: [0, 0])   # label -> [correct, total]
    wrong = []
    skipped = 0

    for pid, label, code in cases:
        d = analyze(code, pid)
        if d["status"] == "correct":      # the mutation did not actually break the code
            skipped += 1
            print("SKIPPED (not a real bug):", pid, label)
            continue
        stats[label][1] += 1
        if d["error_type"] == label:
            stats[label][0] += 1
        else:
            wrong.append((pid, label, d["error_type"]))

    print("\nLabel                              correct/total")
    for label, (ok, total) in sorted(stats.items()):
        print(f"{label:35s}{ok}/{total}")
    ok_all = sum(v[0] for v in stats.values())
    total_all = sum(v[1] for v in stats.values())
    print(f"\nOVERALL: {ok_all}/{total_all}  ({100 * ok_all / max(total_all, 1):.0f}%)   skipped: {skipped}")
    print("\nMistakes (problem, true label, predicted):")
    for w in wrong:
        print("  ", w)


if __name__ == "__main__":
    main()