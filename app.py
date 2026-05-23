"""
app.py â€” Flask REST API for the Diet Recommendation System
"""
import os
import sys
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import METRICS_PATH, MODELS_DIR
from src.predict import predict_diet
from src.recommendation import get_diet_advice, get_all_diets

# ──────────────────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="static", static_url_path="/static")
app.json.ensure_ascii = False          # allow emoji + non-ASCII in JSON responses
CORS(app)


# ──────────────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# â”€â”€â”€ API: Predict â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        model_name = data.get("model", "random_forest")
        valid_models = [
            "logistic_regression", "decision_tree",
            "random_forest", "xgboost", "ann"
        ]
        if model_name not in valid_models:
            return jsonify({"error": f"Unknown model '{model_name}'"}), 400

        required = [
            "Age", "Gender", "Height_cm", "Weight_kg", "BMI",
            "Activity_Level", "Sugar_Level", "Cholesterol", "Goal"
        ]
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        input_dict = {k: float(data[k]) for k in required}
        result     = predict_diet(model_name, input_dict)

        # Attach rich diet advice (without non-JSON-friendly keys)
        advice = get_diet_advice(result["diet"])
        result["advice"] = advice

        return jsonify(result)

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# â”€â”€â”€ API: Model metrics â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.route("/api/models", methods=["GET"])
def get_models():
    try:
        if not os.path.exists(METRICS_PATH):
            return jsonify({"error": "Run src/evaluate.py first to generate metrics."}), 404
        with open(METRICS_PATH) as f:
            return jsonify(json.load(f))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# â”€â”€â”€ API: Diet info for a single diet â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.route("/api/diet-info/<path:diet_name>", methods=["GET"])
def diet_info(diet_name: str):
    label  = diet_name.replace("-", " ").title()
    advice = get_diet_advice(label)
    return jsonify(advice)


# â”€â”€â”€ API: All diets â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.route("/api/diets", methods=["GET"])
def all_diets():
    return jsonify(get_all_diets())


# â”€â”€â”€ API: Dataset statistics â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify({
        "total_patients": 1000,
        "features":       9,
        "diet_classes":   5,
        "class_distribution": {
            "Diabetic":      539,
            "Low Carb":      255,
            "Heart Healthy":  92,
            "High Protein":   70,
            "Balanced":       44,
        },
        "models_available": [
            "logistic_regression", "decision_tree",
            "random_forest", "xgboost", "ann"
        ],
    })


# â”€â”€â”€ Run â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

