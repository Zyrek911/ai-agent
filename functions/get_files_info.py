import os

def get_files_info(working_directory, directory="."):
    try:
        root_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, directory))

        if(root_path == target_path or target_path.startswith(root_path+os.sep)):
            try:
                dir_list = [
                    entry for entry in os.listdir(target_path)
                    if not (entry == "__pycache__" or entry.startswith("."))
                    ]
                file_data = []

                for file in dir_list:
                    path_to_file = os.path.join(target_path, file)
                    f_size = os.path.getsize(path_to_file)
                    f_isdir = os.path.isdir(path_to_file)
                    file_data.append(f" - {file}: file_size={f_size} bytes, is_dir={f_isdir}")
            except Exception as e:
                return f"Error: {e}"

            formatted_data = "\n".join(file_data)
            return formatted_data
        
        elif not (os.path.isdir(target_path)):
            return f'Error: "{directory}" is not a directory'
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"