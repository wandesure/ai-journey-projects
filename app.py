import streamlit as st
import streamlit_authenticator as stauth
import os
from anthropic import Anthropic
from dotenv import load_dotenv
import db_auth

load_dotenv()

# --- Authentication Configuration ---
def get_credentials():
    """
    Get credentials from SQLite database.
    On first run, seeds from Streamlit secrets if database is empty.
    """
    # Seed database from secrets on first run
    if not db_auth.db_exists():
        if hasattr(st, 'secrets') and "credentials" in st.secrets:
            secrets_creds = {
                "usernames": {
                    username: dict(data)
                    for username, data in st.secrets["credentials"]["usernames"].items()
                }
            }
            db_auth.seed_from_secrets(secrets_creds)
        else:
            return None

    # Load credentials from SQLite
    credentials = db_auth.get_all_users()
    if not credentials["usernames"]:
        return None
    return credentials

def show_missing_secrets_error():
    """Display error when secrets are not configured."""
    st.title("AI Document Intelligence Hub")
    st.markdown("---")
    st.error("Authentication not configured")
    st.markdown("""
    ### Setup Required

    Credentials must be configured in Streamlit secrets before the app can run.

    **For local development:**
    1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
    2. Update the passwords with bcrypt hashes (run `python generate_password_hash.py`)
    3. Add your `ANTHROPIC_API_KEY`

    **For Streamlit Cloud:**
    1. Go to your app settings → Secrets
    2. Add the credentials configuration from `secrets.toml.example`
    """)
    st.stop()

# --- Custom CSS Styling ---
st.markdown("""
<style>
    /* Main title styling */
    h1 {
        color: #2E75B6 !important;
        border-bottom: 3px solid #2E75B6;
        padding-bottom: 10px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F0F4F8;
        padding: 10px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2E75B6 !important;
        color: white !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F0F4F8;
        border-right: 2px solid #2E75B6;
    }

    [data-testid="stSidebar"] h1 {
        color: #2E75B6 !important;
        border-bottom: none;
    }

    /* Button styling */
    .stButton > button {
        background-color: #2E75B6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #1E5A8A;
        box-shadow: 0 4px 12px rgba(46, 117, 182, 0.4);
    }

    /* File uploader styling */
    [data-testid="stFileUploader"] {
        border: 2px dashed #2E75B6;
        border-radius: 10px;
        padding: 20px;
        background-color: #F0F4F8;
    }

    /* Success/Info boxes */
    .stSuccess, .stInfo {
        border-left: 4px solid #2E75B6;
    }

    /* Text input styling */
    .stTextInput > div > div > input {
        border: 2px solid #F0F4F8;
        border-radius: 8px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #2E75B6;
        box-shadow: 0 0 0 2px rgba(46, 117, 182, 0.2);
    }

    /* Text area styling */
    .stTextArea > div > div > textarea {
        border: 2px solid #F0F4F8;
        border-radius: 8px;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #2E75B6;
    }

    /* Footer styling */
    footer {
        visibility: hidden;
    }

    /* Custom footer */
    .custom-footer {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #2E75B6, #1E5A8A);
        color: white;
        border-radius: 10px;
        margin-top: 30px;
    }

    /* Section headers */
    h3 {
        color: #2E75B6 !important;
        border-left: 4px solid #2E75B6;
        padding-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Authentication ---
credentials = get_credentials()
if credentials is None:
    show_missing_secrets_error()

authenticator = stauth.Authenticate(
    credentials,
    "ai_doc_hub_cookie",
    "ai_doc_hub_key",
    cookie_expiry_days=30
)

# Show login form
try:
    authenticator.login()
except Exception as e:
    st.error(f"Authentication error: {e}")

# Check authentication status
if st.session_state.get("authentication_status") is None:
    st.title("AI Document Intelligence Hub")
    st.markdown("---")
    st.info("Please enter your username and password to continue.")

    # Forgot password widget
    st.markdown("---")
    with st.expander("Forgot Password?"):
        try:
            username_forgot, email_forgot, new_password = authenticator.forgot_password()
            if username_forgot:
                # Persist the new password hash to SQLite
                new_hash = credentials["usernames"][username_forgot]["password"]
                db_auth.update_password(username_forgot, new_hash)
                st.success(f"New password generated for **{username_forgot}**")
                st.info(f"Your new temporary password is: `{new_password}`")
                st.warning("**Important:** Please change this password after logging in.")
            elif username_forgot is False:
                st.error("Username not found.")
        except Exception as e:
            st.error(f"Error: {e}")
    st.stop()
elif st.session_state.get("authentication_status") is False:
    st.title("AI Document Intelligence Hub")
    st.markdown("---")
    st.error("Username or password is incorrect.")

    # Forgot password widget
    st.markdown("---")
    with st.expander("Forgot Password?"):
        try:
            username_forgot, email_forgot, new_password = authenticator.forgot_password()
            if username_forgot:
                # Persist the new password hash to SQLite
                new_hash = credentials["usernames"][username_forgot]["password"]
                db_auth.update_password(username_forgot, new_hash)
                st.success(f"New password generated for **{username_forgot}**")
                st.info(f"Your new temporary password is: `{new_password}`")
                st.warning("**Important:** Please change this password after logging in.")
            elif username_forgot is False:
                st.error("Username not found.")
        except Exception as e:
            st.error(f"Error: {e}")
    st.stop()

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

# Welcome message and logout
st.sidebar.markdown(f"**Welcome, {st.session_state.get('name', 'User')}!**")
authenticator.logout("Logout", "sidebar")
st.sidebar.markdown("---")

# Password change section
with st.sidebar.expander("Change Password"):
    try:
        if authenticator.reset_password(st.session_state["username"]):
            # Persist the new password hash to SQLite
            username = st.session_state["username"]
            new_hash = credentials["usernames"][username]["password"]
            db_auth.update_password(username, new_hash)
            st.success("Password changed and saved!")
    except Exception as e:
        st.error(f"Error: {e}")
st.sidebar.markdown("---")

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
st.markdown("""
<div class="custom-footer">
    <strong>AI Document Intelligence Hub</strong><br>
    Built by Wande Oluwatomi | Powered by Claude AI
</div>
""", unsafe_allow_html=True)