from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory database
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    {"id": 4, "name": "Diana", "email": "diana@example.com"},
    {"id": 5, "name": "Eve", "email": "eve@example.com"}
]

# Get all users
@app.route("/users", methods=["GET"])

def get_users():
    return jsonify(users), 200

# Get a user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)

    if user:
        return jsonify(user), 200

    return jsonify({"message": "User not found"}), 404
if __name__ == "__main__":
    app.run(debug=True)