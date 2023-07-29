import os

import openai
from click import Choice, command, option, version_option
from dotenv import load_dotenv
from rich.console import Console


@command()
@version_option(version='0.1.0')
@option(
    '-m', '--model',
    type=Choice(['gpt-3.5-turbo', 'gpt-4']),
    default='gpt-3.5-turbo',
    help='model you want use'
)
def main() -> None:
    load_dotenv()
    console = Console()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    model = 'gpt-3.5-turbo'
    messages = []
    lines = []
    while line := input('user >> '):
        line = line.strip()
        if '!send' == line:
            messages.append({
                'role': 'user',
                'content': "\n".join(lines)
            })
            lines = []

            result = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0,
                stream=True
            )

            print("assistant >> ", end="")
            assistant_response = ""
            with console.status("[bold green]Asking..."):
                for chunk in result:
                    chunk_str = chunk["choices"][0]["delta"].get("content", "")
                    assistant_response += chunk_str
                    print(chunk_str, end="")
            messages.append({
                'role': 'assistant',
                'content': assistant_response
            })
        lines.append(line)
