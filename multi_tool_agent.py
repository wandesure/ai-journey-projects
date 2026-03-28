import anthropic
import os 
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
        "name": "reverse_text",
        "description":"Reverse any string of text",
        "input_schema":{
            "type":"object",
            "properties":{
                "text":{
                    "type":"string",
                    "description":"The text to reverse"
                }
            },
            "required":["text"]

        }
    }
    
    
]

def calculate(expression):
    return str(eval(expression))

def get_word_count(text):
    return str(len(text.split()))

def reverse_text(text):
    return text[::-1]

def run_tool(tool_name, tool_input):
    if tool_name == "calculate":
        return calculate(tool_input["expression"])
    elif tool_name == "get_word_count":
        return get_word_count(tool_input["text"])
    elif tool_name == "reverse_text":
        return reverse_text(tool_input["text"])
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
