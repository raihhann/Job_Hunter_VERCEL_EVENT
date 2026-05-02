from flask import Flask, request, jsonify
from flask_cors import CORS
from parsers.file_parser import parse_file
from parsers.job_parser import parse_job_url
from services.pipeline import run_pipeline

app = Flask(__name__)
CORS(app)
@app.route("/api/analyze-cv", methods=["POST"])
def analyze_cv():
    try:
        if "cv" not in request.files:
            return jsonify({"error": "CV missing"}), 400

        if "cover_letter" not in request.files:
            return jsonify({"error": "Cover letter missing"}), 400

        if "url" not in request.form:
            return jsonify({"error": "Job URL missing"}), 400

        cv_file = request.files["cv"]
        cover_file = request.files["cover_letter"]
        url = request.form["url"]

        cv_text = parse_file(cv_file)
        cover_text = parse_file(cover_file)
        job_text = parse_job_url(url)

        result = run_pipeline(cv_text, cover_text, job_text)
        # print(result)
        return jsonify({
            "status": "success",
            "result": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)