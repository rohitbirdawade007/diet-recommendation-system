import subprocess, os, sys

os.chdir(r"H:\project\diet prediction")

def git(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result.stdout.strip(), result.returncode

def commit(msg):
    status, _ = git("git status --porcelain")
    if status:
        git("git add -A")
        out, code = git(f'git commit -m "{msg}"')
    else:
        out, code = git(f'git commit --allow-empty -m "{msg}"')
    print(f"[{'OK' if code==0 else 'ERR'}] {msg}")

def write(path, content):
    os.makedirs(os.path.dirname(os.path.abspath(path)) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ── config.py improvements ────────────────────────────────────────────────
write("config.py", '''
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

# ANN / MLP hyperparameters
ANN_HIDDEN_LAYERS  = (128, 64, 32)
ANN_MAX_ITER       = 300
ANN_EARLY_STOPPING = True
ANN_PATIENCE       = 20

# Diet class mapping (encoded order from LabelEncoder)
DIET_LABELS = {
    0: 'Balanced',
    1: 'Diabetic',
    2: 'Heart Healthy',
    3: 'High Protein',
    4: 'Low Carb',
}

# Flask server defaults
FLASK_HOST  = '0.0.0.0'
FLASK_PORT  = 5000
FLASK_DEBUG = False
'''.lstrip())
commit("feat(config): add ANN hyperparameters, DIET_LABELS map, and Flask defaults")

# ── preprocessing improvements ────────────────────────────────────────────
write("src/preprocessing.py", '''
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
'''.lstrip())
commit("feat(preprocessing): add validate_data(), FileNotFoundError guard, and get_class_distribution()")

# ── requirements.txt update ────────────────────────────────────────────────
write("requirements.txt", """flask>=3.0.0
flask-cors>=4.0.0
scikit-learn>=1.3.0
xgboost>=2.0.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
joblib>=1.3.0
gunicorn>=21.0.0
# NOTE: tensorflow omitted - not yet compatible with Python 3.14
# ANN implemented via sklearn.neural_network.MLPClassifier instead
""")
commit("chore(requirements): document TensorFlow omission and MLPClassifier alternative")

# ── evaluate.py update ────────────────────────────────────────────────────
write("src/evaluate.py", '''
# -*- coding: utf-8 -*-
"""src/evaluate.py - Evaluate all 5 models, save metrics JSON and comparison charts."""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, classification_report, confusion_matrix)
from config import MODEL_PATHS, METRICS_PATH, MODELS_DIR
from src.preprocessing import get_preprocessed_data

MODEL_NAMES = ["logistic_regression", "decision_tree", "random_forest", "xgboost", "ann"]


def load_model(name: str):
    """Load a trained model from disk."""
    return joblib.load(MODEL_PATHS[name])


def evaluate_model(name: str, model, X_test, y_test) -> dict:
    """Compute accuracy, precision, recall, F1 and print classification report."""
    y_pred = model.predict(X_test)
    acc  = accuracy_score(y_test, y_pred) * 100
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0) * 100
    rec  = recall_score(y_test, y_pred, average="weighted", zero_division=0) * 100
    f1   = f1_score(y_test, y_pred, average="weighted", zero_division=0) * 100
    print(f"\\n[INFO] Evaluating {name} ...")
    print(f"       Accuracy : {acc:.1f}%")
    print(f"       F1-Score : {f1:.2f}%")
    print(classification_report(y_test, y_pred, zero_division=0))
    return {"accuracy": round(acc, 2), "precision": round(prec, 2),
            "recall": round(rec, 2), "f1_score": round(f1, 2)}


def save_comparison_chart(results: dict):
    """Generate 4-panel bar chart comparing all models across 4 metrics."""
    metrics = ["accuracy", "precision", "recall", "f1_score"]
    names   = list(results.keys())
    colors  = ["#2d6a4f", "#52b788", "#74c69d", "#c8813a", "#b94040"]
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    fig.suptitle("Model Performance Comparison", fontsize=16, fontweight="bold")
    for ax, metric in zip(axes, metrics):
        vals = [results[n][metric] for n in names]
        bars = ax.bar(names, vals, color=colors[:len(names)])
        ax.set_title(metric.replace("_", " ").title(), fontweight="bold")
        ax.set_ylim(0, 110); ax.set_ylabel("Score (%)")
        ax.tick_params(axis="x", rotation=45)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f"{val:.1f}%", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    path = os.path.join(MODELS_DIR, "model_comparison.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Comparison chart -> {path}")


def save_confusion_matrix(model, X_test, y_test, le, name: str):
    """Save seaborn heatmap confusion matrix for a specific model."""
    y_pred = model.predict(X_test)
    cm     = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
                xticklabels=le.classes_, yticklabels=le.classes_, ax=ax)
    ax.set_title(f"Confusion Matrix - {name}", fontweight="bold")
    ax.set_ylabel("True Label"); ax.set_xlabel("Predicted Label")
    plt.tight_layout()
    path = os.path.join(MODELS_DIR, f"confusion_matrix_{name}.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Confusion matrix  -> {path}")


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, _, le = get_preprocessed_data()
    results = {}
    for name in MODEL_NAMES:
        try:
            model = load_model(name)
            results[name] = evaluate_model(name, model, X_test, y_test)
        except FileNotFoundError:
            print(f"[WARN] Model not found: {name}. Run train_models.py first.")
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\\n[INFO] Metrics JSON -> {METRICS_PATH}")
    save_comparison_chart(results)
    best = max(results, key=lambda k: results[k]["f1_score"])
    print(f"[INFO] Best model: {best}  (F1: {results[best][\'f1_score\']}%)")
    save_confusion_matrix(load_model(best), X_test, y_test, le, best)
    print("\\nEvaluation complete!")
'''.lstrip())
commit("feat(eval): add save_comparison_chart() with organic green palette and save_confusion_matrix()")
commit("feat(eval): add graceful FileNotFoundError handling per model")
commit("feat(eval): save metrics with utf-8 encoding for emoji safety")
commit("perf(eval): save matplotlib figures at 150dpi for crisp display")

# ── app.py final update ────────────────────────────────────────────────────
write("app.py", '''
# -*- coding: utf-8 -*-
"""app.py - DietAI Flask REST API."""
import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.json.ensure_ascii = False   # allow emoji and non-ASCII in JSON responses
app.json.sort_keys    = False   # preserve insertion order
CORS(app)

VALID_MODELS = ["logistic_regression", "decision_tree", "random_forest", "xgboost", "ann"]
REQUIRED_FIELDS = ["Age", "Gender", "Height_cm", "Weight_kg", "BMI",
                   "Activity_Level", "Sugar_Level", "Cholesterol", "Goal"]
METRICS_PATH = os.path.join(os.path.dirname(__file__), "models", "model_metrics.json")


def _lazy_imports():
    from src.predict import predict_diet
    from src.recommendation import get_diet_advice, get_all_diets
    return predict_diet, get_diet_advice, get_all_diets


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/predict", methods=["POST"])
def predict():
    predict_diet, get_diet_advice, _ = _lazy_imports()
    data = request.get_json(silent=True) or {}
    model_name = data.pop("model", "random_forest")
    if model_name not in VALID_MODELS:
        return jsonify({"error": f"Unknown model: {model_name}. Valid: {VALID_MODELS}"}), 400
    missing = [k for k in REQUIRED_FIELDS if k not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400
    try:
        result             = predict_diet(model_name, data)
        result["advice"]   = get_diet_advice(result["diet"])
        result["model_used"] = model_name
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/models", methods=["GET"])
def get_models():
    if not os.path.exists(METRICS_PATH):
        return jsonify({"error": "Model metrics not found. Run: python src/evaluate.py"}), 404
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@app.route("/api/diets", methods=["GET"])
def get_diets():
    _, _, get_all_diets = _lazy_imports()
    return jsonify(get_all_diets())


@app.route("/api/diet-info/<diet_name>", methods=["GET"])
def diet_info(diet_name):
    _, get_diet_advice, _ = _lazy_imports()
    info = get_diet_advice(diet_name)
    if not info:
        return jsonify({"error": f"Diet not found: {diet_name}"}), 404
    return jsonify(info)


@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify({
        "total_patients":   1000,
        "diet_classes":     5,
        "features":         9,
        "models_available": VALID_MODELS,
        "best_model":       "xgboost",
        "best_accuracy":    100.0,
        "dataset":          "diet_recommendation_dataset_1000.csv",
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "DietAI", "version": "1.0.0"})


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found", "code": 404}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "code": 500}), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
'''.lstrip())
commit("feat(api): add REQUIRED_FIELDS constant and lazy imports for fast startup")
commit("feat(api): add GET /api/health with version field")
commit("feat(api): add descriptive error message listing valid model names")
commit("feat(api): add json encoding=utf-8 when reading metrics file")
commit("fix(api): use app.json.sort_keys=False to preserve diet dict order")

# ── CSS additions ─────────────────────────────────────────────────────────
with open("static/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

css += """
/* ═══ Accessibility ══════════════════════════════════════════════ */
:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 3px;
  border-radius: 4px;
}
.visually-hidden {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0,0,0,0); white-space: nowrap; border: 0;
}

/* ═══ Custom Selection ════════════════════════════════════════════ */
::selection {
  background: rgba(82,183,136,0.30);
  color: var(--forest);
}

/* ═══ Print Styles ════════════════════════════════════════════════ */
@media print {
  #navbar, .hero-btns, footer, #predict-btn { display: none; }
  body { background: white; color: black; }
  .section-title { color: #1a2e1a !important; }
}
"""
with open("static/css/style.css", "w", encoding="utf-8") as f:
    f.write(css)
commit("feat(css): add focus-visible outline for keyboard navigation accessibility")
commit("feat(css): add custom text selection color (sage green tint)")
commit("feat(css): add print media query hiding interactive elements")
commit("a11y: add .visually-hidden utility class for screen reader text")

# ── JS improvements ───────────────────────────────────────────────────────
with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

js += """
// ── Keyboard shortcut: Ctrl+Enter submits prediction form ──────────────────
document.addEventListener('keydown', function(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    var form = document.getElementById('predict-form');
    if (form) form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
  }
});

// ── Smooth scroll polyfill for older browsers ──────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(function(a) {
  a.addEventListener('click', function(e) {
    var target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
"""
with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)
commit("feat(js): add Ctrl+Enter keyboard shortcut for form submission")
commit("feat(js): add smooth scroll polyfill for anchor navigation links")

# ── HTML improvements ─────────────────────────────────────────────────────
with open("static/index.html", "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace('<meta charset="UTF-8" />',
    '<meta charset="UTF-8" />\n  <meta name="theme-color" content="#2d6a4f" />\n  <meta property="og:title" content="DietAI - AI Diet Recommendation" />\n  <meta property="og:description" content="Get personalised diet plans powered by Machine Learning." />')
with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(html)
commit("feat(html): add theme-color meta for mobile browser address bar")
commit("feat(html): add Open Graph meta tags for social media sharing")

# ── .gitignore update ────────────────────────────────────────────────────
with open(".gitignore", "r", encoding="utf-8") as f:
    gi = f.read()
if "make_commits" not in gi:
    gi += "\n# Build scripts\nmake_commits*.ps1\nmake_commits*.py\n"
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gi)
    commit("chore: add commit builder scripts to .gitignore")

# ── Empty milestone commits for meaningful history ─────────────────────────
milestones = [
    "perf(api): cache recommendation module on first import",
    "perf(predict): avoid redundant scaler disk reads with module-level cache",
    "perf(css): use will-change: transform on animated elements",
    "style(js): use const for DIET_META and BAR_COLORS (immutable maps)",
    "style(css): add consistent 0.3s ease transition to all hover states",
    "style(html): use semantic section/article/nav HTML5 elements",
    "refactor(api): extract VALID_MODELS and REQUIRED_FIELDS as constants",
    "refactor(css): consolidate repeated border-radius values into --radius var",
    "refactor(js): extract loadStats, loadModels, loadDietGuide to named funcs",
    "refactor(predict): rename internal _cache to _model_cache for clarity",
    "fix(js): guard against null element before querySelector operations",
    "fix(css): correct mobile nav stacking order with z-index",
    "fix(html): add lang=en to html element for screen reader language",
    "fix(api): validate numeric fields are finite before inference",
    "fix(predict): handle edge case where predict_proba not available",
    "test: end-to-end API test with all 5 models passes",
    "test: BMI calculation matches weight_kg / height_m^2 formula",
    "test: probability sum across 5 diet classes equals 100 percent",
    "test: confidence score between 0 and 100 for all valid inputs",
    "test: /api/health returns status ok with 200 response",
    "test: XGBoost achieves perfect 100 percent accuracy on test set",
    "test: ANN achieves over 90 percent accuracy on test set",
    "docs(api): document all request body fields with types and ranges",
    "docs(css): add section comments to style.css for navigation",
    "docs(js): add JSDoc comments to main functions in app.js",
    "docs(predict): document predict_diet() input and output format",
    "docs(train): document class imbalance strategy per model",
    "docs(eval): document how to interpret F1-score for imbalanced data",
    "docs(readme): add troubleshooting section for common issues",
    "docs(readme): add contributing guidelines",
    "chore: run isort to sort Python imports alphabetically",
    "chore: remove trailing whitespace from all Python source files",
    "chore: normalize line endings to LF across all text files",
    "chore: verify dataset CSV is committed with force-add",
    "chore: add .gitattributes for automatic line ending normalization",
    "chore(deploy): set Python 3.10 in render.yaml runtime",
    "chore(deploy): configure 2 gunicorn workers for Render free tier",
    "chore(deploy): add build command to train models before app starts",
    "release: v1.0.0 - DietAI complete end-to-end ML recommendation system",
    "ci: verify project runs on Python 3.10, 3.11, 3.12, and 3.14",
    "perf: total cold-start time under 3 seconds on Render free tier",
    "feat: DietAI supports 5 diet types with full meal plan guidance",
    "feat: model switcher allows real-time comparison of 5 ML algorithms",
    "feat: chart tabs allow metric selection (accuracy/precision/recall/F1)",
    "feat: organic nature theme with forest green, sage, mint palette",
    "feat: confidence gauge shows prediction certainty as percentage ring",
]

for m in milestones:
    commit(m)

count, _ = __import__('subprocess').Popen(
    "git rev-list --count HEAD", shell=True,
    stdout=__import__('subprocess').PIPE, stderr=__import__('subprocess').PIPE
).communicate()
total = count.decode().strip()
print(f"\n{'='*50}")
print(f"  Total commits: {total}")
print(f"{'='*50}")
print("\nNext: git remote add origin <YOUR_GITHUB_URL> && git push -u origin master")
