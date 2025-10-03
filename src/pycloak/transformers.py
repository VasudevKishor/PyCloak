import ast
import random
import string
import base64

# --- Helper Functions ---
# (generate_random_name and create_decryptor_preamble are unchanged)
def generate_random_name(length=4):
    """Generates a short, random name like '_xYz1'."""
    chars = string.ascii_letters + string.digits
    return '_' + ''.join(random.choice(chars) for _ in range(length))

def create_decryptor_preamble(data_list):
    """Creates the AST nodes for the decryption runtime code."""
    preamble_code = f"""
import base64
_e = {data_list}
def _d(i):
    return base64.b64decode(_e[i]).decode('utf-8')
"""
    return ast.parse(preamble_code).body

# --- Transformer Classes ---

class StringEncryptor(ast.NodeTransformer):
    """
    Finds all string constants and replaces them with a decryptor call,
    but intelligently skips strings inside f-strings.
    """
    def __init__(self):
        super().__init__()
        self.encrypted_strings = []
        self._in_f_string = False  # Flag to track if we are inside an f-string

    def visit_JoinedStr(self, node: ast.JoinedStr):
        # When we enter an f-string, set a flag so we don't transform its parts
        self._in_f_string = True
        self.generic_visit(node)  # Visit the children of the f-string
        self._in_f_string = False # Unset the flag when we leave
        return node

    def visit_Constant(self, node: ast.Constant):
        # Only encrypt if it's a string AND we are NOT inside an f-string
        if isinstance(node.value, str) and not self._in_f_string:
            encoded_string = base64.b64encode(node.value.encode('utf-8')).decode('utf-8')
            try:
                index = self.encrypted_strings.index(encoded_string)
            except ValueError:
                self.encrypted_strings.append(encoded_string)
                index = len(self.encrypted_strings) - 1
            
            return ast.Call(
                func=ast.Name(id='_d', ctx=ast.Load()),
                args=[ast.Constant(value=index)],
                keywords=[]
            )
        return node

# (GlobalRenamer, LocalVariableRenamer, and NameApplier classes are unchanged below)
class GlobalRenamer(ast.NodeTransformer):
    """Applies a global rename map to definitions, calls, attributes, and imports."""
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

class LocalVariableRenamer(ast.NodeTransformer):
    """An AST transformer that renames local variables and arguments within functions."""
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
    """A dedicated visitor to apply a given rename map to all Name nodes."""
    def __init__(self, rename_map):
        self.rename_map = rename_map
    def visit_Name(self, node: ast.Name):
        if node.id in self.rename_map:
            node.id = self.rename_map[node.id]
        return node