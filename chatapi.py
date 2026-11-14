
from flask import Flask, request, jsonify, render_template
from google import genai
import os
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("chat.html")
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")

    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({
            "error": "Message is required"
        }), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_message.strip()
        )

        return jsonify({
            "user_message": user_message,
            "ai_response": response.text
        })

    except Exception as e:
        app.logger.exception("Gemini API request failed")
        return jsonify({
            "error_type": type(e).__name__,
            "error_details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

