import os
from google.genai.types import FunctionDeclaration, Schema, Type

schema_write_file = FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, constrained to the working directory.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "file_path": Schema(
                type=Type.STRING,
                description="The path where to write the file, relative to the working directory.",
            ),
            "content": Schema(
                type=Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)

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