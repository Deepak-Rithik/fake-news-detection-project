from flask import Blueprint, request, jsonify
import sqlite3
import joblib
import os

api = Blueprint("api", __name__)

DATABASE = "database/database.db"

MODEL_PATH = "model/model.pkl"
VECTORIZER_PATH = "model/vectorizer.pkl"

# Load ML Model
if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    model = None
    vectorizer = None


def save_prediction(username, news, prediction):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history(username, news, prediction)
        VALUES (?, ?, ?)
    """, (username, news, prediction))

    conn.commit()
    conn.close()


@api.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Fake News Detection API is running"
    })


@api.route("/api/predict", methods=["POST"])
def predict():

    if model is None or vectorizer is None:
        return jsonify({
            "status": "error",
            "message": "Model not found"
        }), 500

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON body required"
        }), 400

    news = data.get("news", "").strip()
    username = data.get("username", "API User")

    if news == "":
        return jsonify({
            "status": "error",
            "message": "News text cannot be empty"
        }), 400

    transformed = vectorizer.transform([news])

    prediction = model.predict(transformed)[0]

    result = "Real News" if prediction == 1 else "Fake News"

    save_prediction(username, news, result)

    return jsonify({
        "status": "success",
        "prediction": result,
        "username": username
    })


@api.route("/api/history", methods=["GET"])
def history():

    username = request.args.get("username")

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    if username:
        cursor.execute("""
            SELECT *
            FROM history
            WHERE username=?
            ORDER BY id DESC
        """, (username,))
    else:
        cursor.execute("""
            SELECT *
            FROM history
            ORDER BY id DESC
        """)

    rows = cursor.fetchall()

    conn.close()

    history = []

    for row in rows:
        history.append({
            "id": row["id"],
            "username": row["username"],
            "news": row["news"],
            "prediction": row["prediction"]
        })

    return jsonify(history)
