import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

#Define the tool
tools = [
    {"name":"calculate",
     "description": "Performs mathematical calculations.Use this for any maths.",
     "input_schema":{
         "type": "object",
         "properties":{
             "expression":{
                 "type": "string",
                 "description": "The mathematical expression to evaluate e.g 2+2"
             }
         },
         "required":["expression"]
     }

    }
]

def run_calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error:{e}"
    
user_message = input("Ask Claude a math questin:")

response = client.messages.create(
    model = "claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    messages= [{"role": "user", "content": user_message}]
)

# Check if Claude wants to use a tool
if response.stop_reason == "tool_use":
    tool_block = next(b for b in response.content if b.type == "tool_use")
    tool_result = run_calculator(tool_block.input["expression"])
    print(f"Claude calculated:{tool_result}")
else:
    print(response.content[0].text)