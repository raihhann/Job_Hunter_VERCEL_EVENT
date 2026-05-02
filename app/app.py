from flask import Flask, request, jsonify
from parsers.file_parser import parse_file
from parsers.job_parser import parse_job_url

app = Flask(__name__)

# ---- CV PARSER ----
@app.route("/api/cv-parser", methods=["POST"])
def cv_parser():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    try:
        text = parse_file(file)
        return jsonify({
            "type": "cv",
            "extracted_text": text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---- COVER LETTER PARSER ----
@app.route("/api/cover-letter-parser", methods=["POST"])
def cover_letter_parser():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    try:
        text = parse_file(file)
        return jsonify({
            "type": "cover_letter",
            "extracted_text": text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---- JOB URL PARSER ----
@app.route("/api/job-url", methods=["POST"])
def job_url_parser():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"]

    try:
        text = parse_job_url(url)
        return jsonify({
            "url": url,
            "job_description": text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)