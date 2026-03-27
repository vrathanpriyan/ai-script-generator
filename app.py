
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers.pipelines import pipeline
app = Flask(__name__)
CORS(app)
generator = pipeline("text-generation", model="gpt2", framework="pt")
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    if data is None:
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
    result = generator(prompt, max_length=200, temperature=0.7)
    try:
        result_list = list(result) if result else []
        if result_list and len(result_list) > 0:
            script = result_list[0].get('generated_text', '') if isinstance(result_list[0], dict) else str(result_list[0])
        else:
            script = ''
    except (TypeError, AttributeError, KeyError):
        script = ''

    return jsonify({
        "script": script
    })
if __name__ == "__main__":
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)