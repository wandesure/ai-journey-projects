import anthropic
import os
from dotenv import load_dotenv 
load_dotenv()
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# --- Initialise embedding model and vector database ---
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("documents")

# --- Split document into chunks ---
def split_into_chunks(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

# --- Read PDF document ---
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# --- Add document to ChromaDB ---
def add_document(file_path, doc_name):
    if file_path.endswith(".pdf"):
        text = read_pdf(file_path)
    else:
        with open(file_path, "r") as f:
            text = f.read()
    
    chunks = split_into_chunks(text)
    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{doc_name}_chunk_{i}"]
        )
    print(f"Added {len(chunks)} chunks from {doc_name} to ChromaDB!!")
# --- Search ChromaDB for relevant chunks ---
def search_relevant_chunks(question, n_results=3):
    question_embedding = embedding_model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )
    return results['documents'][0]

# --- Ask Claude with retrieved context ---
def ask_claude(question, context_chunks):
    context = "\n\n".join(context_chunks)
    
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a helpful document assistant. 
Use the following document excerpts to answer the question accurately.

Document excerpts:
{context}

Question: {question}

Answer based only on the document excerpts provided. 
If the answer is not in the excerpts say so clearly."""
            }
        ]
    )
    return response.content[0].text

# --- Load document and start conversation ---
print("🤖 AI Document Intelligence Assistant")
print("======================================")

# Load and index the document


add_document("sample_policy.txt", "security_policy")
add_document("hr_policy.txt", "hr_policy")

print("\nDocument indexed and ready!!")
print("Ask questions about the document or type 'quit' to exit\n")

# Conversation loop
while True:
    question = input("Your question: ")
    if question.lower() == "quit":
        print("Goodbye!!")
        break
    
    # Search for relevant chunks
    relevant_chunks = search_relevant_chunks(question)
    
    # Get Claude's answer
    answer = ask_claude(question, relevant_chunks)
    
    print(f"\nClaude: {answer}\n")