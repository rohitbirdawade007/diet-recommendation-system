# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from config import DATA_PATH, ENCODER_PATH, SCALER_PATH, TARGET_COLUMN, FEATURE_COLUMNS, RANDOM_STATE, TEST_SIZE

def load_data():
    df = pd.read_csv(DATA_PATH)
    print(f'[INFO] Loaded {df.shape[0]} rows x {df.shape[1]} cols')
    return df

def encode_labels(df):
    le = LabelEncoder()
    y  = le.fit_transform(df[TARGET_COLUMN])
    print(f'[INFO] Classes ({len(le.classes_)}): {list(le.classes_)}')
    joblib.dump(le, ENCODER_PATH)
    return y, le

def scale_features(df):
    X      = df[FEATURE_COLUMNS].copy().astype(float)
    scaler = StandardScaler()
    X_s    = scaler.fit_transform(X.values)
    joblib.dump(scaler, SCALER_PATH)
    return X_s, scaler

def split_data(X, y):
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)