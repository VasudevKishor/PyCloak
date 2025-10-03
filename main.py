import ast
import os
from pycloak.discoverer import ProjectDiscoverer
from pycloak.transformers import generate_random_name, GlobalRenamer

def create_rename_map(names):
    """Takes a set of names and creates a map to new, random names."""
    return {name: generate_random_name() for name in names}

if __name__ == "__main__":
    
    SOURCE_DIR = "./sample_app"
    OUTPUT_DIR = "./obfuscated_app"
    
    print(f"--- Running Discovery on '{SOURCE_DIR}' ---")
    
    # PASS 1: DISCOVERY
    discoverer = ProjectDiscoverer()
    project_names = discoverer.discover(SOURCE_DIR)
    global_rename_map = create_rename_map(project_names)
    
    print(f"\n--- Running Transformation, writing to '{OUTPUT_DIR}' ---")
    
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # PASS 2: TRANSFORMATION
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, SOURCE_DIR)
                output_path = os.path.join(OUTPUT_DIR, relative_path)
                
                print(f"  - Processing {file_path} -> {output_path}")

                with open(file_path, "r", encoding="utf-8") as f:
                    source_code = f.read()
                    tree = ast.parse(source_code)
                    
                    # Apply the global renames
                    transformer = GlobalRenamer(global_rename_map)
                    obfuscated_tree = transformer.visit(tree)
                    ast.fix_missing_locations(obfuscated_tree)
                    
                    # Write the obfuscated code to the new file
                    obfuscated_code = ast.unparse(obfuscated_tree)
                    with open(output_path, "w", encoding="utf-8") as out_f:
                        out_f.write(obfuscated_code)

    print("\n[+] Transformation complete!")