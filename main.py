from flask import Flask, request, jsonify
from quiz_solver import solve_quiz
from dotenv import load_dotenv

load_dotenv()

SECRET = "my_shared_secret123"  # Use your secret here

app = Flask(__name__)

@app.route("/", methods=["POST"])
def api_handler():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    if not data or "email" not in data or "secret" not in data or "url" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if data["secret"] != SECRET:
        return jsonify({"error": "Forbidden"}), 403

    try:
        response = solve_quiz(data["email"], data["secret"], data["url"])
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
