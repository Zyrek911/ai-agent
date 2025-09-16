import os
from LLM_Configs import WORKING_DIR
from google.genai import types

def write_file(file_path, content):
    try:
        root_path = os.path.abspath(WORKING_DIR)
        target_file_path = os.path.abspath(os.path.join(WORKING_DIR, file_path))
        target_file_dir = os.path.dirname(target_file_path)
        
        if not(root_path == target_file_path or target_file_path.startswith(root_path + os.sep)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        try:
            os.makedirs(target_file_dir, exist_ok=True)
            with open(target_file_path, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
        
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the givent content to the file selected by the file path provided, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file which needs to be written into, relative to the working directory. If not provided, the function cannot be called as a file path is necessary. Request the user to provide file path.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content which needs to be written into the file. If not provided, the function will not work as content is required. Request user to provide the content."
            )
        },
    ),
)