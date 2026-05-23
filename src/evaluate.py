"""
src/evaluate.py â€” Evaluate all 5 models, save metrics JSON and comparison charts
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix
)

from config import MODEL_PATHS, SCALER_PATH, ENCODER_PATH, METRICS_PATH, MODELS_DIR
from src.preprocessing import get_preprocessed_data


# â”€â”€â”€ Loaders â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def load_model(name: str):
    # All models (including ANN/MLP) are now stored via joblib
    return joblib.load(MODEL_PATHS[name])


# â”€â”€â”€ Evaluation â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def evaluate_model(name: str, model, X_test, y_test) -> dict:
    # All models use the same sklearn predict interface
    y_pred = model.predict(X_test)

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec  = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1   = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    return {
        "accuracy":  round(acc  * 100, 2),
        "precision": round(prec * 100, 2),
        "recall":    round(rec  * 100, 2),
        "f1_score":  round(f1   * 100, 2),
        "y_pred":    y_pred.tolist(),
    }


# â”€â”€â”€ Plotting â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
DISPLAY_NAMES = {
    "logistic_regression": "Logistic\nRegression",
    "decision_tree":       "Decision\nTree",
    "random_forest":       "Random\nForest",
    "xgboost":             "XGBoost",
    "ann":                 "ANN",
}
COLORS = ["#7c3aed", "#06b6d4", "#10b981", "#f59e0b", "#ef4444"]


def plot_comparison(all_metrics: dict):
    names   = list(all_metrics.keys())
    metrics = ["accuracy", "precision", "recall", "f1_score"]
    labels  = ["Accuracy", "Precision", "Recall", "F1-Score"]

    fig, axes = plt.subplots(1, 4, figsize=(22, 6))
    fig.patch.set_facecolor("#0f0f1e")
    fig.suptitle("Model Performance Comparison", color="white",
                 fontsize=16, fontweight="bold", y=1.02)

    for idx, (metric, label) in enumerate(zip(metrics, labels)):
        ax = axes[idx]
        ax.set_facecolor("#1a1a2e")
        values = [all_metrics[m][metric] for m in names]
        bars   = ax.bar(
            [DISPLAY_NAMES[n] for n in names], values,
            color=COLORS, alpha=0.85, width=0.55
        )
        ax.set_title(label, color="white", fontsize=13, fontweight="bold", pad=10)
        ax.set_ylabel("Score (%)", color="#94a3b8", fontsize=10)
        ax.set_ylim(0, 112)
        ax.tick_params(colors="#94a3b8", labelsize=9)
        ax.spines[:].set_color("#334155")
        ax.grid(axis="y", color="#1e293b", linewidth=0.5)
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1.5,
                f"{val:.1f}%",
                ha="center", va="bottom",
                color="white", fontsize=9, fontweight="bold"
            )

    plt.tight_layout()
    out_path = os.path.join(MODELS_DIR, "model_comparison.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="#0f0f1e")
    plt.close()
    print(f"[INFO] Comparison chart â†’ {out_path}")


def plot_confusion_matrix(y_test, y_pred, le, model_name: str):
    cm  = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#0f0f1e")
    ax.set_facecolor("#1a1a2e")

    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Purples",
        xticklabels=le.classes_, yticklabels=le.classes_, ax=ax,
        linewidths=0.5, linecolor="#334155"
    )
    ax.set_title(f"Confusion Matrix â€” {model_name.replace('_', ' ').title()}",
                 color="white", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Predicted", color="#94a3b8", fontsize=11)
    ax.set_ylabel("Actual",    color="#94a3b8", fontsize=11)
    ax.tick_params(colors="#94a3b8")
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", color="white")
    plt.setp(ax.get_yticklabels(), rotation=0, color="white")

    plt.tight_layout()
    out_path = os.path.join(MODELS_DIR, f"confusion_matrix_{model_name}.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="#0f0f1e")
    plt.close()
    print(f"[INFO] Confusion matrix  â†’ {out_path}")


# â”€â”€â”€ Main â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler, le = get_preprocessed_data()

    model_names  = ["logistic_regression", "decision_tree", "random_forest", "xgboost", "ann"]
    all_metrics  = {}

    for name in model_names:
        print(f"\n[INFO] Evaluating {name} ...")
        model   = load_model(name)
        metrics = evaluate_model(name, model, X_test, y_test)
        all_metrics[name] = metrics
        print(f"       Accuracy : {metrics['accuracy']}%")
        print(f"       F1-Score : {metrics['f1_score']}%")
        report = classification_report(
            y_test, metrics["y_pred"],
            target_names=le.classes_, zero_division=0
        )
        print(report)

    # Save metrics (strip non-serialisable y_pred)
    saveable = {k: {m: v for m, v in d.items() if m != "y_pred"}
                for k, d in all_metrics.items()}
    with open(METRICS_PATH, "w") as f:
        json.dump(saveable, f, indent=2)
    print(f"\n[INFO] Metrics JSON â†’ {METRICS_PATH}")

    # Charts
    plot_comparison(all_metrics)

    best = max(all_metrics, key=lambda x: all_metrics[x]["f1_score"])
    print(f"\n[INFO] Best model: {best}  (F1: {all_metrics[best]['f1_score']}%)")
    plot_confusion_matrix(y_test, all_metrics[best]["y_pred"], le, best)

    print("\nâœ…  Evaluation complete!\n")

