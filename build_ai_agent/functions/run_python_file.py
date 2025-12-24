import os
import subprocess
from google import genai

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_path = os.path.commonpath([absolute_path, target_path]) == absolute_path

        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args:
            command.extend(args)

        process = subprocess.run(command, capture_output=True, text=True, timeout=30)

        stdout = process.stdout
        stderr = process.stderr

        output = ""
        if process.returncode != 0:
            output = f"Process exited with code {process.returncode}"

        if not stdout and not stderr:
            output += "No output produced"

        if stdout:
            output += f"STDOUT: {stdout}"

        if stderr:
            output += f"STDERR: {stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file relative to the working directory",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="File path to run, relative to the working directory",
            ),
            "args": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                items=genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="Optional arguments to pass to the Python file",
                ),
                description="Optional arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)