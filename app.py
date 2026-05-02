import streamlit as st
from utils import extract_text_from_pdf, chunk_text, detect_risks
from rag_pipeline import create_vector_store, get_answer

# -------- Page Config --------
st.set_page_config(page_title="Legal AI Assistant", layout="wide")

# -------- Styling --------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f5f7fb;
}

/* Main container */
.block-container {
    padding-top: 1.5rem;
    max-width: 1100px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 10px 16px;
    border: none;
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Inputs */
input {
    border-radius: 8px !important;
}
/* Remove white box around buttons */
div.stButton {
    background: transparent !important;
    padding: 0px !important;
    border: none !important;
}

/* Fix expander box */
details {
    background: white;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)

# -------- Sidebar --------
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("Upload a contract and start analysis.")

uploaded_file = st.sidebar.file_uploader("📄 Upload Contract (PDF)", type="pdf")

# -------- Header --------
st.title("⚖️ AI Legal Contract Analyzer")

st.markdown(
    "<p style='color:#6b7280; font-size:16px;'>"
    "Analyze legal contracts, detect risks, and get clear AI-powered insights."
    "</p>",
    unsafe_allow_html=True
)

# -------- About Section --------

st.subheader("📘 About This Application")

st.write("""
This AI-powered Legal Contract Analyzer helps users understand complex legal documents quickly and efficiently using Retrieval-Augmented Generation (RAG).

It allows you to upload contracts, detect potential risks, and ask questions in natural language to get simplified legal insights.
""")

# -------- Buttons --------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Upload Guide"):
        st.info("Upload PDF contracts such as agreements, NDAs, or legal documents.")

with col2:
    if st.button("⚠️ Risk Detection"):
        st.info("The system detects clauses like penalties, liabilities, and termination conditions.")

with col3:
    if st.button("❓ How It Works"):
        st.info("The AI reads your document, retrieves relevant sections, and answers your questions.")

st.markdown('</div>', unsafe_allow_html=True)

# -------- Session State --------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "text" not in st.session_state:
    st.session_state.text = ""

# -------- File Processing --------
if uploaded_file:
    with st.spinner("📥 Reading document..."):
        text = extract_text_from_pdf(uploaded_file)
        st.session_state.text = text

        chunks = chunk_text(text)
        st.session_state.vectorstore = create_vector_store(chunks)

    st.success("✅ Document processed successfully!")

# -------- Show Preview + Risks --------
if st.session_state.text:

    risks = detect_risks(st.session_state.text)

    col1, col2 = st.columns(2)

    # -------- Document Preview --------
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📄 Document Preview")
        st.text_area("", st.session_state.text[:1500], height=300)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- Risk Detection --------
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⚠️ Risk Detection")

        if risks:
            for risk in risks:
                st.markdown(f"- ⚠️ **{risk}**")
        else:
            st.success("No major risks detected")

        st.markdown('</div>', unsafe_allow_html=True)

# -------- Q&A Section --------
st.markdown("---")
st.subheader("💬 Ask Questions")

query = st.text_input("Type your question about the contract:")

if st.button("🔍 Analyze"):
    if not st.session_state.vectorstore:
        st.error("Please upload a document first.")
    elif not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("🤖 Analyzing..."):
            answer, docs = get_answer(st.session_state.vectorstore, query)

        # -------- Answer Card --------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📌 Answer")
        st.write(answer)
        st.markdown('</div>', unsafe_allow_html=True)

        # -------- Sources --------
        with st.expander("📚 View Source Clauses"):
            for doc in docs:
                st.write(doc.page_content)
                st.markdown("---")