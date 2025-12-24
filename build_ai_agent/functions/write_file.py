import os
from config import MAX_CHARS
from google import genai

def write_file(working_directory, file_path, content):
    try:
        absolute_path =os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

        if not valid_target_dir:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)

        with open(target_dir, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'


schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file relative to the working directory",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)