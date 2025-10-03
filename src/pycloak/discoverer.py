import ast
import os
from typing import Set

class NameCollector(ast.NodeVisitor):
    """
    An AST visitor that collects the names of all functions and classes defined.
    """
    def __init__(self):
        self.defined_names: Set[str] = set()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Add the function's name to our set
        self.defined_names.add(node.name)
        # Continue traversing inside the function for nested definitions
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        # Add the class's name to our set
        self.defined_names.add(node.name)
        # Also visit the methods inside the class
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.visit_FunctionDef(item)

class ProjectDiscoverer:
    """
    Discovers all user-defined class and function names within a project directory.
    """
    def discover(self, project_path: str) -> Set[str]:
        all_names = set()
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        source_code = f.read()
                        tree = ast.parse(source_code)
                        
                        collector = NameCollector()
                        collector.visit(tree)
                        all_names.update(collector.defined_names)
        
        return all_names