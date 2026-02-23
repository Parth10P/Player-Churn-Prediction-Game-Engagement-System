"""
Train and evaluate a Random Forest model for player churn prediction.
Issue #6 — mirrors src/train_logistic.py but with RandomForest(n_estimators=100).

Outputs:
  models/rf_results.txt         — evaluation metrics
  models/rf_model.pkl           — serialised model
  notebooks/plots/confusion_matrix_rf.png
  notebooks/plots/feature_importance_rf.png
"""

import os
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
)

from preprocess import X_train_scaled, X_test_scaled, y_train, y_test, feature_names

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
PLOTS_DIR = os.path.join(BASE_DIR, "notebooks", "plots")


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # ── Train ──────────────────────────────────────────────────
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)

    # ── Evaluate ───────────────────────────────────────────────
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    print(f"Model trained successfully! F1 Score: {f1:.4f}")

    # ── Save results ───────────────────────────────────────────
    results_path = os.path.join(MODELS_DIR, "rf_results.txt")
    with open(results_path, "w") as f:
        f.write("Random Forest Evaluation Metrics\n")
        f.write("================================\n")
        f.write(f"Accuracy: {acc:.4f}\n")
        f.write(f"Precision: {prec:.4f}\n")
        f.write(f"Recall: {rec:.4f}\n")
        f.write(f"F1 Score: {f1:.4f}\n")
        f.write(f"ROC-AUC: {roc_auc:.4f}\n")

    # ── Save model ─────────────────────────────────────────────
    model_path = os.path.join(MODELS_DIR, "rf_model.pkl")
    joblib.dump(model, model_path)

    print(f"Exported metrics to {results_path}")
    print(f"Exported model to {model_path}")

    # ── Confusion matrix ───────────────────────────────────────
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
                xticklabels=["Active", "Churned"],
                yticklabels=["Active", "Churned"])
    plt.title("Random Forest Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    cm_path = os.path.join(PLOTS_DIR, "confusion_matrix_rf.png")
    plt.savefig(cm_path)
    plt.close()
    print(f"Confusion matrix saved to {cm_path}")

    # ── Feature importance ─────────────────────────────────────
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.figure(figsize=(10, 6))
    plt.barh(
        [feature_names[i] for i in indices],
        importances[indices],
        color=sns.color_palette("viridis", len(feature_names)),
    )
    plt.xlabel("Importance")
    plt.title("Random Forest — Feature Importance")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    fi_path = os.path.join(PLOTS_DIR, "feature_importance_rf.png")
    plt.savefig(fi_path)
    plt.close()
    print(f"Feature importance plot saved to {fi_path}")


if __name__ == "__main__":
    main()
