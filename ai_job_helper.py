# Built by Wande — Week 3 of AI Skills Journey — March 2026
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))



print("🤖 AI Job Helper")
print("=================")
while True:

    task = input("\nWhat work task do you need help with? ")
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system="You are an expert assistant. Give practical, concise advice.",
        messages=[
            {"role": "user", "content": task}
        ]
    )

    print("\nClaude says:")
    print(message.content[0].text)
    while True:
        another = input("\nDo you have another question? (yes/no) ")
        
        if another.lower() == "yes":
            break
        elif another.lower() == "no":
            print("\nGood luck! 👋")
            exit()
        else:
            print("Please type yes or no — try again!")
        
    