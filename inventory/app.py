from flask import Flask, jsonify, request, abort

app = Flask(__name__)
inventory = {}  # sku -> {sku, name, qty}

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "inventory"})

@app.route("/inventory", methods=["GET"])
def list_inventory():
    return jsonify(list(inventory.values()))

@app.route("/inventory/<sku>", methods=["GET"])
def get_item(sku):
    item = inventory.get(sku)
    if not item:
        abort(404)
    return jsonify(item)

@app.route("/inventory/<sku>", methods=["PUT"])
def upsert_item(sku):
    data = request.get_json() or {}
    name = data.get("name")
    qty = data.get("qty", 0)
    inventory[sku] = {"sku": sku, "name": name or sku, "qty": qty}
    return jsonify(inventory[sku])

@app.route("/inventory/<sku>/adjust", methods=["POST"])
def adjust_qty(sku):
    data = request.get_json() or {}
    delta = data.get("delta")
    if delta is None:
        abort(400, "delta required")
    if sku not in inventory:
        abort(404)
    inventory[sku]["qty"] += int(delta)
    return jsonify(inventory[sku])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
