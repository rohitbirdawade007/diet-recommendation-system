"""
config.py â€” Central configuration for the Diet Recommendation System
"""
import os

# â”€â”€â”€ Paths â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_PATH   = os.path.join(BASE_DIR, "data", "diet_recommendation_dataset_1000.csv")
MODELS_DIR  = os.path.join(BASE_DIR, "models")

MODEL_PATHS = {
    "logistic_regression": os.path.join(MODELS_DIR, "logistic_regression.pkl"),
    "decision_tree":       os.path.join(MODELS_DIR, "decision_tree.pkl"),
    "random_forest":       os.path.join(MODELS_DIR, "random_forest.pkl"),
    "xgboost":             os.path.join(MODELS_DIR, "xgboost.pkl"),
    "ann":                 os.path.join(MODELS_DIR, "ann_model.pkl"),  # sklearn MLP via joblib
}

SCALER_PATH  = os.path.join(MODELS_DIR, "scaler.pkl")
ENCODER_PATH = os.path.join(MODELS_DIR, "label_encoder.pkl")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")

# â”€â”€â”€ Feature schema â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
FEATURE_COLUMNS = [
    "Age", "Gender", "Height_cm", "Weight_kg", "BMI",
    "Activity_Level", "Sugar_Level", "Cholesterol", "Goal"
]
TARGET_COLUMN = "Diet"

# â”€â”€â”€ Label maps (raw int â†’ human-readable string) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
GENDER_MAP        = {0: "Female",     1: "Male"}
ACTIVITY_MAP      = {0: "Sedentary",  1: "Moderate",    2: "Active"}
GOAL_MAP          = {0: "Weight Loss",1: "Maintenance",  2: "Muscle Gain"}
DIET_LABELS       = ["Balanced", "Diabetic", "Heart Healthy", "High Protein", "Low Carb"]

# â”€â”€â”€ Hyperparameters â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
RANDOM_STATE  = 42
TEST_SIZE     = 0.20

# ANN
ANN_EPOCHS      = 100
ANN_BATCH_SIZE  = 32
ANN_PATIENCE    = 15

