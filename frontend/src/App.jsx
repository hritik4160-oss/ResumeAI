import { useState } from "react";
import "./App.css";

function App() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeResume = async () => {
    if (!resume) {
      setError("Please upload your PDF resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch(
        "http://https://resumeai-u85q.onrender.com/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || "Analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Could not connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>ResumeAI</h1>
        <p>Smart Resume Analyzer</p>
      </header>

      <main className="main-content">
        <section className="upload-card">
          <h2>Analyze Your Resume</h2>

          <p className="subtitle">
            Upload your resume and compare it with a job description.
          </p>

          <label className="input-label">
            Upload Resume (PDF)
          </label>

          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={(event) => {
              setResume(event.target.files[0] || null);
              setError("");
            }}
          />

          {resume && (
            <p className="file-name">
              Selected: {resume.name}
            </p>
          )}

          <label className="input-label">
            Job Description
          </label>

          <textarea
            placeholder="Paste the job description here..."
            value={jobDescription}
            onChange={(event) =>
              setJobDescription(event.target.value)
            }
            rows="7"
          />

          <button onClick={analyzeResume} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>

          {error && (
            <p className="error-message">{error}</p>
          )}
        </section>

        {result && (
          <section className="results-section">
            <h2>Analysis Results</h2>

            <div className="score-card">
              <div
                className="score-circle"
                style={{ "--score": `${result.ats_score}%` }}
              >
                <div className="score-inner">
                  <strong>{result.ats_score}%</strong>
                  <span>Skill Match</span>
                </div>
              </div>

              <h3>Resume Skill Match</h3>

              <p>
                Matched {result.total_matched} out of{" "}
                {result.total_required} detected job skills.
              </p>
            </div>

            <div className="stats-grid">
              <div className="stat-card">
                <h3>{result.resume_skills.length}</h3>
                <p>Resume Skills</p>
              </div>

              <div className="result-card">
                <h3>Skill Match Overview</h3>

                <div className="progress-info">
                  <span>Overall Skill Match</span>
                  <strong>{result.ats_score}%</strong>
                </div>

                <div className="progress-track">
                  <div
                    className="progress-fill"
                    style={{ width: `${result.ats_score}%` }}
                  ></div>
                </div>

                <div className="progress-details">
                  <span>Matched: {result.total_matched}</span>
                  <span>
                    Missing: {result.missing_skills.length}
                  </span>
                </div>
              </div>

              <div className="stat-card">
                <h3>{result.matched_skills.length}</h3>
                <p>Matched Skills</p>
              </div>

              <div className="stat-card">
                <h3>{result.missing_skills.length}</h3>
                <p>Missing Skills</p>
              </div>
            </div>

            <div className="result-card">
              <h3>Skills Found in Your Resume</h3>

              <div className="keyword-list">
                {result.resume_skills.length > 0 ? (
                  result.resume_skills.map((skill) => (
                    <span className="keyword" key={skill}>
                      {skill}
                    </span>
                  ))
                ) : (
                  <p>No recognized skills found.</p>
                )}
              </div>
            </div>

            <div className="result-card">
              <h3>Matched Skills</h3>

              <div className="keyword-list">
                {result.matched_skills.length > 0 ? (
                  result.matched_skills.map((skill) => (
                    <span className="keyword matched" key={skill}>
                      {skill}
                    </span>
                  ))
                ) : (
                  <p>No matching skills found.</p>
                )}
              </div>
            </div>

            <div className="result-card">
              <h3>Missing Skills</h3>

              <div className="keyword-list">
                {result.missing_skills.length > 0 ? (
                  result.missing_skills.map((skill) => (
                    <span className="keyword missing" key={skill}>
                      {skill}
                    </span>
                  ))
                ) : (
                  <p>No missing detected skills.</p>
                )}
              </div>
            </div>

            <div className="result-card recommendation-card">
              <h3>🚀 Resume Improvement Recommendations</h3>

              {result.suggestions.map((suggestion, index) => (
                <div className="recommendation-item" key={index}>
                  <span className="recommendation-number">
                    {index + 1}
                  </span>

                  <p>{suggestion}</p>
                </div>
              ))}

              {result.missing_skills.length > 0 && (
                <div className="recommendation-item">
                  <span className="recommendation-number">!</span>

                  <p>
                    Review the missing skills:{" "}
                    {result.missing_skills.join(", ")}.
                    If you genuinely have these skills, consider adding
                    relevant examples to your resume.
                  </p>
                </div>
              )}
            </div>

            <div className="result-card recommendation-card">
              <h3>✨ Gemini AI Recommendations</h3>

              <p className="subtitle">
                Personalized resume improvement advice generated by Gemini.
              </p>

              {result.ai_recommendations &&
              result.ai_recommendations.length > 0 ? (
                result.ai_recommendations.map((recommendation, index) => (
                  <div className="recommendation-item" key={index}>
                    <span className="recommendation-number">
                      {index + 1}
                    </span>

                    <p>{recommendation}</p>
                  </div>
                ))
              ) : (
                <p>
                  Gemini recommendations are currently unavailable.
                  Please check your backend terminal.
                </p>
              )}
            </div>

            <p className="disclaimer">
              This is a basic keyword-based skill match, not an official ATS
              score or a guarantee of how an employer's system will rank your
              resume.
            </p>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
