import os

def get_files_info(working_directory, directory="."):
  try:
    relative_path = os.path.join(working_directory, directory)
    
    if not os.path.abspath(relative_path).startswith(os.path.abspath(working_directory)):
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(relative_path):
      return f'Error: "{directory}" is not a directory'
    
    file_names = os.listdir(relative_path)
    
    result = ""
    
    for file_name in file_names:
      file_path = os.path.join(relative_path, file_name)
      result += f'- {file_name}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n'
    
    return result
  except Exception as e:
    return f"Error: {e}"