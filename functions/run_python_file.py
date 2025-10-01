import os
import subprocess
TIMEOUT_DUR = 30

def run_python_file(working_directory, file_path, args=[]):
  try:
    relative_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(relative_path).startswith(os.path.abspath(working_directory)):
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(relative_path):
      return f'Error: File "{file_path}" not found.'
    
    if not relative_path.endswith(".py"):
      return f'Error: "{file_path}" is not a Python file.'
    
    result = ""

    completed_process = subprocess.run(["python3", file_path, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory, timeout=TIMEOUT_DUR)
    stdout_msg = completed_process.stdout.decode()
    stderr_msg = completed_process.stderr.decode()
    
    if stdout_msg == stderr_msg == "":
      return "\nNo output produced"
    
    if stdout_msg:
      result += f"STDOUT: {stdout_msg}"
    
    if stderr_msg:
      result += f"STDERR: {stderr_msg}"
    
    if completed_process.returncode != 0:
      result += f"Process exited with code {completed_process.returncode}"
    
    return result
  except Exception as e:
    return f"Error: executing Python file: {e}"