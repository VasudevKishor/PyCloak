"""
import ast # 1. Import Python's tool for understanding code structure
from pycloak.transformers import LocalVariableRenamer # 2. Import the class we will write

# 3. A simple string containing the Python code we want to obfuscate
SOURCE_CODE = """"""
def calculate_salary(base_pay, bonus, tax_rate):
    gross_salary = base_pay + bonus
    tax_deduction = gross_salary * tax_rate
    net_salary = gross_salary - tax_deduction
    return net_salary
    for i in range(5):
        print(i)
        """
"""

if __name__ == "__main__":
    # This block runs our test
    
    # 4. PARSE: Takes the code string and turns it into a tree-like structure
    tree = ast.parse(SOURCE_CODE)

    # 5. TRANSFORM: This is the magic. We tell our transformer to visit and modify the tree
    transformer = LocalVariableRenamer()
    obfuscated_tree = transformer.visit(tree)
    
    # 6. FIX: A required helper step to clean up the modified tree
    ast.fix_missing_locations(obfuscated_tree)

    # 7. UNPARSE: Turns the modified tree back into a string of code
    obfuscated_code = ast.unparse(obfuscated_tree)

    print("\n--- Obfuscated Code (v0.1) ---")
    print(obfuscated_code)
"""
from pycloak.discoverer import ProjectDiscoverer
from pycloak.transformers import generate_random_name # We'll reuse this

def create_rename_map(names):
    """Takes a set of names and creates a map to new, random names."""
    return {name: generate_random_name() for name in names}

if __name__ == "__main__":
    
    PROJECT_PATH = "./sample_app"
    
    print(f"--- Running Discovery on '{PROJECT_PATH}' ---")
    
    # 1. Discover all function and class names in the project
    discoverer = ProjectDiscoverer()
    project_names = discoverer.discover(PROJECT_PATH)
    
    print("\n[+] Discovered Names:")
    for name in sorted(list(project_names)):
        print(f"  - {name}")
    
    # 2. Create the global rename map
    global_rename_map = create_rename_map(project_names)
    
    print("\n[+] Generated Rename Map:")
    for old, new in global_rename_map.items():
        print(f"  - {old} -> {new}")