# -*- coding: utf-8 -*-
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