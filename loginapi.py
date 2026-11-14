from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded credentials
USERNAME = "admin"
PASSWORD = "12345"


@app.route('/')
def home():
    return """
    <h1>Task Manager API</h1>
    <p>Login API is available at POST /login</p>
    """


@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if username == USERNAME and password == PASSWORD:
        return jsonify({
            "message": "Login successful"
        }), 200

    return jsonify({
        "message": "Invalid username or password"
    }), 401


if __name__ == '__main__':
    app.run(debug=True)