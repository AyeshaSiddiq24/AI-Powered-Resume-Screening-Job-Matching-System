from pathlib import Path
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

from src.ingest_resume import extract_text_from_pdf
from src.chunk_resume import chunk_text



def load_job_description(jd_path: str) -> str:
    if not Path(jd_path).exists():
        raise FileNotFoundError("❌ Job description not found")
    return Path(jd_path).read_text()


def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_texts(chunks, embedding=embeddings)


if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"
    jd_path = "data/job_descriptions/sample_jd.txt"

    resume_text = extract_text_from_pdf(resume_path)
    resume_chunks = chunk_text(resume_text)

    vectorstore = build_vectorstore(resume_chunks)

    job_description = load_job_description(jd_path)

    results = vectorstore.similarity_search(job_description, k=5)

    print("🔍 Top resume sections matching the Job Description:\n")

    for i, doc in enumerate(results):
        print(f"--- Match {i+1} ---")
        print(doc.page_content[:400])
        print()
