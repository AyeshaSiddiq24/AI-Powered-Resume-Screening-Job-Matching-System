import pdfplumber
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a resume PDF and return cleaned text.
    """
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

    full_text = "\n".join(pages)

    # basic cleaning
    full_text = full_text.replace("\t", " ")
    full_text = " ".join(full_text.split())

    return full_text


if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"

    if not Path(resume_path).exists():
        raise FileNotFoundError("❌ Resume PDF not found")

    resume_text = extract_text_from_pdf(resume_path)

    print("✅ Resume text extracted successfully\n")
    print(resume_text[:1500])  # preview
