from groq import Groq
import json

# Initialize Groq client
client = Groq(api_key="API_KEY_HERE")

def analyze_cv(cv_text, job_text):
    prompt = f"""
You are an expert resume reviewer and ATS optimization system.

INPUT:
1. Candidate CV:
\"\"\"{cv_text}\"\"\"

2. Job Description:
\"\"\"{job_text}\"\"\"

TASK:
Analyze the CV against the job description and provide structured suggestions.

OUTPUT FORMAT (JSON ONLY):
{{
  "match_score": "percentage (0-100)",
  "missing_keywords": [],
  "skills_to_add": [],
  "experience_improvements": [
    {{
      "original": "",
      "improved": ""
    }}
  ],
  "summary_improvement": "",
  "ats_optimization_tips": [],
  "general_feedback": []
}}

IMPORTANT:
- Be specific and actionable
- Improve bullet points using strong action verbs
- Align suggestions strictly with job description
- Do NOT return anything except valid JSON
"""

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",  # or mixtral-8x7b
        messages=[
            {"role": "system", "content": "You are a professional resume optimizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    # Try parsing JSON safely
    try:
        return json.loads(content)
    except:
        print("⚠️ Raw response (not valid JSON):")
        print(content)
        return None


# ---------------------------
# Example usage
# ---------------------------

if __name__ == "__main__":
    cv_text = """
    Software engineer with experience in Python and embedded systems.
    Worked on ESP32 and IoT projects.
    """

    job_text = """
    Looking for a Software Engineer with experience in Python, C++, RTOS,
    embedded Linux, and IoT systems. Experience with real-time data processing preferred.
    """

    result = analyze_cv(cv_text, job_text)

    if result:
        print(json.dumps(result, indent=2))