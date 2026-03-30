import anthropic
import os
import requests
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

tools =[
    {
        "name": "calculate",
         "description": "Performs mathematical calculations.Use this for any maths.",
         "input_schema":{
             "type":"object",
             "properties":{
                 "expression":{
                     "type":"string",
                     "description": "The mathematical expression to evaluate e.g 2+2"
                 }
             },
         "required":["expression"]    
             
         }
    },

    {
        "name": "get_word_count",
        "description": "Counts the number of words in a text",
        "input_schema":{
            "type": "object",
            "properties":{
                "text":{
                    "type": "string",
                    "description": "The text to count words in"
                }
            },
        "required":["text"]
        }
    },
    {
        "name": "search_web",
        "description": "Search the web for current information on any topic",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "compliance_check",
        "description": "Search the web for current information on any topic",
        "input_schema": {
            "type": "object",
            "properties": {
                "policy": {
                    "type": "string",
                    "description": "Checks a security policy for compliance gaps against common frameworks"
                }
            },
            "required": ["policy"]
        }
    }
    ]
def calculate(expression):
    return str(eval(expression))

def get_word_count(text):
    return str(len(text.split()))

def search_web(query):
    # Using DuckDuckGo instant answer API — completely free
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
    response = requests.get(url)
    data = response.json()
    result = data.get('AbstractText','')
    if not result:
        result = data.get('Answer', 'No results found')
    return result if result else 'No direct answer found — try a more specific query'

def compliance_check(policy):
    gaps = []
    keywords = ["password", "encryption", "access control", 
                "mfa", "backup", "incident response", "monitoring"]
    policy_lower = policy.lower()
    for keyword in keywords:
        if keyword not in policy_lower:
            gaps.append(keyword)
    if gaps:
        return f"Missing topics: {', '.join(gaps)}"
    else:
        return "Policy covers all basic topics!!"

def run_tool(tool_name, tool_input):
    if tool_name == "calculate":
        return calculate(tool_input["expression"])
    elif tool_name == "get_word_count":
        return get_word_count(tool_input["text"])
    elif tool_name == "search_web":
        return search_web(tool_input["query"])
    elif tool_name == "compliance_check":
        return compliance_check(tool_input["policy"])
    else:
        return "Tool not found"
    

    

user_message = input("Ask Claude anything: ")

response = client.messages.create(
    model = "claude-opus-4-6",
    max_tokens = 1024,
    tools = tools,
    messages = [{"role": "user", "content": user_message}]

)

if response.stop_reason == "tool_use":
    tool_block = next(b for b in response.content if b.type == "tool_use")
    tool_result = run_tool(tool_block.name, tool_block.input)
    print(f"Result: {tool_result}")

else:
    print(response.content[0].text)
