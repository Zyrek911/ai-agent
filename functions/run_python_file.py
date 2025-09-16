import os
import subprocess
from LLM_Configs import WORKING_DIR
from google.genai import types

def run_python_file(file_path, args=[]):
    try:
        root_path = os.path.abspath(WORKING_DIR)
        target_file_path = os.path.abspath(os.path.join(WORKING_DIR, file_path))

        if not(root_path == target_file_path or target_file_path.startswith(root_path + os.sep)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not(os.path.isfile(target_file_path)):
            return f'Error: File "{file_path}" not found.'

        if(target_file_path[-3:] != ".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            cp = subprocess.run(["python", file_path, *args], cwd=WORKING_DIR, timeout=30, capture_output=True, text=True)
            STDOUT = cp.stdout
            STDERR = cp.stderr
            if not STDOUT and not STDERR:
                return "No output produced."
            RETURN_CODE = cp.returncode
            if RETURN_CODE != 0:
                return f"STDOUT:{STDOUT}\nSTDERR:{STDERR}\nProcess exited with code {RETURN_CODE}"
            return f"STDOUT:{STDOUT}\nSTDERR:{STDERR}"    
        except Exception as e:
            return f'Error: executing python file: {e}'
        
    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file selected by the given file path with any optional arguments that might be provided, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file which needs to be run, relative to the working directory. File should be a python file ending with .py .If not provided, the function cannot be called as a file path is necessary.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional. It is an array containing the required arguments for the python file.",
                items=types.Schema(type=types.Type.STRING),
            )
        },
        required=["file_path"]
    ),
)