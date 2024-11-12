import os

def create_structure_from_tree(tree_file):
    with open(tree_file, 'r') as file:
        lines = file.readlines()

    # Initialize variables
    path_stack = []
    previous_indent = 0

    # Process each line in the directory structure
    for index, line in enumerate(lines):
        if not line.strip():
            continue

        stripped_line = line.rstrip('\n')
        indent_level = len(line) - len(line.lstrip(' │├└'))

        # Remove higher-level paths from the stack
        while path_stack and indent_level <= path_stack[-1][0]:
            path_stack.pop()

        # Get the current name
        name = stripped_line.strip(' │├└─')

        # Build the current path
        if path_stack:
            current_path = os.path.join(path_stack[-1][1], name)
        else:
            current_path = name  # This is the root directory

        # Add current path to the stack
        path_stack.append((indent_level, current_path))

        # Check if it's a file or directory
        if '.' in name and not name.endswith('/'):
            # It's a file
            dir_name = os.path.dirname(current_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            with open(current_path, 'w') as f:
                pass
        else:
            # It's a directory
            if not os.path.exists(current_path):
                os.makedirs(current_path, exist_ok=True)

if __name__ == "__main__":
    create_structure_from_tree('directory_structure.txt')
