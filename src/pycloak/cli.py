import ast
import os
import shutil
import click  # Import the click library

from .discoverer import ProjectDiscoverer
from .transformers import (
    generate_random_name, 
    GlobalRenamer, 
    StringEncryptor, 
    create_decryptor_preamble
)

def create_rename_map(names):
    """Takes a set of names and creates a map to new, random names."""
    return {name: generate_random_name() for name in names}

@click.command()
@click.option('--source', 'source_dir', required=True, type=click.Path(exists=True, file_okay=False), help='The source directory to obfuscate.')
@click.option('--output', 'output_dir', required=True, type=click.Path(), help='The output directory for obfuscated files.')
def main(source_dir, output_dir):
    """A powerful and modern obfuscator for Python source code."""
    
    click.echo(f"▶️  Starting PyCloak...")

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Pass 1: Discovery
    click.echo(f"🔎 Running Discovery on '{source_dir}'...")
    discoverer = ProjectDiscoverer()
    project_names = discoverer.discover(source_dir)
    global_rename_map = create_rename_map(project_names)
    click.echo(f"✅ Discovered and mapped {len(project_names)} global names.")

    # Pass 2: Transformation
    click.echo(f"🛡️  Running Transformation, writing to '{output_dir}'...")
    os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        current_output_dir = os.path.join(output_dir, relative_path)
        
        for d in dirs:
            os.makedirs(os.path.join(current_output_dir, d), exist_ok=True)

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                    
                    # Transformation Pipeline
                    global_renamer = GlobalRenamer(global_rename_map)
                    tree = global_renamer.visit(tree)
                    
                    string_encryptor = StringEncryptor()
                    tree = string_encryptor.visit(tree)
                    
                    encrypted_data = string_encryptor.encrypted_strings
                    if encrypted_data:
                        preamble = create_decryptor_preamble(encrypted_data)
                        tree.body = preamble + tree.body

                    ast.fix_missing_locations(tree)
                    
                    output_path = os.path.join(current_output_dir, file)
                    obfuscated_code = ast.unparse(tree)
                    with open(output_path, "w", encoding="utf-8") as out_f:
                        out_f.write(obfuscated_code)

    click.secho(f"\n🎉 Transformation complete! Obfuscated project is in '{output_dir}'", fg="green")

if __name__ == '__main__':
    main()