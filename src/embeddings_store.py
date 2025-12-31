from typing import List
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

from chunk_resume import chunk_text
from ingest_resume import extract_text_from_pdf


def build_faiss_index(chunks: List[str]) -> FAISS:
    """
    Build a FAISS vector store from resume text chunks.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return vectorstore


if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"

    text = extract_text_from_pdf(resume_path)
    chunks = chunk_text(text)

    vectorstore = build_faiss_index(chunks)

    print("✅ FAISS vector store created successfully")

    # Test semantic search
    query = "machine learning and data science experience"
    results = vectorstore.similarity_search(query, k=3)

    print("\n🔍 Top semantic matches:\n")
    for i, doc in enumerate(results):
        print(f"--- Match {i+1} ---")
        print(doc.page_content[:300])
        print()