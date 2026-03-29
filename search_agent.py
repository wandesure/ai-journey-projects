import anthropic
import os
import requests
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def search_web(query):
    # Using DuckDuckGo instant answer API — completely free
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
    response = requests.get(url)
    data = response.json()
    result = data.get('AbstractText','')
    if not result:
        result=data.get('Answer', 'Noresults found')
    return result if result else 'No direct answer found — try a more specific query'

# print(search_web('What is NIST SP 800-53'))

tools = [
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
    }
]

question = input("Ask Claude anything (it can search the web): ")

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": question}]
)

if response.stop_reason == "tool_use":
    tool_block = next(b for b in response.content if b.type == 'tool_use' )
    search_result = search_web(tool_block.input['query'])
    print(f'Search result:{search_result}')

else:
    print(response.content[0].text)