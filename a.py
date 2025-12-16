import ast

node = ast.parse('x + y')
print(ast.dump(node, indent=2))