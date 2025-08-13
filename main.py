import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Check for --verbose flag
verbose = False
args = []
for arg in sys.argv[1:]:
    if arg == "--verbose":
        verbose = True
    else:
        args.append(arg)

if len(args) < 1:
    print("Error: Prompt argument is required.")
    sys.exit(1)

prompt = args[0]

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt
)

print(response.text)

if verbose:
    print(f'User prompt: {prompt}')
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
