import { useState } from "react";
import axios from "axios";

export default function App() {
  const [cv, setCv] = useState(null);
  const [cover, setCover] = useState(null);
  const [url, setUrl] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyze = async () => {
    if (!cv || !cover || !url) {
      setError("Please upload CV, cover letter, and job URL");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const form = new FormData();
      form.append("cv", cv);
      form.append("cover_letter", cover);
      form.append("url", url);

      const res = await axios.post(
        "http://127.0.0.1:5000/api/analyze-cv",
        form
      );

      setData(res.data.result);
    } catch (err) {
      setError("API request failed");
    } finally {
      setLoading(false);
    }
  };

  const d = data || {};
  const cvA = d.cv_analysis || {};
  const coverA = d.cover_letter || {};
  const jobA = d.job_analysis || {};

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <h1>🚀 AI CV Dashboard</h1>

        {/* INPUT */}
        <div style={styles.card}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>📄 Upload CV</label>
            <input
              type="file"
              onChange={(e) => setCv(e.target.files[0])}
              style={styles.input}
            />
          </div>

          <div style={styles.inputGroup}>
            <label style={styles.label}>✉️ Upload Cover Letter</label>
            <input
              type="file"
              onChange={(e) => setCover(e.target.files[0])}
              style={styles.input}
            />
          </div>

          <div style={styles.inputGroup}>
            <label style={styles.label}>🔗 Enter Job URL</label>
            <input
              type="text"
              placeholder="https://..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              style={styles.textInput}
            />
          </div>

          <button
            onClick={analyze}
            style={styles.button}
            onMouseOver={(e) =>
              (e.target.style.opacity = "0.9")
            }
            onMouseOut={(e) =>
              (e.target.style.opacity = "1")
            }
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>

          {error && <p style={styles.error}>{error}</p>}
        </div>

        {/* DASHBOARD */}
        {data && (
          <div style={styles.dashboard}>
            {/* CV SECTION */}
            <h2 style={{ marginTop: "10px", fontWeight: 600 }}>
              📊 CV Analysis
            </h2>

            <h3>Match Score: {cvA.match_score || "N/A"}</h3>

            <Block title="Missing Keywords" items={cvA.missing_keywords} />
            <Block title="Skills to Add" items={cvA.skills_to_add} />
            <Block title="ATS Tips" items={cvA.ats_optimization_tips} />

            <div style={styles.block}>
              <h3>Summary Improvement</h3>
              <p>{cvA.summary_improvement || "No data"}</p>
            </div>

            <div style={styles.block}>
              <h3>Experience Improvements</h3>
              {Array.isArray(cvA.experience_improvements) &&
                cvA.experience_improvements.length > 0 ? (
                cvA.experience_improvements.map((exp, i) => (
                  <div key={i} style={styles.subBlock}>
                    <p><b>Original:</b> {exp.original}</p>
                    <p><b>Improved:</b> {exp.improved}</p>
                  </div>
                ))
              ) : (
                <p>No data</p>
              )}
            </div>

            {/* COVER LETTER */}
            <h2>✉️ Cover Letter</h2>

            <div style={styles.block}>
              <h3>Improved Version</h3>
              <pre style={styles.pre}>
                {coverA.improved_version || "No data"}
              </pre>
            </div>

            <Block title="Key Changes" items={coverA.key_changes} />

            {/* JOB ANALYSIS */}
            <h2>💼 Job Analysis</h2>

            <div style={styles.block}>
              <p><b>Title:</b> {jobA.title}</p>
              <p><b>Location:</b> {jobA.location}</p>
              <p><b>Experience Level:</b> {jobA.experience_level}</p>
            </div>

            <Block title="Skills Required" items={jobA.skills_required} />
            <Block title="Responsibilities" items={jobA.key_responsibilities} />
            <Block title="Languages" items={jobA.language_requirements} />
            <Block title="Technologies" items={jobA.tools_technologies} />
          </div>
        )}
      </div>
    </div>
  );
}

/* ---------------- COMPONENT ---------------- */

function Block({ title, items = [] }) {
  return (
    <div style={styles.block}>
      <h3>{title}</h3>
      <ul>
        {Array.isArray(items) && items.length > 0 ? (
          items.map((i, idx) => <li key={idx}>{i}</li>)
        ) : (
          <li>No data</li>
        )}
      </ul>
    </div>
  );
}

/* ---------------- STYLES ---------------- */

const styles = {
  page: {
    fontFamily: "Inter, Arial",
    background: "linear-gradient(135deg, #0f172a, #020617)",
    color: "white",
    minHeight: "100vh",
    padding: "40px 20px",
  },

  container: {
    maxWidth: "900px",
    margin: "0 auto",
  },

  title: {
    textAlign: "center",
    fontSize: "42px",
    marginBottom: "30px",
    fontWeight: "600",
    letterSpacing: "0.5px",
  },

  card: {
    background: "rgba(30, 41, 59, 0.9)",
    backdropFilter: "blur(10px)",
    padding: "20px",
    borderRadius: "14px",
    display: "flex",
    flexDirection: "column",
    gap: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.4)",
    border: "1px solid rgba(255,255,255,0.05)",
  },

  inputGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "6px",
  },

  label: {
    fontSize: "14px",
    color: "#cbd5f5",
    fontWeight: "500",
    textAlign: "left"
  },

  input: {
    padding: "8px",
    background: "#020617",
    color: "white",
    border: "1px solid #334155",
    borderRadius: "8px",
  },

  textInput: {
    padding: "10px",
    background: "#020617",
    color: "white",
    border: "1px solid #334155",
    borderRadius: "8px",
    outline: "none",
  },

  button: {
    padding: "12px",
    background: "linear-gradient(90deg, #3b82f6, #6366f1)",
    color: "white",
    border: "none",
    borderRadius: "10px",
    fontWeight: "600",
    cursor: "pointer",
    transition: "all 0.2s ease",
  },

  dashboard: {
    marginTop: "30px",
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },

  block: {
    background: "rgba(31, 41, 55, 0.9)",
    padding: "16px",
    borderRadius: "12px",
    boxShadow: "0 6px 20px rgba(0,0,0,0.3)",
    border: "1px solid rgba(255,255,255,0.05)",
  },

  subBlock: {
    marginBottom: "10px",
    padding: "10px",
    background: "#020617",
    borderRadius: "8px",
  },

  pre: {
    whiteSpace: "pre-wrap",
    fontSize: "13px",
    background: "#020617",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #334155",
  },

  error: {
    color: "#f87171",
    fontSize: "13px",
  },
};