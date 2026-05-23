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
    print(f"\n[INFO] Evaluating {name} ...")
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
    print(f"\n[INFO] Metrics JSON -> {METRICS_PATH}")
    save_comparison_chart(results)
    best = max(results, key=lambda k: results[k]["f1_score"])
    print(f"[INFO] Best model: {best}  (F1: {results[best]['f1_score']}%)")
    save_confusion_matrix(load_model(best), X_test, y_test, le, best)
    print("\nEvaluation complete!")
