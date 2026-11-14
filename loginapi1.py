from flask import Flask, request, jsonify

app = Flask(__name__)

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"


@app.route('/login', methods=['GET', 'POST'])
def login():

    # Display message when opened in browser
    if request.method == 'GET':
        return """
        <h2>Login API</h2>
        <p>This API requires a POST request.</p>
        <p>Use Thunder Client to test:</p>
        <p>POST http://127.0.0.1:5000/login</p>
        """

    # Process POST request
    data = request.get_json()

    username = data.get('username', '')
    password = data.get('password', '')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify({
            "success": True,
            "message": "Login successful"
        })

    return jsonify({
        "success": False,
        "message": "Invalid username or password"
    }), 401


if __name__ == '__main__':
    app.run(debug=True)