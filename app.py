# -*- coding: utf-8 -*-
"""app.py - DietAI Flask REST API."""
import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.json.ensure_ascii = False   # allow emoji and non-ASCII in JSON responses
app.json.sort_keys    = False   # preserve insertion order
CORS(app)

VALID_MODELS = ["logistic_regression", "decision_tree", "random_forest", "xgboost", "ann"]
REQUIRED_FIELDS = ["Age", "Gender", "Height_cm", "Weight_kg", "BMI",
                   "Activity_Level", "Sugar_Level", "Cholesterol", "Goal"]
METRICS_PATH = os.path.join(os.path.dirname(__file__), "models", "model_metrics.json")


def _lazy_imports():
    from src.predict import predict_diet
    from src.recommendation import get_diet_advice, get_all_diets
    return predict_diet, get_diet_advice, get_all_diets


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/predict", methods=["POST"])
def predict():
    predict_diet, get_diet_advice, _ = _lazy_imports()
    data = request.get_json(silent=True) or {}
    model_name = data.pop("model", "random_forest")
    if model_name not in VALID_MODELS:
        return jsonify({"error": f"Unknown model: {model_name}. Valid: {VALID_MODELS}"}), 400
    missing = [k for k in REQUIRED_FIELDS if k not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400
    try:
        result             = predict_diet(model_name, data)
        result["advice"]   = get_diet_advice(result["diet"])
        result["model_used"] = model_name
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/models", methods=["GET"])
def get_models():
    if not os.path.exists(METRICS_PATH):
        return jsonify({"error": "Model metrics not found. Run: python src/evaluate.py"}), 404
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@app.route("/api/diets", methods=["GET"])
def get_diets():
    _, _, get_all_diets = _lazy_imports()
    return jsonify(get_all_diets())


@app.route("/api/diet-info/<diet_name>", methods=["GET"])
def diet_info(diet_name):
    _, get_diet_advice, _ = _lazy_imports()
    info = get_diet_advice(diet_name)
    if not info:
        return jsonify({"error": f"Diet not found: {diet_name}"}), 404
    return jsonify(info)


@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify({
        "total_patients":   1000,
        "diet_classes":     5,
        "features":         9,
        "models_available": VALID_MODELS,
        "best_model":       "xgboost",
        "best_accuracy":    100.0,
        "dataset":          "diet_recommendation_dataset_1000.csv",
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "DietAI", "version": "1.0.0"})


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found", "code": 404}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "code": 500}), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
