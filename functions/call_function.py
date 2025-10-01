from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
  args = function_call_part.args or {}
  function_result = ""

  if verbose:
    print(f"Calling function: {function_call_part.name}({args})")
  else:
    print(f" - Calling function: {function_call_part.name}")

  if function_call_part.name == "get_files_info":
    function_result = {"files_info": get_files_info(working_directory="./calculator", **args)}
  
  elif function_call_part.name == "get_file_content":
    path = args.get("path") or args.get("file") or args.get("filepath") or args.get("file_path")
    content = get_file_content(working_directory="./calculator", **args)
    function_result = {"path": path, "content": content}
  
  elif function_call_part.name == "run_python_file":
    function_result = {"stdout": run_python_file(working_directory="./calculator", **args)}
  
  elif function_call_part.name == "write_file":
    function_result = {"result": write_file(working_directory="./calculator", **args)}
  
  else:
    
    return types.Content(
      role="tool",
      parts=[
          types.Part.from_function_response(
              name=function_call_part.name,
              response={"error": f"Unknown function: {function_call_part.name}"},
          )
        ],
      )
  
  return types.Content(
    role="user",
    parts=[
      types.Part(
        function_response=types.FunctionResponse(
          name=function_call_part.name,
          response=function_result,
        )
      )
    ],
  )