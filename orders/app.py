from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)
orders = {}   # order_id -> {id, user_id, items, status, created_at}
next_id = 1

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "orders"})

@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(list(orders.values()))

@app.route("/orders", methods=["POST"])
def create_order():
    global next_id
    data = request.get_json() or {}
    user_id = data.get("user_id")
    items = data.get("items", [])
    if not user_id or not isinstance(items, list):
        abort(400, "user_id and items[] required")
    order = {
        "id": next_id,
        "user_id": user_id,
        "items": items,
        "status": "created",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    orders[next_id] = order
    next_id += 1
    return jsonify(order), 201

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    o = orders.get(order_id)
    if not o:
        abort(404)
    return jsonify(o)

@app.route("/orders/<int:order_id>/status", methods=["PUT"])
def update_status(order_id):
    data = request.get_json() or {}
    status = data.get("status")
    if not status:
        abort(400, "status required")
    o = orders.get(order_id)
    if not o:
        abort(404)
    o["status"] = status
    return jsonify(o)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
