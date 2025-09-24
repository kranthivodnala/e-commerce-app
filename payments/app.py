from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)
payments = {}  # payment_id -> {id, order_id, amount, status, created_at}
next_id = 1

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "payments"})

@app.route("/payments", methods=["POST"])
def create_payment():
    global next_id
    data = request.get_json() or {}
    order_id = data.get("order_id")
    amount = data.get("amount")
    if not order_id or amount is None:
        abort(400, "order_id and amount required")
    payment = {
        "id": next_id,
        "order_id": order_id,
        "amount": amount,
        "status": "processed",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    payments[next_id] = payment
    next_id += 1
    return jsonify(payment), 201

@app.route("/payments/<int:payment_id>", methods=["GET"])
def get_payment(payment_id):
    p = payments.get(payment_id)
    if not p:
        abort(404)
    return jsonify(p)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
