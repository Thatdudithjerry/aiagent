import os
from google.genai.types import FunctionDeclaration, Schema, Type

schema_get_files_info = FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "directory": Schema(
                type=Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))
        # Guardrail: Ensure target is within working_directory
        if not abs_target_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        # Check if target is a directory
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a directory'
        entries = []
        for entry in os.listdir(abs_target_dir):
            entry_path = os.path.join(abs_target_dir, entry)
            try:
                is_dir = os.path.isdir(entry_path)
                file_size = os.path.getsize(entry_path)
                entries.append(f'- {entry}: file_size={file_size} bytes, is_dir={is_dir}')
            except Exception as e:
                entries.append(f'- {entry}: Error: {str(e)}')
        return "\n".join(entries)
    except Exception as e:
        return f'Error: {str(e)}'