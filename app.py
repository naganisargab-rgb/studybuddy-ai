import os

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from google import genai

# Read settings from the .env file
load_dotenv(override=True)

app = Flask(__name__)

# Read the private API key
api_key = os.getenv("GEMINI_API_KEY")
print("KEY CHECK:", (api_key or "")[:3], len(api_key or ""))

# Prepare the AI client
client = genai.Client(api_key=api_key) if api_key else None

# Gemma 4 model
MODEL = "gemma-4-26b-a4b-it"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/study", methods=["POST"])
def study():
    data = request.get_json(silent=True) or {}
    topic = str(data.get("topic", "")).strip()

    if not topic:
        return jsonify({"error": "Please enter a topic."}), 400

    if len(topic) > 5000:
        return jsonify({"error": "Please enter a shorter topic."}), 400

    if client is None:
        return jsonify({
            "error": "API key missing. Check your .env file."
        }), 500

    prompt = f"""
    You are StudyBuddy AI, a friendly college tutor.

    Explain the following topic in simple language:
    {topic}

    Include:
    1. A simple definition
    2. A step-by-step explanation
    3. One example
    4. Three important points to remember
    """

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return jsonify({
            "answer": response.text or "No answer was returned."
        })

    except Exception as e:
        app.logger.exception("Gemma API request failed")
        return jsonify({
            "error": f"AI request failed. {str(e)[:300]}"
        }), 502


if __name__ == "__main__":
    app.run(debug=True)