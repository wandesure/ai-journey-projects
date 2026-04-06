#import anthropic
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings


#client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# --- Initialise LangChain components ---
llm = ChatAnthropic(
    model="claude-opus-4-6",
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

embeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


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
# --- Load and index documents using LangChain ---
def load_documents(file_paths):
    all_docs = []
    for file_path in file_paths:
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        docs = loader.load()
        all_docs.extend(docs)
    
    # Split into chunks
    chunks = text_splitter.split_documents(all_docs)
    
    # Create vector store
    vectorstore = Chroma.from_documents(chunks, embeddings)
    print(f"Loaded {len(chunks)} chunks into ChromaDB!!")
    return vectorstore
    return selected

# --- Ask question using LangChain ---
def ask_question(question, vectorstore, industry="telecom"):
    system_prompt = INDUSTRY_PROMPTS[industry]
    
    # Retrieve relevant chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    relevant_docs = retriever.invoke(question)
    
    # Build context from retrieved docs
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Ask Claude with context and industry prompt
    full_prompt = f"""{system_prompt}

Use the following document excerpts to answer the question accurately.

Document excerpts:
{context}

Question: {question}

Answer based only on the document excerpts provided.
If the answer is not in the excerpts say so clearly."""

    response = llm.invoke(full_prompt)
    return response.content

# --- Main program ---
print("🤖 AI Document Intelligence Assistant (LangChain Edition)")
print("==========================================================")

# Load documents
file_paths = ["sample_policy.txt", "hr_policy.txt"]
vectorstore = load_documents(file_paths)

# Select industry
industry = select_industry()

print("\nReady to answer questions!!")
print("Type 'quit' to exit\n")

# Conversation loop
while True:
    question = input("Your question: ")
    if question.lower() == "quit":
        print("Goodbye!!")
        break
    
    answer = ask_question(question, vectorstore, industry)
    print(f"\nClaude: {answer}\n")


