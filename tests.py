import os
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from config import MAX_FILE_CHARACTERS

def write_file(working_directory, file_path, content):
    """
    Write content to a file within the specified working directory.
    
    Args:
        working_directory (str): The permitted working directory
        file_path (str): Path to the file (relative to working_directory or absolute)
        content (str): Content to write to the file
    
    Returns:
        str: Success message or error message
    """
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        
        # If file_path is relative, join it with working_directory first
        if not os.path.isabs(file_path):
            full_file_path = os.path.join(working_directory, file_path)
        else:
            full_file_path = file_path
        
        full_file_path = os.path.abspath(full_file_path)
        
        # Check if file_path is inside working_directory
        try:
            common_path = os.path.commonpath([working_directory, full_file_path])
            if common_path != working_directory:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            # This happens when paths are on different drives (Windows)
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create directory structure if it doesn't exist
        directory = os.path.dirname(full_file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write content to file
        with open(full_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except PermissionError:
        return f'Error: Permission denied when writing to "{file_path}"'
    except Exception as e:
        return f'Error: {str(e)}'

def main():
    # Test 1: Run main.py without arguments (should show usage instructions)
    result = run_python_file("calculator", "main.py")
    print(f"Test 1 - main.py: {result}")
    print()
    
    # Test 2: Run main.py with calculation argument
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(f"Test 2 - main.py with '3 + 5': {result}")
    print()
    
    # Test 3: Run tests.py
    result = run_python_file("calculator", "tests.py")
    print(f"Test 3 - tests.py: {result}")
    print()
    
    # Test 4: Try to run ../main.py (should error - outside directory)
    result = run_python_file("calculator", "../main.py")
    print(f"Test 4 - ../main.py: {result}")
    print()
    
    # Test 5: Try to run nonexistent.py (should error - file not found)
    result = run_python_file("calculator", "nonexistent.py")
    print(f"Test 5 - nonexistent.py: {result}")
    print()

if __name__ == "__main__":
    main()