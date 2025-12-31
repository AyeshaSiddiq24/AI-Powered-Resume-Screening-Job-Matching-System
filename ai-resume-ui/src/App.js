import React from "react";
import ResumeUploader from "./ResumeUploader";
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <div className="card">
        <h1 className="title">AI Resume Screener</h1>
        <p className="subtitle">
          Upload a resume and job description to get an AI-driven evaluation
        </p>
        <ResumeUploader />
      </div>
    </div>
  );
}

export default App;
