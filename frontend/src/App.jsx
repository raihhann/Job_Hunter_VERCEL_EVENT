import { useState } from "react";
import axios from "axios";

export default function App() {
  const [cv, setCv] = useState(null);
  const [cover, setCover] = useState(null);
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [raw, setRaw] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    if (!cv || !cover || !url) {
      alert("Upload CV, Cover Letter and URL");
      return;
    }

    const form = new FormData();
    form.append("cv", cv);
    form.append("cover_letter", cover);
    form.append("url", url);

    setLoading(true);
    setResult(null);
    setRaw(null);

    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/api/analyze-cv",
        form
      );

      const data = res.data.result;

      // 🔥 Handle error case
      if (data?.error) {
        setRaw(data.raw);
      }

      setResult(data);
    } catch (err) {
      console.log(err);
      alert(err.response?.data?.message || "Network error");
    }

    setLoading(false);
  };

  const safe = (arr) => (Array.isArray(arr) ? arr : []);

  const cleanText = (text) =>
    typeof text === "string" ? text.replace(/<think>[\s\S]*?<\/think>/g, "") : "";

  const r = result || {};
  const cvA = r.cv_analysis || {};
  const coverA = r.cover_letter_analysis || {};
  const jobA = r.job_alignment || {};

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>🚀 AI CV Analyzer</h1>

      {/* INPUT */}
      <div style={styles.card}>
        <input type="file" onChange={(e) => setCv(e.target.files[0])} />
        <input type="file" onChange={(e) => setCover(e.target.files[0])} />

        <input
          placeholder="Job URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={styles.input}
        />

        <button onClick={analyze} style={styles.button}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {/* RESULT */}
      {result && (
        <div style={styles.result}>
          <h2>📊 Result</h2>

          <h3>Match Score: {r.match_score || "N/A"}</h3>

          {/* CV */}
          <Section title="CV Missing Keywords" items={safe(cvA.missing_keywords)} />
          <Section title="Skills to Add" items={safe(cvA.skills_to_add)} />
          <Section title="ATS Tips" items={safe(cvA.ats_tips)} />

          {/* Cover Letter */}
          <Section title="Cover Letter Issues" items={safe(coverA.issues)} />
          <Section title="Improvements" items={safe(coverA.improvements)} />

          {/* Job */}
          <Section title="Job Strengths" items={safe(jobA.strengths)} />
          <Section title="Job Gaps" items={safe(jobA.gaps)} />

          {/* Rewritten Letter */}
          {coverA.rewritten_cover_letter && (
            <div style={styles.block}>
              <h3>✉️ Rewritten Cover Letter</h3>
              <pre style={styles.pre}>
                {cleanText(coverA.rewritten_cover_letter)}
              </pre>
            </div>
          )}

          {/* RAW fallback */}
          {raw && (
            <div style={styles.raw}>
              <h3>⚠️ Raw Output (Debug)</h3>
              <pre style={styles.pre}>{raw}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

/* ---------------- COMPONENT ---------------- */

function Section({ title, items }) {
  return (
    <div style={styles.block}>
      <h3>{title}</h3>

      {items.length > 0 ? (
        <ul>
          {items.map((i, idx) => (
            <li key={idx}>{i}</li>
          ))}
        </ul>
      ) : (
        <p style={{ opacity: 0.6 }}>No data available</p>
      )}
    </div>
  );
}

/* ---------------- STYLES ---------------- */

const styles = {
  page: {
    fontFamily: "Arial",
    background: "#0f172a",
    color: "white",
    minHeight: "100vh",
    padding: "20px",
  },
  title: {
    fontSize: "26px",
    marginBottom: "20px",
  },
  card: {
    background: "#1e293b",
    padding: "15px",
    borderRadius: "10px",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    maxWidth: "500px",
  },
  input: {
    padding: "10px",
    borderRadius: "6px",
    border: "none",
  },
  button: {
    padding: "10px",
    background: "#3b82f6",
    border: "none",
    color: "white",
    cursor: "pointer",
    borderRadius: "6px",
  },
  result: {
    marginTop: "20px",
    background: "#111827",
    padding: "15px",
    borderRadius: "10px",
  },
  block: {
    marginTop: "10px",
    background: "#1f2937",
    padding: "10px",
    borderRadius: "8px",
  },
  raw: {
    marginTop: "20px",
    background: "#7f1d1d",
    padding: "10px",
    borderRadius: "8px",
  },
  pre: {
    whiteSpace: "pre-wrap",
    fontSize: "12px",
  },
};