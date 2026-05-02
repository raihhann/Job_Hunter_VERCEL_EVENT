from groq import Groq
import json
import os

# =========================
# API KEY SETUP
# =========================
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)


# =========================
# MAIN FUNCTION
# =========================
def analyze_application(cv_text, cover_letter_text, job_text):

    prompt = f"""
You are an expert resume and cover letter optimization system.

INPUT:

1. CV:
\"\"\"{cv_text}\"\"\"

2. Cover Letter:
\"\"\"{cover_letter_text}\"\"\"

3. Job Description:
\"\"\"{job_text}\"\"\"

TASK:
Analyze and improve CV + Cover Letter for this job.

OUTPUT FORMAT (JSON ONLY):
{{
  "match_score": "0-100",

  "cv_analysis": {{
    "missing_keywords": [],
    "skills_to_add": [],
    "experience_improvements": [
      {{
        "original": "",
        "improved": ""
      }}
    ],
    "ats_tips": []
  }},

  "cover_letter_analysis": {{
    "issues": [],
    "improvements": [],
    "rewritten_cover_letter": ""
  }},

  "job_alignment": {{
    "strengths": [],
    "gaps": [],
    "recommendations": []
  }},

  "general_feedback": []
}}

IMPORTANT:
- Be specific and job-focused
- Use strong action verbs
- Return ONLY valid JSON
"""

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": "You are a professional career coach and ATS optimizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception as e:
        print("⚠️ Failed to parse JSON response")
        print(content)
        return None


# =========================
# MOCK DATA (TESTING)
# =========================

cv_text = """
Software Engineer with 3 years of experience in Python, embedded systems, and IoT development.

Experience:
- Developed firmware for ESP32-based IoT devices for real-time sensor monitoring.
- Built data pipelines in Python for hardware telemetry analysis.
- Worked with STM32 and ESP32 microcontrollers.
- Designed REST APIs for device communication.

Skills:
Python, C++, Embedded C, ESP32, IoT, Linux, RTOS, Git
"""


cover_letter_text = """
Dear Hiring Manager,

I am applying for this role because I have strong experience in Python and embedded systems. I have worked extensively with IoT devices and ESP32 platforms.

I believe my background aligns well with your requirements.

Thank you for your time.
"""


job_text = """
We are seeking a Software Engineer with experience in Python, C++, embedded systems, RTOS, and IoT development.

Responsibilities:
- Develop embedded software for IoT devices
- Work with real-time operating systems
- Optimize firmware for microcontrollers
- Integrate hardware and software systems

Requirements:
- Strong Python and C++ skills
- Experience with ESP32 or similar MCUs
- Knowledge of RTOS and embedded Linux
- Experience in IoT and real-time systems
"""


# =========================
# RUN TEST
# =========================
if __name__ == "__main__":

    print("🚀 Running CV Analyzer...\n")

    result = analyze_application(cv_text, cover_letter_text, job_text)

    if result:
        print("\n📊 FINAL OUTPUT:\n")
        print(json.dumps(result, indent=2))
    else:
        print("❌ Analysis failed")