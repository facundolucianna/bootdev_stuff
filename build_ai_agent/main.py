import os
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

def main():
    args = parser.parse_args()

    messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=args.prompt)])]

    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
