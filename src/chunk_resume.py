from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.ingest_resume import extract_text_from_pdf



def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[str]:
    """
    Split resume text into overlapping chunks for embeddings.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)


if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"
    text = extract_text_from_pdf(resume_path)

    chunks = chunk_text(text)

    print(f"✅ Total chunks created: {len(chunks)}\n")

    for i, chunk in enumerate(chunks[:3]):
        print(f"--- Chunk {i+1} ---")
        print(chunk[:500])
        print()
