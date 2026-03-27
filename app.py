from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)

# 🔥 STRONG CORS FIX (handles preflight)
CORS(app, supports_credentials=True)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    data = request.json

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    topic = data.get("topic")

    prompt = f"""
Create a YouTube video script.

Topic: {topic}

Format:
Title:
Hook:
Intro:
Point 1:
Point 2:
Point 3:
Outro:

Make it engaging and simple.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        script = response.choices[0].message.content

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"script": script})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)