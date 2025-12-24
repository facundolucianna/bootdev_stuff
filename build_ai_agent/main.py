import os
from dotenv import load_dotenv
from google import genai
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

config=genai.types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

def main():
    args = parser.parse_args()

    messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=args.prompt)])]

    response = client.models.generate_content(model="gemini-2.5-flash", 
                                             contents=messages,
                                             config=config)
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        function_call_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            if len(function_call_result.parts) == 0:
                raise RuntimeError("Function call output is empty")
            
            if not function_call_result.parts[0].function_response:
                raise RuntimeError("Function call output is empty")

            if not function_call_result.parts[0].function_response.response:
                raise RuntimeError("Function call output is empty")

            function_call_responses.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    print(response.text)


if __name__ == "__main__":
    main()
