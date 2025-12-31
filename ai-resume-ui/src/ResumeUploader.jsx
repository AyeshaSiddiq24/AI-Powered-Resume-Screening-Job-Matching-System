import React, { useState } from "react";
import axios from "axios";

function ResumeUploader() {
  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!resume || !jd) {
      alert("Please select both resume and job description");
      return;
    }

    setLoading(true);
    setResult("");

    try {
      const formData = new FormData();
      formData.append("resume", resume);
      formData.append("job_description", jd);

      // STEP 1: Upload files
      const uploadRes = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      console.log("UPLOAD OK:", uploadRes.data);

      // STEP 2: Score candidate
      const scoreRes = await axios.get(
        "http://127.0.0.1:8000/score"
      );

      console.log("SCORE OK:", scoreRes.data);

      setResult(scoreRes.data.evaluation);

    } catch (err) {
      console.error("FULL ERROR:", err);

      if (err.response) {
        alert(`Backend error: ${err.response.data.detail || "Unknown error"}`);
      } else {
        alert("Cannot reach backend. Is FastAPI running?");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setResume(e.target.files[0])}
      />
      <br /><br />

      <input
        type="file"
        accept=".txt"
        onChange={(e) => setJd(e.target.files[0])}
      />
      <br /><br />

        <button className="primary-btn" onClick={handleSubmit}>
    Evaluate Resume
  </button>


      <pre style={{ whiteSpace: "pre-wrap", marginTop: "20px" }}>
        {result && <div className="result">{result}</div>}

      </pre>
    </div>
  );
}

export default ResumeUploader;
