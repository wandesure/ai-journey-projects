# Built by Wande-This script calls the Claude API and answers work-related questions
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
user_question = input('Ask Claude anything: ')
message = client.messages.create(
      model='claude-opus-4-6',
      system='You are an expert in the field of medical science who repond to people diagnosis',
      max_tokens=1024,
      messages=[
          {'role': 'user', 'content': user_question}
      ]
  )

print('Claue says:', message.content[0].text)
