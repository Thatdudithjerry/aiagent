import os
import subprocess
from google.genai.types import FunctionDeclaration, Schema, Type
schema_run_python_file = FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its output, constrained to the working directory.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "file_path": Schema(
                type=Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": Schema(
                type=Type.ARRAY,
                description="Optional command line arguments to pass to the Python script.",
                items=Schema(type=Type.STRING),
            ),
        },
        required=["file_path"]
    ),
)
def run_python_file(working_directory, file_path, args=[]):
 
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
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            # This happens when paths are on different drives (Windows)
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check if file exists
        if not os.path.isfile(full_file_path):
            return f'Error: File "{file_path}" not found.'
        
        # Check if file is a Python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Build command
        cmd = ['python', full_file_path] + args
        
        # Execute the Python file
        completed_process = subprocess.run(
            cmd,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Format output
        output_parts = []
        
        # Add stdout if present
        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")
        
        # Add stderr if present
        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr}")
        
        # Add exit code if non-zero
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
        
        # Return formatted output or "No output produced." if empty
        if output_parts:
            return '\n'.join(output_parts)
        else:
            return "No output produced."
    
    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"