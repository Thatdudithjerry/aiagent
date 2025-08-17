import os
from config import MAX_FILE_CHARACTERS
from google.genai.types import FunctionDeclaration, Schema, Type

schema_get_file_content = FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file, constrained to the working directory.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "file_path": Schema(
                type=Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)
def get_file_content(working_directory, file_path):
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
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            # This happens when paths are on different drives (Windows)
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if file_path is a regular file
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read file contents
        with open(full_file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        if len(content) > MAX_FILE_CHARACTERS:
            truncated_content = content[:MAX_FILE_CHARACTERS]
            truncated_content += f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARACTERS} characters]'
            return truncated_content
        
        return content
        
    except Exception as e:
        return f'Error: {str(e)}'