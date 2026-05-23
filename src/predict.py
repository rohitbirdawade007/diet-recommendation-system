# -*- coding: utf-8 -*-
"""src/predict.py - Load models and return diet predictions with probabilities."""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import joblib
from config import MODEL_PATHS, SCALER_PATH, ENCODER_PATH, FEATURE_COLUMNS

# In-process model cache: avoids repeated disk I/O on every prediction
_model_cache: dict = {}


def _get_artifacts():
    """Lazy-load and cache scaler + label encoder."""
    if 'scaler' not in _model_cache:
        _model_cache['scaler']  = joblib.load(SCALER_PATH)
        _model_cache['encoder'] = joblib.load(ENCODER_PATH)
    return _model_cache['scaler'], _model_cache['encoder']


def _get_model(name: str):
    """Lazy-load and cache a named ML model."""
    if name not in _model_cache:
        path = MODEL_PATHS.get(name)
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        _model_cache[name] = joblib.load(path)
    return _model_cache[name]


def predict_diet(model_name: str, input_dict: dict) -> dict:
    """
    Run inference for a given model and input feature set.

    Parameters
    ----------
    model_name : str
        One of: logistic_regression, decision_tree, random_forest, xgboost, ann
    input_dict : dict
        Feature values keyed by FEATURE_COLUMNS names.

    Returns
    -------
    dict with keys: diet, confidence, probabilities
    """
    scaler, le = _get_artifacts()
    model      = _get_model(model_name)

    features   = np.array([[float(input_dict[c]) for c in FEATURE_COLUMNS]])
    features_s = scaler.transform(features)

    predicted_idx = int(model.predict(features_s)[0])

    if hasattr(model, 'predict_proba'):
        probs = model.predict_proba(features_s)[0]
    else:
        probs = np.zeros(len(le.classes_), dtype=float)
        probs[predicted_idx] = 1.0

    diet       = le.inverse_transform([predicted_idx])[0]
    confidence = round(float(probs[predicted_idx]) * 100, 2)
    prob_dict  = {
        le.inverse_transform([i])[0]: round(float(p) * 100, 2)
        for i, p in enumerate(probs)
    }

    return {'diet': diet, 'confidence': confidence, 'probabilities': prob_dict}


def clear_cache():
    """Clear the in-process model cache (useful for testing)."""
    _model_cache.clear()
