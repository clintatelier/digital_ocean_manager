import os
import sys

def collect_project_structure(root_dir):
    output = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip .git directories
        if '.git' in dirpath:
            continue
        
        # Add directory structure
        relative_path = os.path.relpath(dirpath, root_dir)
        if relative_path != '.':
            output.append(f"\n# Directory: {relative_path}")
        
        # Add file contents
        for filename in filenames:
            # Skip .git files
            if filename.endswith('.git'):
                continue
            
            file_path = os.path.join(dirpath, filename)
            relative_file_path = os.path.relpath(file_path, root_dir)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    output.append(f"\n# File: {relative_file_path}\n```\n{content}\n```\n")
            except Exception as e:
                output.append(f"\n# File: {relative_file_path}\n```\nError reading file: {str(e)}\n```\n")
    
    return "\n".join(output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python project_structure_collector.py <output_file>")
        sys.exit(1)
    
    root_dir = os.getcwd()
    output_file = sys.argv[1]
    
    project_structure = collect_project_structure(root_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(project_structure)
    
    print(f"Project structure and contents have been written to {output_file}")