import os
from LLM_Configs import MAX_CHARS, WORKING_DIR
from google.genai import types

def get_file_content(file_path):
    try:
        root_path = os.path.abspath(WORKING_DIR)
        target_file_path = os.path.abspath(os.path.join(WORKING_DIR, file_path))
        
        if((target_file_path == root_path or target_file_path.startswith(root_path + os.sep)) and os.path.isfile(target_file_path)):
            try:
                with open(target_file_path, "r") as f:
                    file_contents = f.read(MAX_CHARS)
                    print(len(file_contents))
                    if len(file_contents) < 10000:
                        return file_contents
                    else:
                        final_string = file_contents+f'[...File "{file_path}" truncated at 10000 characters]'
                        print(len(final_string))
                        return final_string
            except Exception as e:
                return f"Error: {e}"
            
        elif not (os.path.isfile(target_file_path)):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content inside the file selected by the given file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file which needs to be read, relative to the working directory. If not provided, the function cannot be called as a file path is necessary. Request the user to provide file path.",
            ),
        },
    ),
)