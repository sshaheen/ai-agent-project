import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from function_call_schema import available_functions, schema_get_files_info
from functions.call_function import call_function

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    if len(sys.argv) == 1:
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = len(sys.argv) == 3 and sys.argv[2] == "--verbose"
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    try:
        for x in range(20):
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
                )
            
            for candidate in response.candidates:
                messages.append(candidate.content)
            
            if not response.function_calls:
                if response.text:
                    print(response.text)
                    break
                else:
                    continue
            
            for fc in response.function_calls:
                tool_msg = call_function(fc, verbose)
                messages.append(tool_msg)

                if not tool_msg.parts[0].function_response.response:
                    raise Exception("Fatal Exception")
                    
                if verbose:
                    print(f"-> {tool_msg.parts[0].function_response.response}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
