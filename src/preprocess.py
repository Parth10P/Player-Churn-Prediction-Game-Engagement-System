"""
Shared preprocessing module for standalone src/ training scripts.
Mirrors backend/ml/preprocess.py + feature_engineering.py logic,
but exposes ready-to-use train/test splits at module level.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# ── Paths ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "online_gaming_behavior_dataset.csv")

# ── Load & prepare ─────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)

# Target variable
df["Churned"] = (df["EngagementLevel"] == "Low").astype(int)

# Encode categoricals
categorical_cols = ["Gender", "Location", "GameGenre", "GameDifficulty"]
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Feature engineering (same as backend/ml/feature_engineering.py)
df["EngagementScore"] = df["SessionsPerWeek"] * df["AvgSessionDurationMinutes"]
df["ProgressionRate"] = df["PlayerLevel"] / (df["PlayTimeHours"] + 1)
df["PurchaseFrequency"] = df["InGamePurchases"] / (df["PlayTimeHours"] + 1)
df["IsInactive"] = (df["SessionsPerWeek"] <= 2).astype(int)
df["SessionConsistency"] = (df["SessionsPerWeek"] > 3).astype(int)

# Split
X = df.drop(columns=["PlayerID", "EngagementLevel", "Churned"])
y = df["Churned"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(
    scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index
)
X_test_scaled = pd.DataFrame(
    scaler.transform(X_test), columns=X_test.columns, index=X_test.index
)

feature_names = list(X_train.columns)
