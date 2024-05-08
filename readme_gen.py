import json
import logging
import subprocess
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

AI_MODEL = "claude-3-haiku-20240307"
AI_SYSTEM_TEMPLATE = """
Generate a comprehensive README.md file for the provided code. 
The README.md should include:
- A brief introduction to the project, including its purpose and functionality.
- Installation instructions, including any dependencies or prerequisites.
- Usage examples, including any command-line arguments or configuration options.
- A description of the code structure and organization.
- Any notable features, such as performance optimizations or security considerations.
- Information on how to contribute to the project, including reporting issues and submitting pull requests.
- A license statement, if applicable.
Please format the README.md using Markdown syntax and make it easy to read and understand.
"""


def generate_ai_message(file: str) -> str:
    """
    Generate a commit message using the AI
    model based on the provided git diff.

    Args:
        file (str): file content.

    Returns:
        str: The generated response.
    """
    client = anthropic.Anthropic(api_key=os.getenv("API_KEY"))

    message = client.messages.create(
        model=AI_MODEL,
        max_tokens=1500,
        temperature=0,
        system=AI_SYSTEM_TEMPLATE,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": file
                    }
                ]
            }
        ]
    )

    ai_message = message.content[0].text
    return ai_message


def main(source_file: str) -> str:
    """
    Main function to generate and apply the commit message.
    """
    script_dir = Path(__file__).resolve().parent
    readme = script_dir / "readme.md"
    with open(script_dir / source_file, 'r') as file:
        with open(readme, 'w') as doc:
            doc.write(generate_ai_message(str(file.read())))

if __name__ == "__main__":
    main("readme_gen.py")
