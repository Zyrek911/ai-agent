from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def show(header, result):
    print(header)
    if result.startswith("Error:"):
        print(f"    {result}")
    else:
        print(result)

#No Tests Currently