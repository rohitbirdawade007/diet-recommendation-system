# -*- coding: utf-8 -*-
"""config.py - Central configuration for DietAI project."""
import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_PATH  = os.path.join(DATA_DIR, 'diet_recommendation_dataset_1000.csv')

MODEL_PATHS = {
    'logistic_regression': os.path.join(MODELS_DIR, 'logistic_regression.pkl'),
    'decision_tree':       os.path.join(MODELS_DIR, 'decision_tree.pkl'),
    'random_forest':       os.path.join(MODELS_DIR, 'random_forest.pkl'),
    'xgboost':             os.path.join(MODELS_DIR, 'xgboost.pkl'),
    'ann':                 os.path.join(MODELS_DIR, 'ann_model.pkl'),
}

SCALER_PATH  = os.path.join(MODELS_DIR, 'scaler.pkl')
ENCODER_PATH = os.path.join(MODELS_DIR, 'label_encoder.pkl')
METRICS_PATH = os.path.join(MODELS_DIR, 'model_metrics.json')

FEATURE_COLUMNS = ['Age', 'Gender', 'Height_cm', 'Weight_kg', 'BMI',
                   'Activity_Level', 'Sugar_Level', 'Cholesterol', 'Goal']
TARGET_COLUMN = 'Diet'

RANDOM_STATE = 42
TEST_SIZE    = 0.20

# ANN / MLP hyperparameters
ANN_HIDDEN_LAYERS  = (128, 64, 32)
ANN_MAX_ITER       = 300
ANN_EARLY_STOPPING = True
ANN_PATIENCE       = 20

# Diet class mapping (encoded order from LabelEncoder)
DIET_LABELS = {
    0: 'Balanced',
    1: 'Diabetic',
    2: 'Heart Healthy',
    3: 'High Protein',
    4: 'Low Carb',
}

# Flask server defaults
FLASK_HOST  = '0.0.0.0'
FLASK_PORT  = 5000
FLASK_DEBUG = False
