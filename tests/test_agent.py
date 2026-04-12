"""
Tests for the internal agent workflow and the optional Ask Agent behavior
supported by the main /predict endpoint.
"""

from backend.agent.workflow import create_agent_workflow
from backend.main import PredictInput, load_artifacts, predict


VALID_PLAYER = {
    "Age": 25,
    "Gender": "Male",
    "Location": "USA",
    "GameGenre": "Action",
    "PlayTimeHours": 10.5,
    "InGamePurchases": 1,
    "GameDifficulty": "Medium",
    "SessionsPerWeek": 5,
    "AvgSessionDurationMinutes": 90,
    "PlayerLevel": 30,
    "AchievementsUnlocked": 15,
}


def test_agent_workflow_generates_structured_report():
    agent = create_agent_workflow()

    result = agent.invoke({"player_data": VALID_PLAYER})

    assert "ml_prediction" in result
    assert "final_report" in result
    assert "engagement_analysis" in result

    report = result["final_report"]
    assert "executive_summary" in report
    assert "key_risk_factors" in report
    assert "personalized_strategies" in report
    assert "industry_best_practices" in report
    assert "sources" in report
    assert report["confidence_level"] in ("high", "medium", "low")


def test_agent_workflow_uses_fallbacks_when_llm_is_unavailable():
    agent = create_agent_workflow()

    result = agent.invoke({"player_data": VALID_PLAYER})

    assert "warnings" in result
    assert isinstance(result["warnings"], list)
    assert len(result["warnings"]) >= 1


def test_predict_without_query_keeps_agent_fields_empty():
    load_artifacts()
    response = predict(PredictInput(**VALID_PLAYER))
    payload = response.model_dump()

    assert payload["agent_query"] is None
    assert payload["agent_answer"] is None
    assert payload["agent_strategies"] == []


def test_predict_with_query_returns_agent_follow_up_fields():
    load_artifacts()
    response = predict(
        PredictInput(
            **{
                **VALID_PLAYER,
                "query": "Why is this player likely to churn and what should we do next?",
            }
        )
    )
    payload = response.model_dump()

    assert payload["agent_query"]
    assert isinstance(payload["agent_strategies"], list)
    assert "recommendations" in payload
