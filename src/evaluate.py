# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import joblib
from sklearn.metrics import accuracy_score
from config import MODEL_PATHS
from src.preprocessing import get_preprocessed_data

def load_model(name):
    return joblib.load(MODEL_PATHS[name])

def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    acc    = accuracy_score(y_test, y_pred)
    print(f'[INFO] {name}: Accuracy = {acc*100:.1f}%')
    return {'accuracy': round(acc*100, 2)}