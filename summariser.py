# Built by Wande — Week 4 of AI Skills Journey — March 2026
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

print('\nYou can now ask questions about this document.')
print('Type quit to exit')

doc_history = [
    {'role': 'user', 'content': f'Here is a document:\n\n{content}'},
    {'role': 'assistant', 'content': response.content[0].text}
]

while True:
    question = input('\nYour question:')

    if question.lower() == 'quit':
        print("Goodbye!")
        break
    doc_history.append({'role': 'user', 'content': question})

    follow_up = client.messages.create(
        model = 'claude-opus-4-6',
        max_tokens =1024,
        messages=doc_history

    )

    answer = follow_up.content[0].text
    print('\nClaude:', answer)

    doc_history.append({'role':'assistant', 'content': answer})