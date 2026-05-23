# -*- coding: utf-8 -*-
"""src/preprocessing.py - Data loading, encoding, scaling and splitting."""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from config import (DATA_PATH, ENCODER_PATH, SCALER_PATH, MODELS_DIR,
                    TARGET_COLUMN, FEATURE_COLUMNS, RANDOM_STATE, TEST_SIZE)


def load_data() -> pd.DataFrame:
    """Load the diet dataset from CSV file."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"[INFO] Dataset loaded: {df.shape[0]} rows x {df.shape[1]} cols")
    return df


def validate_data(df: pd.DataFrame) -> None:
    """Assert required feature and target columns are present."""
    expected = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing  = [c for c in expected if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    print(f"[INFO] Data validation passed.")


def preprocess(df: pd.DataFrame):
    """Encode target labels and scale features with StandardScaler."""
    validate_data(df)
    X      = df[FEATURE_COLUMNS].copy().astype(float)
    le     = LabelEncoder()
    y      = le.fit_transform(df[TARGET_COLUMN])
    scaler = StandardScaler()
    X_s    = scaler.fit_transform(X.values)   # fit on numpy -> no feature name warning
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(le, ENCODER_PATH)
    print(f"[INFO] Classes ({len(le.classes_)}): {list(le.classes_)}")
    print(f"[INFO] Scaler  -> {SCALER_PATH}")
    print(f"[INFO] Encoder -> {ENCODER_PATH}")
    return X_s, y, scaler, le


def split_data(X, y):
    """Stratified 80/20 train-test split preserving class proportions."""
    return train_test_split(X, y, test_size=TEST_SIZE,
                            random_state=RANDOM_STATE, stratify=y)


def get_class_distribution(y, le):
    """Return {diet_label: count} for class imbalance analysis."""
    from collections import Counter
    counts = Counter(y)
    return {le.inverse_transform([k])[0]: v for k, v in sorted(counts.items())}


def get_preprocessed_data():
    """One-call pipeline: load -> validate -> preprocess -> split."""
    df                               = load_data()
    X, y, scaler, le                 = preprocess(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"[INFO] Train: {X_train.shape} | Test: {X_test.shape}")
    return X_train, X_test, y_train, y_test, scaler, le
