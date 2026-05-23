# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from config import DATA_PATH, ENCODER_PATH, TARGET_COLUMN, FEATURE_COLUMNS
import joblib

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