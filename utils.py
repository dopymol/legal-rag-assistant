import pdfplumber
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # -------- CLEAN TEXT --------

    # Remove unnecessary line breaks
    text = re.sub(r'\n+', '\n', text)

    # Join broken sentences
    text = re.sub(r'(?<!\.)\n(?!\n)', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_text(text)

def detect_risks(text):
    risks = []

    keywords = {
        "Penalty Clause": ["penalty", "fine", "charge"],
        "Auto Renewal": ["auto-renew", "automatic renewal"],
        "Liability": ["liable", "liability", "damages"],
        "Termination Conditions": ["terminate", "termination"]
    }

    for risk_type, words in keywords.items():
        for word in words:
            if word.lower() in text.lower():
                risks.append(risk_type)
                break

    return list(set(risks))