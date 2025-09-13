import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set. See README for setup.", file=sys.stderr)
        sys.exit(1)
    client = genai.Client(api_key=api_key)
    promptContents = sys.argv
    user_prompt = promptContents[1]

    if(len(promptContents) >= 2):
        messages = [types.Content(role="user", parts=[types.Part(text = user_prompt)])]
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents= messages
        )

        usage = response.usage_metadata
        promptTokens = usage.prompt_token_count
        responseTokens = usage.candidates_token_count

        print(response.text)
        if("--verbose" in promptContents):
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {promptTokens}")
            print(f"Response tokens: {responseTokens}")
    else:
        print("Error:missing prompt.\nUsage: uv run main.py \"<write prompt here>\"", file=sys.stderr)
        sys.exit(1)

main()