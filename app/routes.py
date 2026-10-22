import os
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('routes', __name__)

@bp.route('/health')
def health():
    return jsonify({"status": "ok"})

@bp.route('/products')
def products():
    category = request.args.get('category', '')
    # Vulnerable SQL query (intentional)
    sql = f"SELECT id, name, price FROM products WHERE category = '{category}' AND is_public = 1"
    rows = current_app.db.execute(sql).fetchall()
    # Convert rows to list of dicts
    result = [{"id": row["id"], "name": row["name"], "price": row["price"]} for row in rows]
    return jsonify(result)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"ok": False}), 400
    # Parameterised query for security
    sql = "SELECT password_hash FROM users WHERE username = ?"
    row = current_app.db.execute(sql, (username,)).fetchone()
    if row and current_app.db.row_factory == None:
        # Not expected, fallback
        return jsonify({"ok": False}), 401
    from werkzeug.security import check_password_hash
    if row and check_password_hash(row["password_hash"], password):
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 401
