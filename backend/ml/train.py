import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
import joblib
import os

from backend.ml.preprocess import (
    load_data, create_target, encode_categoricals,
    split_data, scale_features, MODELS_DIR
)
from backend.ml.feature_engineering import run_feature_engineering


def train_model(X_train, y_train):
    """Train a Logistic Regression classifier for smoother probabilities."""
    model = LogisticRegression(
        random_state=42,
        class_weight="balanced",
        max_iter=1000,
        C=0.1
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate the model and print metrics."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "ROC-AUC": roc_auc_score(y_test, y_proba),
    }

    print("\n--- Model Evaluation ---")
    print(f"Accuracy:  {metrics['Accuracy']:.4f}")
    print(f"ROC AUC:   {metrics['ROC-AUC']:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Active", "Churned"]))

    return metrics, y_pred, y_proba


def save_model(model, filename="churn_model.pkl"):
    """Save the trained model to disk."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    path = os.path.join(MODELS_DIR, filename)
    joblib.dump(model, path)
    print(f"Model saved to {path}")


def save_results(metrics):
    """Persist evaluation metrics for the backend/API layer."""
    os.makedirs(os.path.join(os.path.dirname(MODELS_DIR), "models"), exist_ok=True)
    results_path = os.path.join(os.path.dirname(MODELS_DIR), "models", "logistic_results.txt")
    with open(results_path, "w", encoding="utf-8") as f:
        f.write("Logistic Regression Evaluation Metrics\n")
        f.write("======================================\n")
        for key, value in metrics.items():
            f.write(f"{key}: {value:.4f}\n")
    print(f"Metrics saved to {results_path}")


def save_feature_weights(model, feature_names):
    """Persist signed logistic coefficients for interpretability."""
    coef = model.coef_[0]
    weights = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": coef,
            "abs_coefficient": np.abs(coef),
            "odds_multiplier": np.exp(coef),
        }
    ).sort_values("abs_coefficient", ascending=False)

    weights_path = os.path.join(MODELS_DIR, "logistic_feature_weights.csv")
    weights.to_csv(weights_path, index=False)
    print(f"Feature weights saved to {weights_path}")


def run_training_pipeline():
    """Run the full training pipeline."""
    print("=" * 60)
    print("PLAYER CHURN PREDICTION — TRAINING PIPELINE")
    print("=" * 60)

    # Preprocessing
    df = load_data()
    df = create_target(df)
    df, _ = encode_categoricals(df, fit=True)

    # Feature engineering
    df = run_feature_engineering(df)

    # Split & scale
    X_train, X_test, y_train, y_test = split_data(df)
    X_train_scaled, X_test_scaled, _ = scale_features(X_train, X_test, fit=True)

    # Train
    print("\nTraining Logistic Regression model...")
    model = train_model(X_train_scaled, y_train)

    # Evaluate
    metrics, _, _ = evaluate_model(model, X_test_scaled, y_test)

    # Save
    save_model(model)
    save_results(metrics)

    # Save feature names for prediction
    feature_names = list(X_train_scaled.columns)
    joblib.dump(feature_names, os.path.join(MODELS_DIR, "feature_names.pkl"))
    save_feature_weights(model, feature_names)
    print(f"Feature names saved ({len(feature_names)} features)")

    print("\nTraining pipeline complete!")
    return model


if __name__ == "__main__":
    run_training_pipeline()
