from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/')
def home():
    return "Flask Registration API is running!"

@app.route('/register', methods=['GET', 'POST'])
def register():

    # Browser request (GET)
    if request.method == 'GET':
        name = request.args.get('name', '')
        email = request.args.get('email', '')

    # Postman/API request (POST)
    else:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({
                "success": False,
                "message": "Request must contain JSON data"
            }), 400

        name = data.get('name', '')
        email = data.get('email', '')

    if not name or not email:
        return jsonify({
            "success": False,
            "message": "Name and email are required"
        }), 400

    if not is_valid_email(email):
        return jsonify({
            "success": False,
            "message": "Invalid email format"
        }), 400

    return jsonify({
        "success": True,
        "message": f"User {name} registered successfully with email {email}"
    })

if __name__ == '__main__':
    app.run(debug=True)