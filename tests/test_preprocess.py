"""
Tests for the preprocessing module.
Covers data loading, target creation, encoding, and scaling.
"""

import pandas as pd
import numpy as np
import pytest
import os
from backend.ml.preprocess import (
    load_data,
    create_target,
    encode_categoricals,
    DATA_PATH,
)


# ─── Data Loading ───

class TestLoadData:
    def test_loads_dataframe(self):
        df = load_data()
        assert isinstance(df, pd.DataFrame)

    def test_data_not_empty(self):
        df = load_data()
        assert len(df) > 0

    def test_expected_columns_exist(self):
        df = load_data()
        required = [
            "PlayerID", "Age", "Gender", "Location", "GameGenre",
            "PlayTimeHours", "InGamePurchases", "GameDifficulty",
            "SessionsPerWeek", "AvgSessionDurationMinutes",
            "PlayerLevel", "AchievementsUnlocked", "EngagementLevel",
        ]
        for col in required:
            assert col in df.columns, f"Missing column: {col}"

    def test_no_fully_null_columns(self):
        df = load_data()
        for col in df.columns:
            assert not df[col].isna().all(), f"Column {col} is entirely null"

    def test_dataset_file_exists(self):
        assert os.path.exists(DATA_PATH), f"Dataset not found at {DATA_PATH}"


# ─── Target Creation ───

class TestCreateTarget:
    def test_churned_column_added(self):
        df = load_data()
        result = create_target(df)
        assert "Churned" in result.columns

    def test_churned_is_binary(self):
        df = load_data()
        result = create_target(df)
        assert set(result["Churned"].unique()).issubset({0, 1})

    def test_low_engagement_is_churned(self):
        df = pd.DataFrame({"EngagementLevel": ["Low", "Medium", "High"]})
        result = create_target(df)
        assert result["Churned"].tolist() == [1, 0, 0]

    def test_does_not_mutate_input(self):
        df = load_data()
        original = df.copy()
        create_target(df)
        pd.testing.assert_frame_equal(df, original)

    def test_churn_rate_reasonable(self):
        """Churn rate should be between 10% and 50% for this dataset."""
        df = load_data()
        result = create_target(df)
        rate = result["Churned"].mean()
        assert 0.10 < rate < 0.50, f"Unexpected churn rate: {rate:.2%}"


# ─── Categorical Encoding ───

class TestEncodeCategoricals:
    def test_encoding_produces_numeric(self):
        df = load_data()
        encoded, _ = encode_categoricals(df, fit=True)
        for col in ["Gender", "Location", "GameGenre", "GameDifficulty"]:
            assert pd.api.types.is_numeric_dtype(encoded[col]), f"{col} is not numeric after encoding"

    def test_encoding_returns_label_encoders(self):
        df = load_data()
        _, encoders = encode_categoricals(df, fit=True)
        assert "Gender" in encoders
        assert "GameGenre" in encoders

    def test_encoding_no_nans(self):
        df = load_data()
        encoded, _ = encode_categoricals(df, fit=True)
        for col in ["Gender", "Location", "GameGenre", "GameDifficulty"]:
            assert not encoded[col].isna().any(), f"NaN found in {col} after encoding"

    def test_encoding_preserves_row_count(self):
        df = load_data()
        encoded, _ = encode_categoricals(df, fit=True)
        assert len(encoded) == len(df)
