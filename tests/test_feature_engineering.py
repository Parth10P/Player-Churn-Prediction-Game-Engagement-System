"""
Tests for the feature engineering module.
Covers all derived features + edge cases.
"""

import pandas as pd
import numpy as np
import pytest
from backend.ml.feature_engineering import (
    run_feature_engineering,
    add_engagement_score,
    add_progression_rate,
    add_purchase_frequency,
    add_inactivity_flag,
    add_session_consistency,
    ENGINEERED_FEATURES,
)


@pytest.fixture
def sample_player():
    """A typical active player."""
    return pd.DataFrame([{
        "Age": 25,
        "Gender": 0,
        "Location": 0,
        "GameGenre": 0,
        "PlayTimeHours": 10.0,
        "InGamePurchases": 1,
        "GameDifficulty": 1,
        "SessionsPerWeek": 5,
        "AvgSessionDurationMinutes": 90,
        "PlayerLevel": 30,
        "AchievementsUnlocked": 15,
    }])


@pytest.fixture
def inactive_player():
    """A player with very low activity — likely to churn."""
    return pd.DataFrame([{
        "Age": 40,
        "Gender": 1,
        "Location": 2,
        "GameGenre": 3,
        "PlayTimeHours": 0.5,
        "InGamePurchases": 0,
        "GameDifficulty": 2,
        "SessionsPerWeek": 1,
        "AvgSessionDurationMinutes": 15,
        "PlayerLevel": 3,
        "AchievementsUnlocked": 0,
    }])


@pytest.fixture
def edge_zero_playtime():
    """Player with 0 play time hours — tests division-by-zero safety."""
    return pd.DataFrame([{
        "Age": 18,
        "Gender": 0,
        "Location": 0,
        "GameGenre": 0,
        "PlayTimeHours": 0.0,
        "InGamePurchases": 0,
        "GameDifficulty": 0,
        "SessionsPerWeek": 0,
        "AvgSessionDurationMinutes": 10,
        "PlayerLevel": 1,
        "AchievementsUnlocked": 0,
    }])


# ─── Engagement Score ───

def test_engagement_score_calculation(sample_player):
    result = add_engagement_score(sample_player)
    expected = 5 * 90  # SessionsPerWeek * AvgSessionDurationMinutes
    assert result["EngagementScore"].iloc[0] == expected


def test_engagement_score_zero_sessions(edge_zero_playtime):
    result = add_engagement_score(edge_zero_playtime)
    assert result["EngagementScore"].iloc[0] == 0


# ─── Progression Rate ───

def test_progression_rate_calculation(sample_player):
    result = add_progression_rate(sample_player)
    expected = 30 / (10.0 + 1)  # PlayerLevel / (PlayTimeHours + 1)
    assert abs(result["ProgressionRate"].iloc[0] - expected) < 1e-6


def test_progression_rate_zero_playtime(edge_zero_playtime):
    """Should NOT divide by zero — formula uses (PlayTimeHours + 1)."""
    result = add_progression_rate(edge_zero_playtime)
    assert np.isfinite(result["ProgressionRate"].iloc[0])
    assert result["ProgressionRate"].iloc[0] == 1 / 1  # level 1 / (0+1)


# ─── Purchase Frequency ───

def test_purchase_frequency_with_purchases(sample_player):
    result = add_purchase_frequency(sample_player)
    expected = 1 / (10.0 + 1)
    assert abs(result["PurchaseFrequency"].iloc[0] - expected) < 1e-6


def test_purchase_frequency_no_purchases(inactive_player):
    result = add_purchase_frequency(inactive_player)
    assert result["PurchaseFrequency"].iloc[0] == 0.0


def test_purchase_frequency_zero_playtime(edge_zero_playtime):
    """Should NOT divide by zero."""
    result = add_purchase_frequency(edge_zero_playtime)
    assert np.isfinite(result["PurchaseFrequency"].iloc[0])


# ─── Inactivity Flag ───

def test_inactive_player_flagged(inactive_player):
    result = add_inactivity_flag(inactive_player)
    assert result["IsInactive"].iloc[0] == 1


def test_active_player_not_flagged(sample_player):
    result = add_inactivity_flag(sample_player)
    assert result["IsInactive"].iloc[0] == 0


def test_boundary_two_sessions():
    """Exactly 2 sessions → should be flagged as inactive (<=2)."""
    df = pd.DataFrame([{"SessionsPerWeek": 2}])
    result = add_inactivity_flag(df)
    assert result["IsInactive"].iloc[0] == 1


def test_boundary_three_sessions():
    """Exactly 3 sessions → should NOT be flagged as inactive."""
    df = pd.DataFrame([{"SessionsPerWeek": 3}])
    result = add_inactivity_flag(df)
    assert result["IsInactive"].iloc[0] == 0


# ─── Session Consistency ───

def test_consistent_player(sample_player):
    result = add_session_consistency(sample_player)
    assert result["SessionConsistency"].iloc[0] == 1


def test_inconsistent_player(inactive_player):
    result = add_session_consistency(inactive_player)
    assert result["SessionConsistency"].iloc[0] == 0


def test_boundary_consistency_three():
    """Exactly 3 sessions → NOT consistent (>3 required)."""
    df = pd.DataFrame([{"SessionsPerWeek": 3}])
    result = add_session_consistency(df)
    assert result["SessionConsistency"].iloc[0] == 0


def test_boundary_consistency_four():
    """4 sessions → consistent."""
    df = pd.DataFrame([{"SessionsPerWeek": 4}])
    result = add_session_consistency(df)
    assert result["SessionConsistency"].iloc[0] == 1


# ─── Full Pipeline ───

def test_run_feature_engineering_adds_all_columns(sample_player):
    result = run_feature_engineering(sample_player)
    for feat in ENGINEERED_FEATURES:
        assert feat in result.columns, f"Missing feature: {feat}"


def test_run_feature_engineering_no_nans(sample_player):
    result = run_feature_engineering(sample_player)
    assert not result[ENGINEERED_FEATURES].isna().any().any()


def test_original_columns_preserved(sample_player):
    original_cols = list(sample_player.columns)
    result = run_feature_engineering(sample_player)
    for col in original_cols:
        assert col in result.columns, f"Original column lost: {col}"


def test_does_not_mutate_input(sample_player):
    original = sample_player.copy()
    run_feature_engineering(sample_player)
    pd.testing.assert_frame_equal(sample_player, original)


def test_multiple_rows():
    """Pipeline works with batch of players."""
    df = pd.DataFrame([
        {"SessionsPerWeek": 5, "AvgSessionDurationMinutes": 60,
         "PlayerLevel": 20, "PlayTimeHours": 8.0,
         "InGamePurchases": 1},
        {"SessionsPerWeek": 1, "AvgSessionDurationMinutes": 15,
         "PlayerLevel": 2, "PlayTimeHours": 0.5,
         "InGamePurchases": 0},
    ])
    result = run_feature_engineering(df)
    assert len(result) == 2
    assert result["EngagementScore"].iloc[0] == 300
    assert result["EngagementScore"].iloc[1] == 15
