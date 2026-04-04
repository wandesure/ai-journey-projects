
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# --- Load the document ---
with open("sample_policy.txt", "r") as f:
    document = f.read()
print(f"Document loaded!! {len(document)} characters read.")

# --- Split document into chunks ---
def split_into_chunks(text, chunk_size=200, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

chunks = split_into_chunks(document)
print(f"Document split into {len(chunks)} chunks!!")

# --- Find most relevant chunk ---
def find_relevant_chunk(question, chunks):
    question_words = question.lower().split()
    best_chunk = ""
    best_score = 0
    
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = 0
        for word in question_words:
            if word in chunk_lower:
                score += 1
        if score > best_score:
            best_score = score
            best_chunk = chunk
    
    return best_chunk

# --- Ask Claude using the relevant chunk as context ---
def ask_claude(question, context):
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Use the following document excerpt to answer the question.
                
Document excerpt:
{context}

Question: {question}

Answer based only on the document excerpt provided. If the answer is not in the excerpt say so."""
            }
        ]
    )
    return response.content[0].text

# --- Main conversation loop ---
print("🔍 Simple RAG System")
print("====================")
print(f"Document loaded and split into {len(chunks)} chunks")
print("Ask questions about the document or type 'quit' to exit\n")

while True:
    question = input("Your question: ")
    if question.lower() == "quit":
        print("Goodbye!")
        break
    
    # Find relevant chunk
    relevant_chunk = find_relevant_chunk(question, chunks)
    
    # Ask Claude with context
    answer = ask_claude(question, relevant_chunk)
    
    print(f"\nClaude: {answer}\n")