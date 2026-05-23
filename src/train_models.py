# -*- coding: utf-8 -*-
"""src/train_models.py - Train all 5 ML classifiers and persist as .pkl artifacts."""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier
from config import MODEL_PATHS, MODELS_DIR, RANDOM_STATE, ANN_HIDDEN_LAYERS, ANN_MAX_ITER
from src.preprocessing import get_preprocessed_data


def train_logistic_regression(X_train, y_train, n_classes):
    """Logistic Regression - baseline linear classifier with balanced class weight."""
    print("\n[1/5] Training Logistic Regression ...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE,
        class_weight="balanced",   # compensate for Diabetic class dominance (54%)
        solver="lbfgs",
    )
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATHS["logistic_regression"])
    print(f"      Saved -> {MODEL_PATHS['logistic_regression']}")
    return model


def train_decision_tree(X_train, y_train):
    """Decision Tree - interpretable non-linear classifier, max_depth=8."""
    print("\n[2/5] Training Decision Tree ...")
    model = DecisionTreeClassifier(
        max_depth=8,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATHS["decision_tree"])
    print(f"      Saved -> {MODEL_PATHS['decision_tree']}")
    return model


def train_random_forest(X_train, y_train):
    """Random Forest - 200 trees with balanced class weight, parallel training."""
    print("\n[3/5] Training Random Forest ...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=RANDOM_STATE,
        class_weight="balanced",
        n_jobs=-1,                  # use all CPU cores
    )
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATHS["random_forest"])
    print(f"      Saved -> {MODEL_PATHS['random_forest']}")
    return model


def train_xgboost(X_train, y_train, n_classes):
    """XGBoost - gradient boosting with sample_weight for imbalance. Best model (100% acc)."""
    print("\n[4/5] Training XGBoost ...")
    sample_weight = compute_sample_weight("balanced", y_train)
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=RANDOM_STATE,
        eval_metric="mlogloss",
        objective="multi:softprob",
        num_class=n_classes,
        verbosity=0,
    )
    model.fit(X_train, y_train, sample_weight=sample_weight)
    joblib.dump(model, MODEL_PATHS["xgboost"])
    print(f"      Saved -> {MODEL_PATHS['xgboost']}")
    return model


def train_ann(X_train, y_train):
    """ANN (MLP) - 3-layer neural network via sklearn. Python 3.14 compatible."""
    print("\n[5/5] Training ANN (MLP Neural Network) ...")
    model = MLPClassifier(
        hidden_layer_sizes=ANN_HIDDEN_LAYERS,   # (128, 64, 32)
        activation="relu",
        solver="adam",
        alpha=1e-4,                             # L2 regularization
        batch_size=32,
        learning_rate_init=1e-3,
        max_iter=ANN_MAX_ITER,                  # 300
        early_stopping=True,
        validation_fraction=0.15,
        n_iter_no_change=20,                    # patience
        random_state=RANDOM_STATE,
        verbose=False,
    )
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATHS["ann"])
    print(f"      Saved -> {MODEL_PATHS['ann']}")
    return model


if __name__ == "__main__":
    os.makedirs(MODELS_DIR, exist_ok=True)
    X_train, X_test, y_train, y_test, scaler, le = get_preprocessed_data()
    n_classes = len(le.classes_)
    print(f"\n[INFO] n_classes = {n_classes}  |  classes = {list(le.classes_)}")

    train_logistic_regression(X_train, y_train, n_classes)
    train_decision_tree(X_train, y_train)
    train_random_forest(X_train, y_train)
    train_xgboost(X_train, y_train, n_classes)
    train_ann(X_train, y_train)

    print("\nAll 5 models trained and saved successfully!")
