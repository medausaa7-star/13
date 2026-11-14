from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response = client.chat.completions.create(
        model="gpt-5.6-terra",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    ai_reply = response.choices[0].message.content

    return jsonify({
        "user_message": user_message,
        "ai_response": ai_reply
    })

if __name__ == '__main__':
    app.run(debug=True)
