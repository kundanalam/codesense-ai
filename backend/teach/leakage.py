import ast
import re
from difflib import SequenceMatcher


def _normalise(code):
    """Turn code into a form that ignores names and spacing."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            node.id = "v"
        if isinstance(node, ast.arg):
            node.arg = "v"
        if isinstance(node, ast.FunctionDef):
            node.name = "f"
    return ast.dump(tree)


def _code_in(text):
    """Pull out anything in the hint that looks like code lines."""
    lines = []
    for line in text.splitlines():
        if re.search(r"(def |return |for .* in |while |if |elif |else:|\w+\s*[+\-*/]?=\s*\S)", line):
            lines.append(line.strip())
    return "\n".join(lines)


def _line_overlap(hint, reference):
    """Share of the reference solution's lines that appear in the hint."""
    ref_lines = [re.sub(r"\s+", "", l) for l in reference.splitlines() if l.strip()]
    hint_lines = {re.sub(r"\s+", "", l) for l in hint.splitlines() if l.strip()}
    if len(ref_lines) < 3:
        return 0.0
    hits = sum(1 for l in ref_lines if l in hint_lines)
    return hits / len(ref_lines)


def is_leaking(hint, reference, threshold=0.8):
    """True if the hint contains code that is too close to the reference solution."""
    # New check: most lines of the solution appear in the hint
    if _line_overlap(hint, reference) >= 0.6:
        return True

    snippet = _code_in(hint)
    if not snippet:
        return False

    ref_norm = _normalise(reference)
    snip_norm = _normalise(snippet)
    if ref_norm and snip_norm:
        if SequenceMatcher(None, snip_norm, ref_norm).ratio() >= threshold:
            return True

    # Fallback: compare plain text with spaces removed
    a = re.sub(r"\s+", "", snippet)
    b = re.sub(r"\s+", "", reference)
    return a in b and len(a) > 40


SAFE_FALLBACK = "Look carefully at the line you changed last. What should it do for the smallest input?"


def check_hint(hint, reference):
    """Return (hint_to_show, was_blocked)."""
    if is_leaking(hint, reference):
        return SAFE_FALLBACK, True
    return hint, False