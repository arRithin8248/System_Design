from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "users.json"

# -------------------------------
# Load users from file
# -------------------------------
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# -------------------------------
# Save users to file
# -------------------------------
def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Initialize users
users = load_users()

# -------------------------------
# CREATE USER
# -------------------------------
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    # Validation
    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "Name and age required"}), 400

    if not isinstance(data["age"], int) or data["age"] <= 0:
        return jsonify({"error": "Age must be positive integer"}), 400

    # Create user
    user = {
        "id": len(users),
        "name": data["name"],
        "age": data["age"]
    }

    users.append(user)
    save_users(users)

    return jsonify({"message": "User created", "user": user}), 201

# -------------------------------
# GET ALL USERS (with search)
# -------------------------------
@app.route('/users', methods=['GET'])
def get_users():
    name = request.args.get("name")

    if name:
        filtered = [u for u in users if u["name"].lower() == name.lower()]
        return jsonify(filtered)

    return jsonify(users)

# -------------------------------
# GET SINGLE USER
# -------------------------------
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)

    return jsonify({"error": "User not found"}), 404

# -------------------------------
# UPDATE USER
# -------------------------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json

    for user in users:
        if user["id"] == user_id:

            # Validation
            if "name" in data:
                user["name"] = data["name"]

            if "age" in data:
                if not isinstance(data["age"], int) or data["age"] <= 0:
                    return jsonify({"error": "Invalid age"}), 400
                user["age"] = data["age"]

            save_users(users)
            return jsonify({"message": "User updated", "user": user})

    return jsonify({"error": "User not found"}), 404

# -------------------------------
# DELETE USER
# -------------------------------
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for i, user in enumerate(users):
        if user["id"] == user_id:
            deleted = users.pop(i)
            save_users(users)
            return jsonify({"message": "User deleted", "user": deleted})

    return jsonify({"error": "User not found"}), 404

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)