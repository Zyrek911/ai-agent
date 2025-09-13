import sys
import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set. See README for setup.", file=sys.stderr)
        sys.exit(1)
    client = genai.Client(api_key=api_key)
    promptContents = sys.argv

    if(len(promptContents) == 2):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents= promptContents[1]
        )

        usage = response.usage_metadata
        promptTokens = usage.prompt_token_count
        responseTokens = usage.candidates_token_count

        print(response.text)
        print(f"Prompt tokens: {promptTokens}")
        print(f"Response tokens: {responseTokens}")
    else:
        print("Error:missing prompt.\nUsage: uv run main.py \"<write prompt here>\"", file=sys.stderr)
        sys.exit(1)

main()