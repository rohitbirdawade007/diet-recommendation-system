"""
src/preprocessing.py â€” Data loading, encoding, scaling and splitting
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

from config import (
    DATA_PATH, SCALER_PATH, ENCODER_PATH,
    FEATURE_COLUMNS, TARGET_COLUMN,
    RANDOM_STATE, TEST_SIZE
)


def load_data() -> pd.DataFrame:
    """Load the diet dataset from CSV."""
    df = pd.read_csv(DATA_PATH)
    print(f"[INFO] Dataset loaded: {df.shape[0]} rows Ã-- {df.shape[1]} cols")
    return df


def preprocess(df: pd.DataFrame):
    """
    Encode target label and scale features.

    Returns
    -------
    X_scaled : np.ndarray  (n_samples, n_features)
    y_encoded: np.ndarray  (n_samples,)
    scaler   : fitted StandardScaler
    le       : fitted LabelEncoder
    """
    X = df[FEATURE_COLUMNS].copy().astype(float)
    y = df[TARGET_COLUMN].copy()

    # Encode target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Scale features (fit on numpy array so no feature-name mismatch at inference)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.values)

    # Persist artifacts
    os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(le, ENCODER_PATH)

    print(f"[INFO] Classes ({len(le.classes_)}): {list(le.classes_)}")
    print(f"[INFO] Scaler  â†’ {SCALER_PATH}")
    print(f"[INFO] Encoder â†’ {ENCODER_PATH}")
    return X_scaled, y_encoded, scaler, le


def split_data(X, y):
    """Stratified 80/20 train-test split."""
    return train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )


def get_preprocessed_data():
    """One-call helper used by train_models and evaluate."""
    df = load_data()
    X, y, scaler, le = preprocess(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"[INFO] Train: {X_train.shape} | Test: {X_test.shape}")
    return X_train, X_test, y_train, y_test, scaler, le

