import os
from pathlib import Path

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# Step 1: Setup Groq LLM
# -----------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL_NAME = "llama-3.1-8b-instant"

llm = ChatGroq(
    model=GROQ_MODEL_NAME,
    temperature=0.5,
    max_tokens=512,
    api_key=GROQ_API_KEY,
)

# -----------------------------
# Step 2: FAISS (AUTO LOAD / CREATE)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DB_FAISS_PATH = BASE_DIR / "vectorstore" / "db_faiss"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def load_or_create_faiss():
    """
    Loads FAISS if exists.
    Creates FAISS automatically if missing (Streamlit-safe).
    """
    if DB_FAISS_PATH.exists():
        print("✅ Loading existing FAISS index...")
        return FAISS.load_local(
            str(DB_FAISS_PATH),
            embedding_model,
            allow_dangerous_deserialization=True
        )
    else:
        print("⚠️ FAISS not found. Creating new index...")

        # Import here to avoid circular import
        from create_memory_for_llm import create_vectorstore

        db = create_vectorstore()
        return db

db = load_or_create_faiss()

# -----------------------------
# Step 3: Build RAG Chain
# -----------------------------
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

combine_docs_chain = create_stuff_documents_chain(
    llm,
    retrieval_qa_chat_prompt
)

rag_chain = create_retrieval_chain(
    db.as_retriever(search_kwargs={"k": 3}),
    combine_docs_chain
)

# -----------------------------
# Step 4: Run Query
# -----------------------------
user_query = input("Write Query Here: ")
response = rag_chain.invoke({"input": user_query})

print("\nRESULT:", response["answer"])
print("\nSOURCE DOCUMENTS:")
for doc in response["context"]:
    print(f"- {doc.metadata} -> {doc.page_content[:200]}...")
