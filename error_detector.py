import ast
from typing import Any, Dict, List


class ErrorFinder(ast.NodeVisitor):
    """
    Walks the AST and collects simple static issues:
    - unused variables
    - variables possibly used before assignment
    - trivial logical issues (e.g. x == x, constant conditions, division by zero)
    """

    def __init__(self) -> None:
        self.errors: List[Dict[str, Any]] = []
        self.defined_vars: dict[str, int] = {}
        self.used_vars: set[str] = set()
        self.builtins = set(dir(__builtins__))

    def _add_error(self, err_type: str, node: ast.AST, message: str, suggestion: str) -> None:
        line = getattr(node, "lineno", "Unknown")
        self.errors.append(
            {
                "type": err_type,
                "line": line,
                "message": message,
                "suggestion": suggestion,
            }
        )

    def visit_Assign(self, node: ast.Assign) -> None:
        """Track assigned variable names and their line numbers."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                # First assignment wins for the "defined at" line reference.
                self.defined_vars.setdefault(target.id, node.lineno)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        """Track variables being read, and flag reads of never-defined names."""
        if isinstance(node.ctx, ast.Load):
            name = node.id
            self.used_vars.add(name)
            if name not in self.defined_vars and name not in self.builtins:
                self._add_error(
                    "PossiblyUndefinedVariable",
                    node,
                    f"Variable '{name}' is used before being defined in this scope.",
                    f"Define '{name}' before using it, or check for typos.",
                )
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        """Look for simple always-true/false comparisons like x == x."""
        if len(node.ops) == 1 and len(node.comparators) == 1:
            left = node.left
            right = node.comparators[0]
            op = node.ops[0]

            if isinstance(left, ast.Name) and isinstance(right, ast.Name) and left.id == right.id:
                if isinstance(op, ast.Eq):
                    self._add_error(
                        "TrivialComparison",
                        node,
                        f"Expression '{left.id} == {right.id}' is always True.",
                        "Double-check the condition; you may have intended to compare two different variables.",
                    )
                elif isinstance(op, ast.NotEq):
                    self._add_error(
                        "TrivialComparison",
                        node,
                        f"Expression '{left.id} != {right.id}' is always False.",
                        "Double-check the condition; you may have intended to compare two different variables.",
                    )
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Detect obvious arithmetic problems (e.g. division by literal zero)."""
        if isinstance(node.op, (ast.Div, ast.FloorDiv)) and isinstance(node.right, ast.Constant):
            if isinstance(node.right.value, (int, float)) and node.right.value == 0:
                self._add_error(
                    "DivisionByZero",
                    node,
                    "This division operation divides by zero, which will raise a ZeroDivisionError at runtime.",
                    "Guard against zero before dividing, or handle the zero case separately.",
                )
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """Flag if statements with constant conditions like if True / if False."""
        test = node.test
        if isinstance(test, ast.Constant) and isinstance(test.value, bool):
            value = test.value
            self._add_error(
                "ConstantCondition",
                node,
                f"Condition 'if {value}' is constant and may hide unreachable code.",
                "Replace with a real condition or remove the branch.",
            )
        self.generic_visit(node)

    def find_unused_variables(self) -> List[Dict[str, Any]]:
        """After visiting, check for unused vars."""
        unused = set(self.defined_vars.keys()) - self.used_vars
        for var in unused:
            line = self.defined_vars.get(var, "Unknown")
            self.errors.append(
                {
                    "type": "UnusedVariable",
                    "line": line,
                    "message": f"Variable '{var}' is defined but never used.",
                    "suggestion": f"Remove '{var}' or use it in your code.",
                }
            )
        return self.errors


def detect_errors(code_string: str) -> Dict[str, Any]:
    """Main function you'll call."""
    try:
        tree = ast.parse(code_string)
        finder = ErrorFinder()
        finder.visit(tree)

        errors = finder.find_unused_variables()

        return {
            "success": True,
            "errors": errors,
            "error_count": len(errors),
        }

    except SyntaxError:
        return {
            "success": False,
        }