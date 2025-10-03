import ast
import random
import string

def generate_random_name(length=4):
    """Generates a short, random name like '_xYz1'."""
    chars = string.ascii_letters + string.digits
    return '_' + ''.join(random.choice(chars) for _ in range(length))

class LocalVariableRenamer(ast.NodeTransformer):
    """
    An AST transformer that renames local variables and arguments within functions.
    (We are keeping this class for future use or single-file operations)
    """
    def visit_FunctionDef(self, node: ast.FunctionDef):
        rename_map = {}
        for arg in node.args.args:
            if arg.arg != 'self':
                rename_map[arg.arg] = generate_random_name()

        for body_node in ast.walk(node):
            if isinstance(body_node, ast.Assign):
                for target in body_node.targets:
                    if isinstance(target, ast.Name) and target.id not in rename_map:
                        rename_map[target.id] = generate_random_name()

        for arg in node.args.args:
            if arg.arg in rename_map:
                arg.arg = rename_map[arg.arg]

        applier = NameApplier(rename_map)
        node.body = [applier.visit(statement) for statement in node.body]
        return node

class NameApplier(ast.NodeTransformer):
    """
    A dedicated visitor to apply a given rename map to all Name nodes.
    """
    def __init__(self, rename_map):
        self.rename_map = rename_map

    def visit_Name(self, node: ast.Name):
        if node.id in self.rename_map:
            node.id = self.rename_map[node.id]
        return node

class GlobalRenamer(ast.NodeTransformer):
    """
    Applies a global rename map to definitions, calls, attributes, and imports.
    """
    def __init__(self, rename_map):
        self.rename_map = rename_map

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name in self.rename_map:
            node.name = self.rename_map[node.name]
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name in self.rename_map:
            node.name = self.rename_map[node.name]
        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name):
        if node.id in self.rename_map:
            node.id = self.rename_map[node.id]
        return node

    def visit_Attribute(self, node: ast.Attribute):
        if node.attr in self.rename_map:
            node.attr = self.rename_map[node.attr]
        self.generic_visit(node)
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            if alias.name in self.rename_map:
                alias.name = self.rename_map[alias.name]
        self.generic_visit(node)
        return node