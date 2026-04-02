# ============================================
# AI Security Compliance Checker
# Author: Wande Oluwatomi
# Date: April 2026
# Description: Analyses security policies against
# major compliance frameworks using Claude AI
# Frameworks: NIST SP 800-53, ISO 27001,
#             CIS Controls v8, SOC 2 Type II
# ============================================

# --- Load environment variables and initialise Claude client ---
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# --- System prompt: defines Claude's role as compliance analyst ---
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
# --- Display tool header ---
print("🔒 AI Security Compliance Checker")
print("=================================")

# --- Collect security policy input from user ---
print("Print your security policy below.")
print("When done type END on a new line")

# --- Store input lines until END is typed ---
lines =[]

while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

# --- Join lines into single policy document ---
policy_text = '\n'.join(lines)

# --- Send policy to Claude for initial analysis ---
print('\n🔍 Analysing against compliance frameworks...')
try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"Please analyse this security policy:\n\n{policy_text}"}
            ]
        )
        # --- Display initial compliance analysis ---
        print('\n📋 Compliance Analysis:')
        print(response.content[0].text)

except Exception as e:
            print(f'\n❌ Error during analysis: {e}')
            print('Please check your API key and try again.')

# --- Enable follow-up questions with conversation memory ---
            print('\nYou can now ask follow-up questions about the compliance gaps.')
            print('Type quit to exit')

comp_history = [
            {'role': 'user', 'content': f'Analyse this policy:\n\n{policy_text}'},
            {'role': 'assistant', 'content': response.content[0].text}
        ]

# --- Follow-up question loop ---
while True:
    question = input('\nYour question: ')
    if question.lower() == 'quit':
        print('Goodbye!')
        break
    comp_history.append({'role': 'user', 'content': question})
    try:
        follow_up = client.messages.create(
            model='claude-opus-4-6',
            max_tokens=1024,
            system=system_prompt,
            messages=comp_history
        )
        answer = follow_up.content[0].text
        print('\nClaude:', answer)
        comp_history.append({'role': 'assistant', 'content': answer})

    except Exception as e:
        print(f'\n❌ Error: {e}')
        print('Something went wrong. Please try again.')