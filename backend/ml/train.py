"""
Model training module for Player Churn Prediction.
Trains a Random Forest classifier and saves the model.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
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

    print("\n--- Model Evaluation ---")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC AUC:   {roc_auc_score(y_test, y_proba):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Active", "Churned"]))

    return y_pred, y_proba


def save_model(model, filename="churn_model.pkl"):
    """Save the trained model to disk."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    path = os.path.join(MODELS_DIR, filename)
    joblib.dump(model, path)
    print(f"Model saved to {path}")


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
    evaluate_model(model, X_test_scaled, y_test)

    # Save
    save_model(model)

    # Save feature names for prediction
    feature_names = list(X_train_scaled.columns)
    joblib.dump(feature_names, os.path.join(MODELS_DIR, "feature_names.pkl"))
    print(f"Feature names saved ({len(feature_names)} features)")

    print("\nTraining pipeline complete!")
    return model


if __name__ == "__main__":
    run_training_pipeline()
