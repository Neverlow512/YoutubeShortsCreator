import os
import argparse

def parse_arguments():
    """
    Parses command-line arguments.
    
    Returns:
        args: Parsed arguments containing output file name.
    """
    parser = argparse.ArgumentParser(description="Capture directory structure and script contents.")
    parser.add_argument(
        '-o', '--output',
        default='output.txt',
        help='Name of the output text file (default: output.txt).'
    )
    return parser.parse_args()

def get_user_input(prompt_text, default=None):
    """
    Prompts the user for input with an optional default value.
    
    Args:
        prompt_text (str): The message displayed to the user.
        default (str, optional): The default value if the user provides no input.
    
    Returns:
        str: The user's input or the default value.
    """
    if default:
        prompt = f"{prompt_text} [{default}]: "
    else:
        prompt = f"{prompt_text}: "
    response = input(prompt).strip()
    if not response and default is not None:
        return default
    return response

def is_excluded(dirpath, excluded_dirs):
    """
    Determines if the current directory should be excluded.
    
    Args:
        dirpath (str): The current directory path.
        excluded_dirs (list): List of directory names to exclude.
    
    Returns:
        bool: True if the directory is to be excluded, False otherwise.
    """
    for excluded in excluded_dirs:
        if os.path.basename(dirpath).lower() == excluded.lower():
            return True
    return False

def traverse_directories(root_dir, excluded_dirs, include_parent, output_file):
    """
    Traverses directories, captures script files and their contents, and writes to the output file.
    
    Args:
        root_dir (str): The root directory from which to start traversal.
        excluded_dirs (list): List of directory names to exclude.
        include_parent (bool): Whether to include scripts from the parent directory.
        output_file (str): Path to the output text file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        # If including parent directory scripts
        if include_parent:
            parent_scripts = [file for file in os.listdir(root_dir) 
                              if file.endswith('.py') and file != 'grab_structure.py']
            if parent_scripts:
                f.write(f"{root_dir}\n")
                f.write("-" * len(root_dir) + "\n")
                for script in parent_scripts:
                    file_path = os.path.join(root_dir, script)
                    f.write(f"{script}:\n")
                    f.write("```python\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as script_file:
                            content = script_file.read()
                        f.write(content)
                    except Exception as e:
                        f.write(f"# Error reading file: {e}\n")
                    f.write("```\n\n")
        
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Modify dirnames in-place to skip excluded directories
            dirnames[:] = [d for d in dirnames if not is_excluded(os.path.join(dirpath, d), excluded_dirs)]
            
            # Skip the current directory if it was included as parent
            if include_parent and os.path.abspath(dirpath) == os.path.abspath(root_dir):
                continue
            
            # Write the current directory path
            f.write(f"{dirpath}\n")
            f.write("-" * len(dirpath) + "\n")
            
            # Process each file in the current directory
            for filename in filenames:
                # Exclude grab_structure.py
                if filename == 'grab_structure.py':
                    continue
                # Modify this condition based on the script file types you want to include
                if filename.endswith('.py'):
                    file_path = os.path.join(dirpath, filename)
                    f.write(f"{filename}:\n")
                    f.write("```python\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as script_file:
                            content = script_file.read()
                        f.write(content)
                    except Exception as e:
                        f.write(f"# Error reading file: {e}\n")
                    f.write("```\n\n")
            f.write("\n\n")  # Add extra spacing between directories

def main():
    """
    The main function to execute the script with interactive prompts.
    """
    args = parse_arguments()
    output_file = args.output
    root_dir = os.getcwd()  # Current working directory

    print(f"Starting traversal from: {root_dir}\n")

    # Prompt to exclude directories
    exclude_response = get_user_input("Do you want to exclude any folders from traversal? (yes/no)", default="no").lower()
    excluded_dirs = []
    if exclude_response in ['yes', 'y']:
        exclude_input = get_user_input("Enter the folder names to exclude, separated by commas:")
        # Split by commas and strip whitespace
        excluded_dirs = [dir_name.strip() for dir_name in exclude_input.split(',') if dir_name.strip()]
        print(f"Excluded directories: {', '.join(excluded_dirs)}\n")
    
    # Prompt to include parent directory scripts
    include_parent_response = get_user_input("Do you want to include scripts present in the current directory? (yes/no)", default="no").lower()
    include_parent = include_parent_response in ['yes', 'y']
    if include_parent:
        print("Scripts from the current directory will be included.\n")
    else:
        print("Scripts from the current directory will be excluded.\n")
    
    print(f"Output will be saved to: {output_file}\n")

    traverse_directories(root_dir, excluded_dirs, include_parent, output_file)
    print(f"Traversal complete. Output saved to {output_file}")

if __name__ == "__main__":
    main()
