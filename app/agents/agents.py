import os
import json
from groq import Groq
from dotenv import load_dotenv
import re

# Load env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not set")

client = Groq(api_key=api_key)


def extract_json(text: str):
    # Remove <think>...</think>
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # Extract JSON block
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("No JSON found")

    return match.group(0)

def analyze_job(job_text: str) -> dict:
    prompt = f"""
        Extract structured job requirements.

        JOB:
        \"\"\"{job_text}\"\"\"

        RETURN JSON:
        {{
        "title": "",
        "skills_required": [],
        "experience_level": "",
        "location": "",
        "language_requirements": [],
        "key_responsibilities": [],
        "tools_technologies": []
        }}
        """

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": "You extract structured job data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    print("Job Analysis Response:", response)

    content = response.choices[0].message.content

    try:
        json_str = extract_json(content)
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON", "raw": content}
    
def analyze_cv(cv_text: str, job_text: str) -> dict:
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
"""

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": "You are a professional resume optimizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    try:
        json_str = extract_json(content)
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON", "raw": content}
    
def improve_cover_letter(cl_text: str, job_text: str) -> dict:
    prompt = f"""
Rewrite and optimize this cover letter for the job.

CL:
\"\"\"{cl_text}\"\"\"

JOB:
\"\"\"{job_text}\"\"\"

RETURN JSON:
{{
  "improved_version": "",
  "key_changes": []
}}
"""

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": "You improve cover letters professionally."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    content = response.choices[0].message.content

    try:
        json_str = extract_json(content)
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON", "raw": content}