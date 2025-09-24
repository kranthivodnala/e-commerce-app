from flask import Flask, jsonify, request, abort

app = Flask(__name__)
users = {}   # user_id -> {id, name, email}
next_id = 1

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "users"})

@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(list(users.values()))

@app.route("/users", methods=["POST"])
def create_user():
    global next_id
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        abort(400, "name and email required")
    user = {"id": next_id, "name": name, "email": email}
    users[next_id] = user
    next_id += 1
    return jsonify(user), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        abort(404)
    return jsonify(user)

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return '', 204
    abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
