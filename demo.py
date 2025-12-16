import ast

code = """
def greet(name):
    return f"Hello {name}!"

print(greet("World"))
"""

tree = ast.parse(code)
print(ast.dump(tree, indent=2))