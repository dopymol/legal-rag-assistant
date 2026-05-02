from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain
from transformers import pipeline
from langchain.prompts import PromptTemplate

# Load embedding model
def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore

# Load local LLM
from functools import lru_cache

@lru_cache(maxsize=1)
def load_llm():
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",   # faster model
        max_length=512
    )
    return HuggingFacePipeline(pipeline=pipe)

# QA function
def get_answer(vectorstore, query):
    docs = vectorstore.similarity_search(query, k=5)

    llm = load_llm()
    prompt_template = """
    You are a legal assistant.

    Use the provided contract context to answer the question clearly.

    Instructions:
    - Explain in simple language
    - If clause exists, explain it clearly
    - Do NOT return clause numbers only
    - Do NOT guess
    - If not found, say "Not found in document"

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    chain = load_qa_chain(llm, chain_type="stuff", prompt=PROMPT)

    response = chain.run(input_documents=docs, question=query)
    return response, docs