
import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing")

# Configure the client and request timeout
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=120000
    )
)


@app.route("/", methods=["GET"])
def home():
    return "Chat API is running!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    # Make sure the request contains a JSON object
    if not isinstance(data, dict):
        return jsonify({
            "error": "Send a valid JSON object"
        }), 400

    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "error": "Please enter a valid message"
        }), 400

    message = message.strip()

    try:
        print("Sending message to Gemini...", flush=True)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message,
            config=types.GenerateContentConfig(
                max_output_tokens=200
            )
        )

        return jsonify({
            "user_message": message,
            "ai_response": response.text
        })

    except Exception as e:
        error_message = str(e)
        print("Gemini error:", error_message, flush=True)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            return jsonify({
                "error": "Gemini is temporarily busy.",
                "message": "Please wait a few seconds and try again."
            }), 503

        return jsonify({
            "error": "AI service request failed",
            "details": error_message
        }), 502

if __name__ == "__main__":
    app.run(debug=True)

