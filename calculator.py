"""Simple command-line calculator.

Supports + - * / // % ** , parentheses, unary minus, and a few math functions.
Type 'quit' or 'exit' to leave. The last result is available as 'ans'.
"""

import ast
import math
import operator

MAX_EXPONENT = 10000


def safe_pow(base, exponent):
    """Power with a cap on the exponent, so 9**9**9 can't hang the process."""
    if abs(exponent) > MAX_EXPONENT:
        raise ValueError(f"exponent too large (max {MAX_EXPONENT})")
    return operator.pow(base, exponent)


BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: safe_pow,
}

UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "abs": abs,
    "round": round,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def evaluate(expression, variables=None):
    """Safely evaluate an arithmetic expression string."""
    names = {**CONSTANTS, **(variables or {})}
    tree = ast.parse(expression, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPS:
            return BINARY_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
            return UNARY_OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.Name) and node.id in names:
            return names[node.id]
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in FUNCTIONS
        ):
            return FUNCTIONS[node.func.id](*[_eval(arg) for arg in node.args])
        raise ValueError("Unsupported expression")

    return _eval(tree)


def main():
    print("Calculator — type an expression (e.g. 2 + 3 * (4 - 1)), or 'quit' to exit.")
    ans = 0
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.lower() in ("quit", "exit"):
            break
        if not line:
            continue
        try:
            ans = evaluate(line, {"ans": ans})
            print(ans)
        except ZeroDivisionError:
            print("Error: division by zero")
        except (SyntaxError, ValueError, TypeError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
