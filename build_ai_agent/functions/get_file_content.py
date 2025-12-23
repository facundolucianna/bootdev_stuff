import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        absolute_path =os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" is not a file'

        with open(target_dir, 'r') as file:
            file_content = file.read(MAX_CHARS)

            if file.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content

    except Exception as e:
        return f'Error: {e}'
