# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json, joblib, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, classification_report)
from config import MODEL_PATHS, METRICS_PATH, MODELS_DIR
from src.preprocessing import get_preprocessed_data

def load_model(name): return joblib.load(MODEL_PATHS[name])

def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    acc  = accuracy_score(y_test, y_pred) * 100
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    rec  = recall_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    f1   = f1_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    print(f'[INFO] Evaluating {name} ...')
    print(f'       Accuracy : {acc:.1f}%')
    print(f'       F1-Score : {f1:.2f}%')
    print(classification_report(y_test, y_pred, zero_division=0))
    return {'accuracy': round(acc,2), 'precision': round(prec,2),
            'recall': round(rec,2), 'f1_score': round(f1,2)}

if __name__ == '__main__':
    MODEL_NAMES = ['logistic_regression','decision_tree','random_forest','xgboost','ann']
    X_train, X_test, y_train, y_test, _, _ = get_preprocessed_data()
    results = {}
    for name in MODEL_NAMES:
        m = load_model(name)
        results[name] = evaluate_model(name, m, X_test, y_test)
    with open(METRICS_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'[INFO] Metrics saved -> {METRICS_PATH}')
    best = max(results, key=lambda k: results[k]['f1_score'])
    print(f'[INFO] Best model: {best} (F1: {results[best][\"f1_score\"]}%)')