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

def load_data():
    df = pd.read_csv(DATA_PATH)
    print(f'[INFO] Loaded {df.shape[0]} rows x {df.shape[1]} cols')
    return df

def preprocess(df):
    X      = df[FEATURE_COLUMNS].copy().astype(float)
    le     = LabelEncoder()
    y      = le.fit_transform(df[TARGET_COLUMN])
    scaler = StandardScaler()
    X_s    = scaler.fit_transform(X.values)
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(le,     ENCODER_PATH)
    print(f'[INFO] Classes ({len(le.classes_)}): {list(le.classes_)}')
    return X_s, y, scaler, le

def split_data(X, y):
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)

def get_preprocessed_data():
    df = load_data()
    X, y, scaler, le = preprocess(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f'[INFO] Train: {X_train.shape} | Test: {X_test.shape}')
    return X_train, X_test, y_train, y_test, scaler, le