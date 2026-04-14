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
st.markdown("**Built by Wande Oluwatomi** | AI Developer | Security & Compliance Specialist")
st.markdown("---")
st.info("This tool helps you extract insights from documents and check compliance against major security frameworks including NIST SP 800-53, ISO 27001, CIS Controls v8 and SOC 2.")
st.markdown("---")
st.write("Upload a document, select your industry, and ask questions!!")

st.sidebar.title("Settings")
industry = st.sidebar.selectbox(
    "Select Industry Mode",
    list(INDUSTRY_PROMPTS.keys())
)
st.sidebar.write(f"Active mode: {industry}")



# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Document Q&A", "Compliance Checker", "Document Summariser"])

with tab1:
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
            st.success(f"Document ready: {uploaded_file.name}")
            question = st.text_input("Ask a question about your document:")

            if question:
                with st.spinner("Finding answer..."):
                    try:
                        answer = ask_claude(question, document_text, industry)
                        st.write("### Answer")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"Error: {e}")

with tab2:
    st.write("### AI Compliance Checker")
    st.write("Paste your security policy below and get a compliance analysis!!")
    
    policy_text = st.text_area(
        "Paste your security policy here:",
        height=200
    )
    
    if st.button("Analyse Policy"):
        if policy_text:
            with st.spinner("Analysing against compliance frameworks..."):
                try:
                    compliance_prompt = """You are an expert security and compliance analyst with deep knowledge of:
- NIST SP 800-53 controls
- ISO 27001 requirements  
- CIS Controls v8
- SOC 2 Type II criteria

When given a security policy:
1. Identify which compliance frameworks it relates to
2. List what requirements are MET
3. List what requirements are MISSING or GAP
4. Give a compliance score out of 10
5. Provide specific improvement recommendations"""

                    client = Anthropic(api_key=get_api_key())
                    response = client.messages.create(
                        model="claude-opus-4-6",
                        max_tokens=2048,
                        system=compliance_prompt,
                        messages=[{
                            "role": "user",
                            "content": f"Please analyse this security policy:\n\n{policy_text}"
                        }]
                    )
                    st.write("### Compliance Analysis")
                    st.write(response.content[0].text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please paste a policy to analyse!!")

with tab3:
    st.write("### Document Summariser")
    st.write("Upload a document to get a clean, structured summary with key points highlighted.")

    summary_file = st.file_uploader(
        "Upload your document (PDF or TXT)",
        type=["txt", "pdf"],
        key="summary_uploader"
    )

    if summary_file:
        # Extract text from uploaded file
        if summary_file.type == "application/pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(summary_file)
                summary_doc_text = ""
                for page in reader.pages:
                    summary_doc_text += page.extract_text()
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
                summary_doc_text = ""
        else:
            summary_doc_text = summary_file.read().decode("utf-8")

        if summary_doc_text:
            st.success(f"Document ready: {summary_file.name}")

            if st.button("Generate Summary"):
                with st.spinner("Generating structured summary..."):
                    try:
                        summariser_prompt = """You are an expert document analyst who creates clear, structured summaries.

When summarising a document:
1. Start with a brief executive summary (2-3 sentences)
2. List the KEY POINTS as bullet points (use **bold** for the most important terms)
3. Identify any ACTION ITEMS or recommendations if present
4. Note any important dates, figures, or deadlines
5. End with a one-line conclusion

Format your response clearly with headers and bullet points for easy reading."""

                        client = Anthropic(api_key=get_api_key())
                        response = client.messages.create(
                            model="claude-opus-4-6",
                            max_tokens=2048,
                            system=summariser_prompt,
                            messages=[{
                                "role": "user",
                                "content": f"Please provide a structured summary of this document:\n\n{summary_doc_text[:5000]}"
                            }]
                        )
                        st.write("### Summary")
                        st.markdown(response.content[0].text)
                    except Exception as e:
                        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("**AI Document Intelligence Hub** | Built by Wande Oluwatomi | Powered by Claude AI")