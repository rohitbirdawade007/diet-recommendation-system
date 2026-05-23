# -*- coding: utf-8 -*-
"""src/train_models.py - Train all 5 ML models."""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import joblib
from config import MODEL_PATHS, MODELS_DIR, RANDOM_STATE
from src.preprocessing import get_preprocessed_data