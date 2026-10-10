import ast


def _is_len_call(node):
    return (isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "len")


def _len_plus_minus_one(arg, op_type):
    """True for len(x) + 1 (op_type=ast.Add) or len(x) - 1 (op_type=ast.Sub)."""
    return (isinstance(arg, ast.BinOp)
            and isinstance(arg.op, op_type)
            and _is_len_call(arg.left)
            and isinstance(arg.right, ast.Constant)
            and arg.right.value == 1)


def _names_in(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def find_misconceptions(code):
    """Return a list of (error_type, line, explanation) found in the code."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    # names of all function parameters (used by the range(1, n) rule)
    params = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef):
            params |= {a.arg for a in n.args.args}

    found = []

    for node in ast.walk(tree):

        # Rules 1 and 8: range bounds that are one too far or one too short
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "range"):
            for arg in node.args:
                if _len_plus_minus_one(arg, ast.Add):
                    found.append((
                        "off_by_one_loop", node.lineno,
                        "The loop runs one step too many, so it goes past the end of the list."))
                if _len_plus_minus_one(arg, ast.Sub):
                    found.append((
                        "off_by_one_skip_last", node.lineno,
                        "The loop stops one step too early, so the last item is never visited."))
            # NEW: range(1, n) never reaches n itself
            if (len(node.args) == 2
                    and isinstance(node.args[0], ast.Constant)
                    and node.args[0].value == 1
                    and isinstance(node.args[1], ast.Name)
                    and node.args[1].id in params):
                found.append((
                    "off_by_one_skip_last", node.lineno,
                    "range(1, n) stops at n - 1, so n itself is never included."))

        # NEW: while i <= len(x) goes one step too far
        if isinstance(node, ast.While) and isinstance(node.test, ast.Compare):
            t = node.test
            if (len(t.ops) == 1 and isinstance(t.ops[0], ast.LtE)
                    and _is_len_call(t.comparators[0])):
                found.append((
                    "off_by_one_loop", node.lineno,
                    "The loop condition allows one step too many, so it goes past the end of the list."))

        # Rule 2: return placed inside a loop
        if isinstance(node, (ast.For, ast.While)):
            for child in ast.walk(node):
                if isinstance(child, ast.Return):
                    found.append((
                        "return_inside_loop", child.lineno,
                        "The return is inside the loop, so the function stops after the first pass."))
                    break

        # Rule 3: variable reset inside a loop
        if isinstance(node, (ast.For, ast.While)):
            for stmt in node.body:
                if (isinstance(stmt, ast.Assign)
                        and isinstance(stmt.value, ast.Constant)
                        and stmt.value.value in (0, 1)):
                    found.append((
                        "reset_inside_loop", stmt.lineno,
                        "A variable is set back to its starting value on every pass of the loop."))

        # Rule 4 (generalised): result replaced using only the loop variable,
        # never using its own old value
        if isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            loop_var = node.target.id
            for stmt in node.body:
                if (isinstance(stmt, ast.Assign)
                        and len(stmt.targets) == 1
                        and isinstance(stmt.targets[0], ast.Name)):
                    target = stmt.targets[0].id
                    used = _names_in(stmt.value)
                    if loop_var in used and target not in used:
                        found.append((
                            "overwrite_instead_of_accumulate", stmt.lineno,
                            "The variable is replaced on every pass instead of building up a result."))

        # Rule 5: a line that only compares (==) and stores nothing
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Compare):
            found.append((
                "comparison_instead_of_assignment", node.lineno,
                "This line uses == to compare, but nothing is stored. Did you mean a single = ?"))

        # Rule 6: function calls itself but has no if (no base case)
        if isinstance(node, ast.FunctionDef):
            calls_self = any(
                isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                and c.func.id == node.name
                for c in ast.walk(node))
            has_check = any(isinstance(c, (ast.If, ast.IfExp)) for c in ast.walk(node))
            if calls_self and not has_check:
                found.append((
                    "missing_base_case", node.lineno,
                    "The function calls itself but never checks when to stop."))

        # Rule 7: changing a list while looping over it
        if isinstance(node, ast.For) and isinstance(node.iter, ast.Name):
            for child in ast.walk(node):
                if (isinstance(child, ast.Call)
                        and isinstance(child.func, ast.Attribute)
                        and isinstance(child.func.value, ast.Name)
                        and child.func.value.id == node.iter.id
                        and child.func.attr in ("append", "remove", "pop", "insert")):
                    found.append((
                        "modify_list_while_iterating", child.lineno,
                        "The list is changed while the loop is going through it, so items get skipped."))
                    break

    return found