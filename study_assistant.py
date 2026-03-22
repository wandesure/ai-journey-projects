import anthropic
from dotenv import load_dotenv
load_dotenv()
import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
print("🤖 Your Personal AI Study Assistant")
print("=====================================")

question = input("What AI concept do you want to understand better today? ")

message = client.messages.create (
    model="claude-opus-4-6",

    max_tokens=1024,

    messages=[
        {"role": "user", "content": question}
    ],
    system="You are a friendly AI tutor teaching a beginner. Always explain concepts in plain English using simple real-world analogies. Keep answers short and clear. End with one follow-up question to check understanding."
)

print("\nClaude says:")
print(message.content[0].text)