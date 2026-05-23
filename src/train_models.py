# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from config import MODEL_PATHS, MODELS_DIR, RANDOM_STATE
from src.preprocessing import get_preprocessed_data

def train_logistic_regression(X_train, y_train, n_classes):
    print('\n[1/5] Training Logistic Regression ...')
    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, solver='lbfgs')
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATHS['logistic_regression'])
    return model