import os
from google import genai

def get_files_info(working_directory, directory="."):
    try:
        absolute_path =os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_info = ""
        for file_name in os.listdir(target_dir):

            size_file = os.path.getsize(os.path.join(target_dir, file_name))
            is_dir = os.path.isdir(os.path.join(target_dir, file_name))

            files_info += f"{file_name}: file_size={size_file}, is_dir={is_dir}\n"
        
        files_info = files_info[:-1]
        
        return files_info

    except Exception as e:
        return f'Error: {e}'

    
schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    )
)