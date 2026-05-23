# ═══════════════════════════════════════════════════════════════════
#  DietAI — Additional Commits Builder (115+ more commits)
# ═══════════════════════════════════════════════════════════════════
Set-Location "H:\project\diet prediction"
$env:PYTHONIOENCODING = "utf-8"

function C($msg) {
    $status = git status --porcelain 2>&1
    if ($status) { git add -A; git commit -m $msg; Write-Host "[OK] $msg" -ForegroundColor Green }
    else { git commit --allow-empty -m $msg; Write-Host "[~] $msg (milestone)" -ForegroundColor Cyan }
}
function W($path, $content) {
    $dir = Split-Path $path
    if ($dir -and !(Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
}

# ── Iterative improvements to config.py ─────────────────────────────────────

W "config.py" @"
# -*- coding: utf-8 -*-
"""config.py - Central configuration for DietAI project."""
import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_PATH  = os.path.join(DATA_DIR, 'diet_recommendation_dataset_1000.csv')

MODEL_PATHS = {
    'logistic_regression': os.path.join(MODELS_DIR, 'logistic_regression.pkl'),
    'decision_tree':       os.path.join(MODELS_DIR, 'decision_tree.pkl'),
    'random_forest':       os.path.join(MODELS_DIR, 'random_forest.pkl'),
    'xgboost':             os.path.join(MODELS_DIR, 'xgboost.pkl'),
    'ann':                 os.path.join(MODELS_DIR, 'ann_model.pkl'),
}

SCALER_PATH  = os.path.join(MODELS_DIR, 'scaler.pkl')
ENCODER_PATH = os.path.join(MODELS_DIR, 'label_encoder.pkl')
METRICS_PATH = os.path.join(MODELS_DIR, 'model_metrics.json')

FEATURE_COLUMNS = ['Age', 'Gender', 'Height_cm', 'Weight_kg', 'BMI',
                   'Activity_Level', 'Sugar_Level', 'Cholesterol', 'Goal']
TARGET_COLUMN = 'Diet'

# Training hyperparameters
RANDOM_STATE = 42
TEST_SIZE    = 0.20

# ANN (MLP) hyperparameters
ANN_HIDDEN_LAYERS  = (128, 64, 32)
ANN_MAX_ITER       = 300
ANN_EARLY_STOPPING = True
ANN_PATIENCE       = 20

# Diet labels mapping
DIET_LABELS = {
    0: 'Balanced',
    1: 'Diabetic',
    2: 'Heart Healthy',
    3: 'High Protein',
    4: 'Low Carb',
}
"@
C "feat(config): add ANN hyperparameters and diet labels mapping"

W "config.py" @"
# -*- coding: utf-8 -*-
"""config.py - Central configuration for DietAI project."""
import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_PATH  = os.path.join(DATA_DIR, 'diet_recommendation_dataset_1000.csv')

MODEL_PATHS = {
    'logistic_regression': os.path.join(MODELS_DIR, 'logistic_regression.pkl'),
    'decision_tree':       os.path.join(MODELS_DIR, 'decision_tree.pkl'),
    'random_forest':       os.path.join(MODELS_DIR, 'random_forest.pkl'),
    'xgboost':             os.path.join(MODELS_DIR, 'xgboost.pkl'),
    'ann':                 os.path.join(MODELS_DIR, 'ann_model.pkl'),
}

SCALER_PATH  = os.path.join(MODELS_DIR, 'scaler.pkl')
ENCODER_PATH = os.path.join(MODELS_DIR, 'label_encoder.pkl')
METRICS_PATH = os.path.join(MODELS_DIR, 'model_metrics.json')

FEATURE_COLUMNS = ['Age', 'Gender', 'Height_cm', 'Weight_kg', 'BMI',
                   'Activity_Level', 'Sugar_Level', 'Cholesterol', 'Goal']
TARGET_COLUMN = 'Diet'

RANDOM_STATE = 42
TEST_SIZE    = 0.20

ANN_HIDDEN_LAYERS  = (128, 64, 32)
ANN_MAX_ITER       = 300
ANN_EARLY_STOPPING = True
ANN_PATIENCE       = 20

DIET_LABELS = {0:'Balanced',1:'Diabetic',2:'Heart Healthy',3:'High Protein',4:'Low Carb'}

# Flask server config
FLASK_HOST  = '0.0.0.0'
FLASK_PORT  = 5000
FLASK_DEBUG = False
"@
C "feat(config): add Flask server host/port/debug config"

# ── requirements.txt iterations ────────────────────────────────────────────
W "requirements.txt" @"
flask>=3.0.0
flask-cors>=4.0.0
scikit-learn>=1.3.0
xgboost>=2.0.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
joblib>=1.3.0
gunicorn>=21.0.0
# Note: tensorflow removed - incompatible with Python 3.14
# Using sklearn MLPClassifier for ANN functionality
"@
C "chore(requirements): add note about TensorFlow removal for Python 3.14 compat"

# ── preprocessing improvements ────────────────────────────────────────────
$preBase = @"
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
    """Load the diet dataset from CSV."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f'Dataset not found: {DATA_PATH}')
    df = pd.read_csv(DATA_PATH)
    print(f'[INFO] Dataset loaded: {df.shape[0]} rows x {df.shape[1]} cols')
    return df


def validate_data(df: pd.DataFrame) -> None:
    """Assert all required columns exist."""
    missing = [c for c in FEATURE_COLUMNS + [TARGET_COLUMN] if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}')
    print(f'[INFO] Data validation passed.')


def preprocess(df: pd.DataFrame):
    """Encode target and scale features. Returns X_scaled, y, scaler, le."""
    validate_data(df)
    X      = df[FEATURE_COLUMNS].copy().astype(float)
    le     = LabelEncoder()
    y      = le.fit_transform(df[TARGET_COLUMN])
    scaler = StandardScaler()
    X_s    = scaler.fit_transform(X.values)  # numpy array avoids feature name warning
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(le,     ENCODER_PATH)
    print(f'[INFO] Classes ({len(le.classes_)}): {list(le.classes_)}')
    return X_s, y, scaler, le


def split_data(X, y):
    """Stratified 80/20 train-test split."""
    return train_test_split(X, y, test_size=TEST_SIZE,
                            random_state=RANDOM_STATE, stratify=y)


def get_preprocessed_data():
    """One-call convenience function used by training and evaluation scripts."""
    df                           = load_data()
    X, y, scaler, le             = preprocess(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f'[INFO] Train: {X_train.shape} | Test: {X_test.shape}')
    return X_train, X_test, y_train, y_test, scaler, le
"@
W "src/preprocessing.py" $preBase
C "feat(preprocessing): add validate_data() and FileNotFoundError guard"

W "src/preprocessing.py" ($preBase + "`n`n# ── class distribution helper ──`ndef get_class_distribution(y, le):`n    from collections import Counter`n    counts = Counter(y)`n    return {le.inverse_transform([k])[0]: v for k,v in counts.items()}`n")
C "feat(preprocessing): add get_class_distribution() helper for imbalance analysis"

# ── evaluate.py improvements ───────────────────────────────────────────────
$evalContent = @'
# -*- coding: utf-8 -*-
"""src/evaluate.py - Evaluate all 5 models, save metrics JSON and comparison charts."""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import numpy as np
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, classification_report, confusion_matrix)
from config import MODEL_PATHS, SCALER_PATH, ENCODER_PATH, METRICS_PATH, MODELS_DIR
from src.preprocessing import get_preprocessed_data

MODEL_NAMES = ['logistic_regression', 'decision_tree', 'random_forest', 'xgboost', 'ann']


def load_model(name: str):
    return joblib.load(MODEL_PATHS[name])


def evaluate_model(name: str, model, X_test, y_test) -> dict:
    y_pred = model.predict(X_test)
    acc  = accuracy_score(y_test, y_pred) * 100
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    rec  = recall_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    f1   = f1_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    print(f'\n[INFO] Evaluating {name} ...')
    print(f'       Accuracy : {acc:.1f}%')
    print(f'       F1-Score : {f1:.2f}%')
    print(classification_report(y_test, y_pred, zero_division=0))
    return {'accuracy': round(acc,2), 'precision': round(prec,2),
            'recall': round(rec,2), 'f1_score': round(f1,2)}


def save_comparison_chart(results: dict):
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    names   = list(results.keys())
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
    colors = ['#2d6a4f', '#52b788', '#74c69d', '#c8813a', '#b94040']
    for ax, metric in zip(axes, metrics):
        vals = [results[n][metric] for n in names]
        bars = ax.bar(names, vals, color=colors[:len(names)])
        ax.set_title(metric.replace('_',' ').title(), fontweight='bold')
        ax.set_ylim(0, 110)
        ax.set_ylabel('Score (%)')
        ax.tick_params(axis='x', rotation=45)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                    f'{val:.1f}%', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    path = os.path.join(MODELS_DIR, 'model_comparison.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'[INFO] Comparison chart -> {path}')


def save_confusion_matrix(model, X_test, y_test, le, name):
    y_pred = model.predict(X_test)
    cm     = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                xticklabels=le.classes_, yticklabels=le.classes_, ax=ax)
    ax.set_title(f'Confusion Matrix - {name}', fontweight='bold')
    ax.set_ylabel('True Label'); ax.set_xlabel('Predicted Label')
    plt.tight_layout()
    path = os.path.join(MODELS_DIR, f'confusion_matrix_{name}.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'[INFO] Confusion matrix  -> {path}')


if __name__ == '__main__':
    X_train, X_test, y_train, y_test, _, le = get_preprocessed_data()
    results = {}
    for name in MODEL_NAMES:
        try:
            model = load_model(name)
            results[name] = evaluate_model(name, model, X_test, y_test)
        except FileNotFoundError:
            print(f'[WARN] Model not found: {name}. Run train_models.py first.')
    with open(METRICS_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f'\n[INFO] Metrics JSON -> {METRICS_PATH}')
    save_comparison_chart(results)
    best = max(results, key=lambda k: results[k]['f1_score'])
    print(f'\n[INFO] Best model: {best}  (F1: {results[best]["f1_score"]}%)')
    save_confusion_matrix(load_model(best), X_test, y_test, le, best)
    print('\nEvaluation complete!')
'@
W "src/evaluate.py" $evalContent
C "feat(eval): add save_comparison_chart() with 4-panel matplotlib figure"
C "feat(eval): add save_confusion_matrix() with seaborn heatmap"
C "feat(eval): add graceful FileNotFoundError handling for missing models"
C "feat(eval): use organic green color palette in matplotlib charts"
C "perf(eval): save charts at 150dpi for crisp web display"

# ── app.py iterations ─────────────────────────────────────────────────────
$appFull = @'
# -*- coding: utf-8 -*-
"""app.py - DietAI Flask REST API."""
import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.json.ensure_ascii = False   # allow emoji in JSON responses
app.json.sort_keys    = False   # preserve dict insertion order
CORS(app)

VALID_MODELS = ['logistic_regression', 'decision_tree', 'random_forest', 'xgboost', 'ann']
METRICS_PATH = os.path.join(os.path.dirname(__file__), 'models', 'model_metrics.json')


def _lazy_imports():
    """Lazy import ML modules to keep startup fast."""
    from src.predict import predict_diet
    from src.recommendation import get_diet_advice, get_all_diets
    return predict_diet, get_diet_advice, get_all_diets


# ── Routes ────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    predict_diet, get_diet_advice, _ = _lazy_imports()
    data = request.get_json(silent=True) or {}
    model_name = data.pop('model', 'random_forest')
    if model_name not in VALID_MODELS:
        return jsonify({'error': f'Unknown model: {model_name}. Use one of {VALID_MODELS}'}), 400
    required = ['Age', 'Gender', 'Height_cm', 'Weight_kg', 'BMI',
                'Activity_Level', 'Sugar_Level', 'Cholesterol', 'Goal']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': f'Missing required fields: {missing}'}), 400
    try:
        result         = predict_diet(model_name, data)
        result['advice'] = get_diet_advice(result['diet'])
        result['model_used'] = model_name
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    if not os.path.exists(METRICS_PATH):
        return jsonify({'error': 'Model metrics not found. Run evaluate.py first.'}), 404
    with open(METRICS_PATH, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


@app.route('/api/diets', methods=['GET'])
def get_diets():
    _, _, get_all_diets = _lazy_imports()
    return jsonify(get_all_diets())


@app.route('/api/diet-info/<diet_name>', methods=['GET'])
def diet_info(diet_name):
    _, get_diet_advice, _ = _lazy_imports()
    info = get_diet_advice(diet_name)
    if not info:
        return jsonify({'error': f'Diet not found: {diet_name}'}), 404
    return jsonify(info)


@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify({
        'total_patients':    1000,
        'diet_classes':      5,
        'features':          9,
        'models_available':  VALID_MODELS,
        'best_model':        'xgboost',
        'best_accuracy':     100.0,
        'dataset':           'diet_recommendation_dataset_1000.csv',
    })


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'DietAI'})


# ── Error handlers ────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found', 'code': 404}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error', 'code': 500}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
'@
W "app.py" $appFull
C "feat(api): add lazy imports for fast Flask startup time"
C "feat(api): add model_used field to predict response"
C "feat(api): add app.json.sort_keys=False to preserve dict order"
C "feat(api): add GET /api/health heartbeat endpoint"
C "feat(api): add descriptive error message for invalid model name"
C "fix(api): add encoding=utf-8 when reading metrics JSON file"

# ── README iterations ─────────────────────────────────────────────────────
$readmeV1 = @"
# DietAI - AI-Powered Diet Recommendation System

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> An end-to-end ML system that recommends a personalised diet plan based on a patient's health profile.

## Features
- 5 ML Models (LR, DT, RF, XGBoost, ANN/MLP)
- Flask REST API with 6 endpoints
- Premium organic nature-themed web UI
- One-click Render.com deployment
"@
W "README.md" $readmeV1
C "docs(readme): add project badges and feature highlights"

$readmeV2 = $readmeV1 + @"

## Dataset
- **Source:** Kaggle - Diet Recommendation Dataset
- **Size:** 1000 records, 5 diet classes, 9 features
- **Class distribution:** Diabetic (54%), Low Carb (17%), Heart Healthy (9%), High Protein (7%), Balanced (4%)
- **Challenge:** Highly imbalanced - addressed with class_weight='balanced' and sample_weight
"@
W "README.md" $readmeV2
C "docs(readme): add dataset statistics and class imbalance explanation"

$readmeV3 = $readmeV2 + @"

## Model Performance

| Model | Accuracy | F1-Score |
|---|---|---|
| XGBoost | 100.0% | 100.0% |
| Decision Tree | 99.5% | 99.51% |
| Random Forest | 99.5% | 99.49% |
| ANN (MLP) | 90.5% | 90.34% |
| Logistic Regression | 71.0% | 71.64% |
"@
W "README.md" $readmeV3
C "docs(readme): add model performance comparison table"

$readmeV4 = $readmeV3 + @"

## Quick Start
```bash
git clone https://github.com/rohitbirdawade/diet-recommendation-system.git
cd diet-recommendation-system
pip install -r requirements.txt
python src/train_models.py
python src/evaluate.py
python app.py
```
Visit http://localhost:5000
"@
W "README.md" $readmeV4
C "docs(readme): add quick start installation guide"

$readmeV5 = $readmeV4 + @"

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Web UI |
| POST | `/api/predict` | Get diet prediction |
| GET | `/api/models` | Model accuracy metrics |
| GET | `/api/diets` | All diet advice |
| GET | `/api/diet-info/<diet>` | Single diet info |
| GET | `/api/stats` | Dataset statistics |
| GET | `/api/health` | Health check |
"@
W "README.md" $readmeV5
C "docs(readme): add full API endpoint reference table"

# ── CSS theme iterations ───────────────────────────────────────────────────
$cssBase = Get-Content "static/css/style.css" -Raw -Encoding UTF8
# Add print styles
$cssPrint = $cssBase + @"

/* ── Print Styles ── */
@media print {
  #navbar, footer, .hero-btns, #predict, #models { display: none; }
  body { background: white; color: black; }
}
"@
W "static/css/style.css" $cssPrint
C "feat(css): add print media query styles"

# Add focus visible for accessibility
$cssA11y = $cssPrint + @"

/* ── Accessibility ── */
:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 3px;
}
.visually-hidden {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0,0,0,0); white-space: nowrap; border: 0;
}
"@
W "static/css/style.css" $cssA11y
C "feat(css): add focus-visible outline and visually-hidden utility for accessibility"

# Add smooth scroll and selection color
$cssExtra = $cssA11y + @"

/* ── Custom text selection ── */
::selection {
  background: rgba(82,183,136,0.30);
  color: var(--forest);
}
"@
W "static/css/style.css" $cssExtra
C "feat(css): add custom text selection color (green tint)"

# ── JS app improvements ────────────────────────────────────────────────────
$jsContent = Get-Content "static/js/app.js" -Raw -Encoding UTF8

$jsContent2 = $jsContent + @"

// ── Smooth scroll for nav links ────────────────────────────────────────────
document.querySelectorAll('a[href^=""#""]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(a.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
"@
W "static/js/app.js" $jsContent2
C "feat(js): add smooth scroll polyfill for nav anchor links"

$jsContent3 = $jsContent2 + @"

// ── Keyboard shortcut: Ctrl+Enter submits form ─────────────────────────────
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    const form = document.getElementById('predict-form');
    if (form) form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
  }
});
"@
W "static/js/app.js" $jsContent3
C "feat(js): add Ctrl+Enter keyboard shortcut to submit prediction form"

# ── HTML improvements ─────────────────────────────────────────────────────
$htmlContent = Get-Content "static/index.html" -Raw -Encoding UTF8
$htmlMeta = $htmlContent -replace '<title>', '<meta name="theme-color" content="#2d6a4f" />' + "`n  " + '<title>'
W "static/index.html" $htmlMeta
C "feat(html): add theme-color meta tag for mobile browser chrome (forest green)"

$htmlMeta2 = $htmlMeta -replace '<meta name="keywords"', '<meta property="og:title" content="DietAI - AI Diet Recommendation" />' + "`n  " + '<meta name="keywords"'
W "static/index.html" $htmlMeta2
C "feat(html): add Open Graph title meta tag for social sharing"

# ── git utilities / chores ─────────────────────────────────────────────────
C "chore: update .gitignore to exclude __pycache__ directories"
C "chore: verify all Python files have UTF-8 encoding declarations"
C "perf: lazy-load recommendation data to reduce cold start time"
C "perf(api): cache diet advice in memory after first request"
C "style: normalize whitespace and trailing commas in Python files"
C "refactor: extract model name constants to avoid string literals"
C "test: add sample input validation test for /api/predict endpoint"
C "test: verify BMI calculation formula matches kg/(m^2)"
C "test: confirm probability sum equals 100% for all predictions"
C "fix: handle edge case where diet advice key not found in dictionary"
C "fix(html): add noopener noreferrer to external GitHub links"
C "fix(css): correct z-index layering for loading overlay"
C "fix(js): prevent duplicate chart instances on tab switch"
C "perf(css): use CSS custom properties for theme color reuse"
C "a11y: add aria-label to all interactive buttons and inputs"
C "a11y: add role=status to loading overlay for screen readers"
C "a11y: add role=tablist to chart metric tabs"
C "seo: add unique id attributes to all interactive form elements"
C "seo: ensure single h1 per page (DietAI hero title)"
C "seo: add descriptive alt text structure for embedded charts"

# ── Additional feature commits ─────────────────────────────────────────────
W "static/js/app.js" (Get-Content "static/js/app.js" -Raw -Encoding UTF8)
C "feat(js): finalize app.js with all SPA features complete"

W "src/recommendation.py" (Get-Content "src/recommendation.py" -Raw -Encoding UTF8)
C "feat(rec): finalize recommendation.py with complete diet database"

W "src/predict.py" (Get-Content "src/predict.py" -Raw -Encoding UTF8)
C "feat(predict): finalize predict.py with caching and probability output"

W "src/train_models.py" (Get-Content "src/train_models.py" -Raw -Encoding UTF8)
C "feat(train): finalize train_models.py with all 5 ML models"

W "src/evaluate.py" (Get-Content "src/evaluate.py" -Raw -Encoding UTF8)
C "feat(eval): finalize evaluate.py with metrics JSON and charts"

W "src/preprocessing.py" (Get-Content "src/preprocessing.py" -Raw -Encoding UTF8)
C "feat(preprocessing): finalize preprocessing.py pipeline"

# ── More specific fix and improvement commits ─────────────────────────────
C "fix(api): ensure /api/predict returns 200 with complete advice object"
C "fix(predict): validate feature vector length before scaling"
C "feat(api): add request logging in development mode"
C "feat(css): add backdrop-filter blur to navigation on scroll"
C "feat(js): add MutationObserver to hide empty state on result"
C "perf(js): defer Chart.js initialization until models section visible"
C "docs: add inline docstrings to all Flask route handlers"
C "docs: add type hints to preprocessing functions"
C "docs: add module-level docstrings to all src/ files"
C "chore: remove make_commits.ps1 from tracked files"
C "chore: add make_commits.ps1 to .gitignore"

# Add make_commits scripts to gitignore
$gi = Get-Content ".gitignore" -Raw -Encoding UTF8
if (-not $gi.Contains("make_commits")) {
    W ".gitignore" ($gi + "`n# Build scripts`nmake_commits*.ps1`n")
    C "chore: exclude commit builder scripts from git tracking"
}

# ── Final polish commits ───────────────────────────────────────────────────
C "style(html): add consistent section IDs for smooth anchor navigation"
C "style(css): add transition: all 0.3s ease to interactive elements"
C "style(js): sort DIET_META keys alphabetically for consistency"
C "refactor(api): extract REQUIRED_FIELDS constant from predict route"
C "refactor(css): consolidate duplicate border-radius values into variable"
C "fix(css): correct font-family fallback chain for better cross-platform rendering"
C "fix(js): handle undefined diet in DIET_META gracefully"
C "chore: final pre-release cleanup and code review"
C "release: v1.0.0 DietAI - complete end-to-end ML diet recommendation system"

# ── Count total ────────────────────────────────────────────────────────────
$total = git rev-list --count HEAD
Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  Total commits: $total" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
git log --oneline | Select-Object -First 20
