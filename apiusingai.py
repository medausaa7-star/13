
from flask import Flask, request, jsonify
import re

app = Flask(__name__)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "status_code": 400,
            "message": "Request body must be valid JSON"
        }), 400

    name = data.get('name', '')
    email = data.get('email', '')
    password = data.get('password', '')

    # Validate required fields
    if (
        not isinstance(name, str) or not name.strip()
        or not isinstance(email, str) or not email.strip()
        or not isinstance(password, str) or not password.strip()
    ):
        return jsonify({
            "success": False,
            "status_code": 400,
            "message": "Validation Error",
            "errors": {
                "name": "Name is required" if not isinstance(name, str) or not name.strip() else None,
                "email": "Email is required" if not isinstance(email, str) or not email.strip() else None,
                "password": "Password is required" if not isinstance(password, str) or not password.strip() else None
            }
        }), 400

    name = name.strip()
    email = email.strip()
    password = password.strip()

    # Validate email format
    if not is_valid_email(email):
        return jsonify({
            "success": False,
            "status_code": 400,
            "message": "Validation Error",
            "errors": {
                "email": "Invalid email format. Please provide a valid email address"
            }
        }), 400

    # Successful registration (not saved to a database)
    return jsonify({
        "success": True,
        "status_code": 201,
        "message": f"User {name} registered successfully",
        "data": {
            "name": name,
            "email": email
        }
    }), 201


if __name__ == '__main__':
    app.run(debug=True)
