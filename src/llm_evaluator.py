from typing import List

from src.ingest_resume import extract_text_from_pdf
from src.chunk_resume import chunk_text
from src.match_resume_to_jd import load_job_description, build_vectorstore



def evaluate_resume_locally(
    jd_text: str,
    resume_chunks: List[str],
    similarity_scores: List[float]
) -> str:
    """
    Local deterministic resume evaluator (LLM fallback).
    Produces structured evaluation using semantic similarity scores.
    """

    avg_score = sum(similarity_scores) / len(similarity_scores)

    # Normalize similarity score to 0–100
    match_score = min(int(avg_score * 100), 100)

    strengths = []
    gaps = []

    jd_lower = jd_text.lower()
    resume_text = " ".join(resume_chunks).lower()

    # Simple skill inference
    key_skills = [
        "python", "machine learning", "data science", "sql",
        "api", "nlp", "deep learning", "cloud", "docker"
    ]

    for skill in key_skills:
        if skill in jd_lower and skill in resume_text:
            strengths.append(skill)
        elif skill in jd_lower and skill not in resume_text:
            gaps.append(skill)

    recommendation = (
        "Hire" if match_score >= 80 else
        "Consider" if match_score >= 60 else
        "Reject"
    )

    return f"""
Match Score: {match_score}/100

Key Strengths:
- {', '.join(strengths) if strengths else 'Relevant experience aligned with job requirements'}

Skill Gaps:
- {', '.join(gaps) if gaps else 'No major gaps identified'}

Final Recommendation:
{recommendation}
""".strip()


if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"
    jd_path = "data/job_descriptions/sample_jd.txt"

    # Load resume and job description
    resume_text = extract_text_from_pdf(resume_path)
    resume_chunks = chunk_text(resume_text)

    vectorstore = build_vectorstore(resume_chunks)
    jd_text = load_job_description(jd_path)

    # Retrieve relevant chunks + similarity scores
    results = vectorstore.similarity_search_with_score(jd_text, k=4)

    top_chunks = [doc.page_content for doc, _ in results]
    similarity_scores = [score for _, score in results]

    evaluation = evaluate_resume_locally(
        jd_text,
        top_chunks,
        similarity_scores
    )

    print("\n🧠 Resume Evaluation Result (Local Fallback):\n")
    print(evaluation)
