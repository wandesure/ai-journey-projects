import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

system_prompt = """
You are an expert security and compliance analyst with deep knowledge of:
- NIST SP 800-53 controls
- ISO 27001 requirements
- CIS Controls v8
- SOC 2 Type II criteria

When given a security policy or procedure:
1. Identify which compliance frameworks it relates to
2. List what requirements are MET
3. List what requirements are MISSING or GAP
4. Give a compliance score out of 10
5. Provide specific improvement recommendations
"""
print("🔒 AI Security Compliance Checker")
print("=================================")

print("Print your security policy below.")
print("When done type END on a new line")

lines =[]

while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)


policy_text = '\n'.join(lines)

print('\n🔍 Analysing against compliance frameworks...')

response = client.messages.create(
    model = "claude-opus-4-6",
    max_tokens= 2048,
    system = system_prompt,
    messages=[
        {"role":"user","content": f"Please analyse this security policy:\n\n{policy_text}"}

    ]

)
print('\n📋 Compliance Analysis:')
print(response.content[0].text)

print('\nYou can now ask follow-up questions about the compliance gaps.')
print('Type quit to exit')

comp_history = [
    {'role': 'user', 'content': f'Analyse this policy:\n\n{policy_text}'},
    {'role': 'assistant', 'content': response.content[0].text}
]

while True:
    question = input('\nYour question: ')
    if question.lower() == 'quit':
        print('Goodbye!')
        break
    comp_history.append({'role': 'user', 'content': question})
    follow_up = client.messages.create(
        model='claude-opus-4-6',
        max_tokens=1024,
        system=system_prompt,
        messages=comp_history
    )
    answer = follow_up.content[0].text
    print('\nClaude:', answer)
    comp_history.append({'role': 'assistant', 'content': answer})

