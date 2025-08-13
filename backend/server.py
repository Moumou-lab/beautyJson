from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def is_plain_object(v):
    return isinstance(v, dict)

def path_to_string(path_arr):
    return ".".join(f"[{seg}]" if isinstance(seg, int) else seg for seg in path_arr)

def walk_and_rebuild(obj, path, order_store):
    if isinstance(obj, list):
        return [walk_and_rebuild(v, path + [i], order_store) for i, v in enumerate(obj)]
    if not is_plain_object(obj):
        return obj
    key = path_to_string(path)
    stored_order = order_store.get(key)
    keys = list(obj.keys())
    if stored_order:
        known = [k for k in stored_order if k in keys]
        rest = [k for k in keys if k not in stored_order]
        ordered_keys = known + rest
    else:
        ordered_keys = keys
    return {k: walk_and_rebuild(obj[k], path + [k], order_store) for k in ordered_keys}

@app.route("/api/reorder", methods=["POST"])
def reorder():
    payload = request.get_json(silent=True)
    if not payload or "json" not in payload or "orders" not in payload:
        return jsonify({"error": "invalid payload"}), 400
    try:
        rebuilt = walk_and_rebuild(payload["json"], [], payload["orders"])
        return jsonify({"data": rebuilt})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5174)
