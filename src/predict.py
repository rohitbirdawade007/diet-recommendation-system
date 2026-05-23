# -*- coding: utf-8 -*-
"""src/predict.py - Load models and return diet predictions."""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, joblib
from config import MODEL_PATHS, SCALER_PATH, ENCODER_PATH, FEATURE_COLUMNS

_cache = {}

def _get_artifacts():
    if 'scaler' not in _cache:
        _cache['scaler']  = joblib.load(SCALER_PATH)
        _cache['encoder'] = joblib.load(ENCODER_PATH)
    return _cache['scaler'], _cache['encoder']

def _get_model(name):
    if name not in _cache:
        _cache[name] = joblib.load(MODEL_PATHS[name])
    return _cache[name]

def predict_diet(model_name, input_dict):
    scaler, le   = _get_artifacts()
    model        = _get_model(model_name)
    features     = np.array([[float(input_dict[c]) for c in FEATURE_COLUMNS]])
    features_s   = scaler.transform(features)
    predicted_idx = int(model.predict(features_s)[0])
    probs = model.predict_proba(features_s)[0] if hasattr(model,'predict_proba') else None
    if probs is None:
        probs = np.zeros(len(le.classes_)); probs[predicted_idx] = 1.0
    diet       = le.inverse_transform([predicted_idx])[0]
    confidence = round(float(probs[predicted_idx])*100, 2)
    prob_dict  = {le.inverse_transform([i])[0]: round(float(p)*100,2) for i,p in enumerate(probs)}
    return {'diet': diet, 'confidence': confidence, 'probabilities': prob_dict}