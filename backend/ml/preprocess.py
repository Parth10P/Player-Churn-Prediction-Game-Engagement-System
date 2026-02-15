"""
Preprocessing module for Player Churn Prediction.
Handles data loading, encoding, scaling, and train/test splitting.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "online_gaming_behavior_dataset.csv")
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")


def load_data(path=DATA_PATH):
    """Load the raw CSV dataset."""
    df = pd.read_csv(path)
    return df


def create_target(df):
    """Create binary churn column from EngagementLevel."""
    df = df.copy()
    df["Churned"] = (df["EngagementLevel"] == "Low").astype(int)
    return df


def encode_categoricals(df, fit=True, label_encoders=None):
    """
    Encode categorical columns using LabelEncoder.
    If fit=True, fit new encoders and save them.
    If fit=False, use provided label_encoders to transform.
    """
    df = df.copy()
    categorical_cols = ["Gender", "Location", "GameGenre", "GameDifficulty"]

    if fit:
        label_encoders = {}
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le
        os.makedirs(MODELS_DIR, exist_ok=True)
        joblib.dump(label_encoders, os.path.join(MODELS_DIR, "label_encoders.pkl"))
    else:
        if label_encoders is None:
            label_encoders = joblib.load(os.path.join(MODELS_DIR, "label_encoders.pkl"))
        for col in categorical_cols:
            df[col] = label_encoders[col].transform(df[col])

    return df, label_encoders


def split_data(df, test_size=0.2, random_state=42):
    """Split into train/test sets."""
    X = df.drop(columns=["PlayerID", "EngagementLevel", "Churned"])
    y = df["Churned"]
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def scale_features(X_train, X_test, fit=True, scaler=None):
    """
    Scale features using StandardScaler.
    If fit=True, fit new scaler and save it.
    If fit=False, use provided scaler to transform.
    """
    if fit:
        scaler = StandardScaler()
        X_train_scaled = pd.DataFrame(
            scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index
        )
        X_test_scaled = pd.DataFrame(
            scaler.transform(X_test), columns=X_test.columns, index=X_test.index
        )
        os.makedirs(MODELS_DIR, exist_ok=True)
        joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
    else:
        if scaler is None:
            scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
        X_train_scaled = pd.DataFrame(
            scaler.transform(X_train), columns=X_train.columns, index=X_train.index
        )
        X_test_scaled = pd.DataFrame(
            scaler.transform(X_test), columns=X_test.columns, index=X_test.index
        )

    return X_train_scaled, X_test_scaled, scaler


def run_preprocessing_pipeline():
    """Run the full preprocessing pipeline end-to-end."""
    print("Loading data...")
    df = load_data()
    print(f"  Dataset shape: {df.shape}")

    print("Creating target variable...")
    df = create_target(df)
    print(f"  Churn rate: {df['Churned'].mean():.2%}")

    print("Encoding categorical features...")
    df, label_encoders = encode_categoricals(df, fit=True)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = split_data(df)
    print(f"  Train: {X_train.shape}, Test: {X_test.shape}")

    print("Scaling features...")
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test, fit=True)

    print("Preprocessing complete!")
    return X_train_scaled, X_test_scaled, y_train, y_test


if __name__ == "__main__":
    run_preprocessing_pipeline()
