import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.ingest_resume import extract_text_from_pdf
from src.chunk_resume import chunk_text
from src.match_resume_to_jd import load_job_description, build_vectorstore
from src.llm_evaluator import evaluate_resume_locally


# ✅ 1. CREATE THE APP FIRST
app = FastAPI(title="AI Resume Screener", version="1.0")


# ✅ 2. THEN ADD MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/upload")
def upload_files(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...)
):
    resume_path = os.path.join(UPLOAD_DIR, "resume.pdf")
    jd_path = os.path.join(UPLOAD_DIR, "job_description.txt")

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(job_description.file, buffer)

    return {"message": "Files uploaded successfully"}


@app.get("/score")
def score_candidate():
    resume_text = extract_text_from_pdf("data/uploads/resume.pdf")
    resume_chunks = chunk_text(resume_text)

    vectorstore = build_vectorstore(resume_chunks)
    jd_text = load_job_description("data/uploads/job_description.txt")

    results = vectorstore.similarity_search_with_score(jd_text, k=4)
    top_chunks = [doc.page_content for doc, _ in results]
    scores = [score for _, score in results]

    evaluation = evaluate_resume_locally(jd_text, top_chunks, scores)

    return {"evaluation": evaluation}
