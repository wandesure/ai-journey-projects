import anthropic
import os
from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
filename = input('Enter filename to summarise:')

try:
    with open(filename, 'r',encoding='utf-8') as file:
        content = file.read()
except FileNotFoundError:
    print(f'Sorry- could not find {filename}')
    print(f'Please check the filename and try again')
    exit()


print('\nSending to Claude for summary...')

response = client.messages.create(
    model='claude-opus-4-6',
    max_tokens=1024,
    system="You are an expert summariser. Give clear, concise summaries with key points.",
    messages=[
        {'role': 'user','content':f'Please summarise this document:\n\n{content}'}
    ]

)

print('\n📋 Summary')
print(response.content[0].text)
