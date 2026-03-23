# Built by Wande — Week 3 of AI Skills Journey — March 2026

import anthropic
import os
from dotenv import load_dotenv
load_dotenv()
conversation_history = []
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
print('🤖 AI Chatbot — I remember our conversation!')
print('Type quit to exit')
print('================================')

while True:
    user_input = input('\nYou:')
    
    if user_input.lower() == 'quit':
        print('Goodbye!')
        break
    conversation_history.append(
        {'role':'user','content':user_input}
    )

    if len(conversation_history)> 20:
        conversation_history = conversation_history[-20:]

    response = client.messages.create(
        model='claude-opus-4-6',
        max_tokens=1024,
        system='You are a helpful assistant with a great memory.',
        messages=conversation_history
    )
    
    assistant_message=response.content[0].text
    print("Claude:", assistant_message)
    
    conversation_history.append(
        {'role': 'assistant', 'content':assistant_message}
    )
    print(f'[Message {len(conversation_history)//2} of conversation]')

