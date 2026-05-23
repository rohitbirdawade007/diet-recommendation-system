"""
src/predict.py â€” Load saved models and return diet prediction + probabilities
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import joblib

from config import MODEL_PATHS, SCALER_PATH, ENCODER_PATH, FEATURE_COLUMNS

# Simple in-process cache so models are loaded only once
_cache: dict = {}


def _get_artifacts():
    if "scaler" not in _cache:
        _cache["scaler"]  = joblib.load(SCALER_PATH)
        _cache["encoder"] = joblib.load(ENCODER_PATH)
    return _cache["scaler"], _cache["encoder"]


def _get_model(name: str):
    if name not in _cache:
        # All models (including ANN/MLP) are stored via joblib
        _cache[name] = joblib.load(MODEL_PATHS[name])
    return _cache[name]


def predict_diet(model_name: str, input_dict: dict) -> dict:
    """
    Parameters
    ----------
    model_name : one of logistic_regression | decision_tree |
                 random_forest | xgboost | ann
    input_dict : dict with keys matching FEATURE_COLUMNS

    Returns
    -------
    {diet, confidence, probabilities}
    """
    scaler, le = _get_artifacts()
    model       = _get_model(model_name)

    # Build feature vector in the exact column order
    features        = np.array([[float(input_dict[c]) for c in FEATURE_COLUMNS]])
    features_scaled = scaler.transform(features)

    predicted_idx = int(model.predict(features_scaled)[0])
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(features_scaled)[0]
    else:
        probs = np.zeros(len(le.classes_))
        probs[predicted_idx] = 1.0

    predicted_diet = le.inverse_transform([predicted_idx])[0]
    confidence     = float(probs[predicted_idx]) * 100

    prob_dict = {
        le.inverse_transform([i])[0]: round(float(p) * 100, 2)
        for i, p in enumerate(probs)
    }

    return {
        "diet":          predicted_diet,
        "confidence":    round(confidence, 2),
        "probabilities": prob_dict,
    }


if __name__ == "__main__":
    # Quick smoke test
    sample = {
        "Age": 35, "Gender": 1, "Height_cm": 175, "Weight_kg": 80,
        "BMI": 26.1, "Activity_Level": 1, "Sugar_Level": 120,
        "Cholesterol": 200, "Goal": 0
    }
    for name in ["logistic_regression", "decision_tree", "random_forest", "xgboost", "ann"]:
        res = predict_diet(name, sample)
        print(f"{name:25s} â†’ {res['diet']} ({res['confidence']:.1f}%)")

