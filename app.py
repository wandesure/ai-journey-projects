import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
load_dotenv()

# --- Industry prompts ---
INDUSTRY_PROMPTS = {
    "General": "You are a helpful document assistant. Answer questions accurately from the provided documents.",
    "Telecom": "You are a telecom compliance analyst with knowledge of CRTC regulations and PIPEDA.",
    "Legal": "You are a legal analyst specialising in contract analysis and regulatory compliance.",
    "Healthcare": "You are a healthcare compliance analyst with knowledge of HIPAA and patient privacy.",
    "HR": "You are an HR analyst specialising in employment law and workplace compliance.",
    "Finance": "You are a financial compliance analyst with knowledge of financial regulations.",
}

# --- Initialise models ---
@st.cache_resource
def load_models():
    llm = ChatAnthropic(
        model="claude-opus-4-6",
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return llm, embeddings

# --- Process uploaded file ---
def process_file(uploaded_file, embeddings):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    if uploaded_file.type == "application/pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        os.unlink(tmp_path)
    else:
        content = uploaded_file.read().decode("utf-8")
        docs = [Document(page_content=content)]

    chunks = text_splitter.split_documents(docs)
    #vectorstore = FAISS.from_documents(chunks, embeddings)
    #return vectorstore
    vectorstore = Chroma.from_documents(chunks, embeddings)
    return vectorstore

# --- Main app ---
st.title("AI Document Intelligence Hub")
st.write("Upload a document, select your industry, and ask questions!!")

# Load models
llm, embeddings = load_models()

# Sidebar - industry selector
st.sidebar.title("Settings")
industry = st.sidebar.selectbox(
    "Select Industry Mode",
    list(INDUSTRY_PROMPTS.keys())
)
st.sidebar.write(f"Mode: {industry}")

# File upload
uploaded_file = st.file_uploader(
    "Upload your document (PDF or TXT)",
    type=["txt", "pdf"]
)

if uploaded_file:
    with st.spinner("Processing your document..."):
        vectorstore = process_file(uploaded_file, embeddings)
    st.success(f"Document ready: {uploaded_file.name}")

    # Question input
    question = st.text_input("Ask a question about your document:")

    if question:
        with st.spinner("Finding answer..."):
            system_prompt = INDUSTRY_PROMPTS[industry]
            retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
            relevant_docs = retriever.invoke(question)
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

            full_prompt = f"""{system_prompt}

Use these document excerpts to answer accurately:
{context}

Question: {question}

Answer based only on the document. If not found, say so."""

            response = llm.invoke(full_prompt)
            st.write("### Answer")
            st.write(response.content)