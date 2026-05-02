from agents.agents import analyze_cv, analyze_job, improve_cover_letter

def run_pipeline(cv_text, cl_text, job_text):
    job_data = analyze_job(job_text)

    cv_analysis = analyze_cv(cv_text, job_text)

    cl_analysis = improve_cover_letter(cl_text, job_text)

    return {
        "job_analysis": job_data,
        "cv_analysis": cv_analysis,
        "cover_letter": cl_analysis
    }