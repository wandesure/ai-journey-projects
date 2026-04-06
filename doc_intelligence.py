import anthropic
import os
from dotenv import load_dotenv 
load_dotenv()
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# --- Industry system prompts ---
INDUSTRY_PROMPTS = {
    "telecom": """You are an expert telecom compliance analyst with deep knowledge of:
- CRTC regulations and Canadian telecom law
- Network security and data governance
- Privacy regulations (PIPEDA)
- Telecom infrastructure security
Answer questions accurately from the provided documents using telecom industry terminology.""",

    "legal": """You are an expert legal analyst with deep knowledge of:
- Contract law and analysis
- Regulatory compliance
- Risk and liability assessment
- Legal document review
Answer questions accurately from the provided documents using precise legal terminology.""",

    "healthcare": """You are an expert healthcare compliance analyst with deep knowledge of:
- HIPAA and patient privacy regulations
- Medical data security
- Healthcare facility compliance
- Clinical documentation standards
Answer questions accurately from the provided documents using healthcare terminology.""",

    "hr": """You are an expert HR analyst with deep knowledge of:
- Employment law and regulations
- HR policies and procedures
- Workplace compliance
- People management best practices
Answer questions accurately from the provided documents using HR terminology.""",

    "finance": """You are an expert financial compliance analyst with deep knowledge of:
- Financial regulations and reporting
- Risk management frameworks
- Audit and compliance requirements
- Banking and investment regulations
Answer questions accurately from the provided documents using financial terminology."""
}

# --- Industry selection ---
def select_industry():
    print("\nSelect your industry mode:")
    print("1. Telecom")
    print("2. Legal")
    print("3. Healthcare")
    print("4. HR")
    print("5. Finance")
    
    choice = input("\nEnter number (1-5): ")
    
    industries = {
        "1": "telecom",
        "2": "legal",
        "3": "healthcare",
        "4": "hr",
        "5": "finance"
    }
    
    selected = industries.get(choice, "telecom")
    print(f"\nActivating {selected.upper()} mode!!")
    return selected

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
def ask_claude(question, context_chunks, industry="telecom"):
    context = "\n\n".join(context_chunks)
    system_prompt = INDUSTRY_PROMPTS[industry]
    
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"""Use the following document excerpts to answer the question accurately.

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

# Load and index documents
add_document("sample_policy.txt", "security_policy")
add_document("hr_policy.txt", "hr_policy")

# Select industry mode
industry = select_industry()

print("\nDocuments indexed and ready!!")
print("Ask questions about the documents or type 'quit' to exit\n")

# Conversation loop
while True:
    question = input("Your question: ")
    if question.lower() == "quit":
        print("Goodbye!!")
        break
    
    relevant_chunks = search_relevant_chunks(question)
    answer = ask_claude(question, relevant_chunks, industry)
    
    print(f"\nClaude: {answer}\n")