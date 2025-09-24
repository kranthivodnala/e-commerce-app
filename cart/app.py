from flask import Flask, jsonify, request, abort

app = Flask(__name__)
carts = {}  # user_id -> list of items

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "cart"})

@app.route("/cart/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    return jsonify(carts.get(user_id, []))

@app.route("/cart/<int:user_id>/add", methods=["POST"])
def add_item(user_id):
    data = request.get_json() or {}
    sku = data.get("sku")
    qty = int(data.get("qty", 1))
    if not sku:
        abort(400, "sku required")
    carts.setdefault(user_id, []).append({"sku": sku, "qty": qty})
    return jsonify(carts[user_id])

@app.route("/cart/<int:user_id>/clear", methods=["POST"])
def clear_cart(user_id):
    carts[user_id] = []
    return jsonify(carts[user_id])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
