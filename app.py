import streamlit as st
import os
from anthropic import Anthropic
from dotenv import load_dotenv

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

def get_api_key():
    # Try .env first (local), then Streamlit secrets (cloud)
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    if hasattr(st, 'secrets') and "ANTHROPIC_API_KEY" in st.secrets:
        return st.secrets["ANTHROPIC_API_KEY"]
    return None
def ask_claude(question, document_text, industry):
    client = Anthropic(api_key=get_api_key())
    system_prompt = INDUSTRY_PROMPTS[industry]
    context = document_text[:3000]

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"""Use the following document to answer the question accurately.

Document:
{context}

Question: {question}

Answer based only on the document. If the answer is not in the document, say so clearly."""
        }]
    )
    return response.content[0].text

# --- Main app ---
st.title("AI Document Intelligence Hub")
st.write("Upload a document, select your industry, and ask questions!!")

st.sidebar.title("Settings")
industry = st.sidebar.selectbox(
    "Select Industry Mode",
    list(INDUSTRY_PROMPTS.keys())
)
st.sidebar.write(f"Active mode: {industry}")

uploaded_file = st.file_uploader(
    "Upload your document (PDF or TXT)",
    type=["txt", "pdf"]
)

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(uploaded_file)
            document_text = ""
            for page in reader.pages:
                document_text += page.extract_text()
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            document_text = ""
    else:
        document_text = uploaded_file.read().decode("utf-8")

    if document_text:
        st.success(f"Document ready: {uploaded_file.name} ({len(document_text)} characters)")
        question = st.text_input("Ask a question about your document:")

        if question:
            with st.spinner("Finding answer..."):
                try:
                    answer = ask_claude(question, document_text, industry)
                    st.write("### Answer")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error: {e}")