"""
Feature Engineering module for Player Churn Prediction.
Creates derived features that improve model performance.
"""

import pandas as pd
import numpy as np


def add_engagement_score(df):
    """Players who play more often and longer."""
    df = df.copy()
    df["EngagementScore"] = df["SessionsPerWeek"] * df["AvgSessionDurationMinutes"]
    return df


def add_progression_rate(df):
    """How fast the player levels up relative to time spent."""
    df = df.copy()
    df["ProgressionRate"] = df["PlayerLevel"] / (df["PlayTimeHours"] + 1)
    return df


def add_purchase_frequency(df):
    """Purchase frequency relative to play time."""
    df = df.copy()
    df["PurchaseFrequency"] = df["InGamePurchases"] / (df["PlayTimeHours"] + 1)
    return df


def add_inactivity_flag(df):
    """Flag players with very low session count as inactive."""
    df = df.copy()
    df["IsInactive"] = (df["SessionsPerWeek"] <= 2).astype(int)
    return df


def add_session_consistency(df):
    """Flag players with consistent session activity."""
    df = df.copy()
    df["SessionConsistency"] = (df["SessionsPerWeek"] > 3).astype(int)
    return df


def run_feature_engineering(df):
    """Apply all feature engineering steps."""
    df = add_engagement_score(df)
    df = add_progression_rate(df)
    df = add_purchase_frequency(df)
    df = add_inactivity_flag(df)
    df = add_session_consistency(df)
    return df


ENGINEERED_FEATURES = [
    "EngagementScore",
    "ProgressionRate",
    "PurchaseFrequency",
    "IsInactive",
    "SessionConsistency",
]


if __name__ == "__main__":
    from backend.ml.preprocess import load_data, create_target

    df = load_data()
    df = create_target(df)
    df = run_feature_engineering(df)

    print("Engineered Feature Statistics:")
    print(df[ENGINEERED_FEATURES].describe().round(2))

    print("\nCorrelation with Churn:")
    for feat in ENGINEERED_FEATURES:
        corr = df[feat].corr(df["Churned"])
        print(f"  {feat}: {corr:.4f}")
