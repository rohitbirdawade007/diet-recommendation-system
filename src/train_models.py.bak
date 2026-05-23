# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier
from config import MODEL_PATHS, MODELS_DIR, RANDOM_STATE
from src.preprocessing import get_preprocessed_data

def train_logistic_regression(X_train, y_train, n_classes):
    print('\n[1/5] Training Logistic Regression ...')
    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE,
                               class_weight='balanced', solver='lbfgs')
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATHS['logistic_regression'])
    print(f'      Saved -> {MODEL_PATHS[\"logistic_regression\"]}'); return model

def train_decision_tree(X_train, y_train):
    print('\n[2/5] Training Decision Tree ...')
    model = DecisionTreeClassifier(max_depth=8, random_state=RANDOM_STATE, class_weight='balanced')
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATHS['decision_tree'])
    print(f'      Saved -> {MODEL_PATHS[\"decision_tree\"]}'); return model

def train_random_forest(X_train, y_train):
    print('\n[3/5] Training Random Forest ...')
    model = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=RANDOM_STATE,
                                   class_weight='balanced', n_jobs=-1)
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATHS['random_forest'])
    print(f'      Saved -> {MODEL_PATHS[\"random_forest\"]}'); return model

def train_xgboost(X_train, y_train, n_classes):
    print('\n[4/5] Training XGBoost ...')
    sw    = compute_sample_weight('balanced', y_train)
    model = XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1,
                          random_state=RANDOM_STATE, eval_metric='mlogloss',
                          objective='multi:softprob', num_class=n_classes, verbosity=0)
    model.fit(X_train, y_train, sample_weight=sw)
    joblib.dump(model, MODEL_PATHS['xgboost'])
    print(f'      Saved -> {MODEL_PATHS[\"xgboost\"]}'); return model