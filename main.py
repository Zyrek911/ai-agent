import sys
import os
from LLM_Configs import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set. See README for setup.", file=sys.stderr)
        sys.exit(1)
    client = genai.Client(api_key=api_key)
    promptContents = sys.argv
    user_prompt = promptContents[1]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    if(len(promptContents) >= 2):
        messages = [types.Content(role="user", parts=[types.Part(text = user_prompt)])]
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents= messages,
            config= types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

        usage = response.usage_metadata
        promptTokens = usage.prompt_token_count
        responseTokens = usage.candidates_token_count

        if response.function_calls:
            fc = response.function_calls[0]
            print(f"Calling function: {fc.name}({fc.args})")
            if fc.name == "get_files_info":
                result = get_files_info(fc.args.get("directory", "."))
                
            if fc.name == "get_file_content":
                result = get_file_content(fc.args.get("file_path"))
                
            if fc.name == "write_file":
                result = write_file(fc.args.get("file_path"), fc.args.get("content"))
                
            if fc.name == "run_python_file":
                result = run_python_file(fc.args.get("file_path"), fc.args.get("args") or [])
            
            print(result)
            
        else:
            print(response.text)
        if("--verbose" in promptContents):
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {promptTokens}")
            print(f"Response tokens: {responseTokens}")
    else:
        print("Error:missing prompt.\nUsage: uv run main.py \"<write prompt here>\"", file=sys.stderr)
        sys.exit(1)

main()