import json
from typing import Any

def build_analysis_prompt(player_data: dict[str, Any], prediction: dict[str, Any]) -> str:
    return f"""
You are a highly skilled gaming retention analyst.
Given the player data and ML prediction below, explain why this player may churn.

Player data:
{json.dumps(player_data, indent=2)}

ML prediction:
{json.dumps(prediction, indent=2)}

Return valid JSON with this exact shape:
{{
  "engagement_analysis": "2-4 sentence explanation in clear language",
  "key_risk_factors": ["factor 1", "factor 2", "factor 3"],
  "confidence_level": "high" | "medium" | "low"
}}

Rules:
- Be specific to the data.
- Do not invent features not present in the player data.
- Keep factors actionable and easy to understand.
"""

def build_report_prompt(
    user_query: str,
    player_data: dict[str, Any],
    prediction: dict[str, Any],
    analysis: dict[str, Any],
    industry_best_practices: list[str]
) -> str:
    return f"""
You are creating a structured churn-risk report for a gaming analytics product.

User question: {user_query}

Player data:
{json.dumps(player_data, indent=2)}

ML prediction:
{json.dumps(prediction, indent=2)}

Analysis:
{json.dumps(analysis, indent=2)}

Industry research:
{json.dumps(industry_best_practices, indent=2)}

CRITICAL INSTRUCTIONS FOR USER QUESTION:
1. SPELLING ERROR CORRECTION: Actively interpret and fix any spelling mistakes or typos in the user's question (e.g., "playre chrun" -> "player churn", "imporve" -> "improve"). Do not be strict about typos.
2. OFF-TOPIC GUARDRAIL: If the question is completely unrelated to gaming, player engagement, or churn prediction (e.g., "What's the weather?", "How do I improve my generic logic?", etc.), you MUST decline.
   - Write exactly this in the `direct_answer_to_user` field: "I'm specialized in player churn analysis and game engagement strategies. Please ask a question related to this player's gaming behavior or retention."
3. RELEVANT QUERIES: If the question IS related to the player, analyze their stats and answer directly and insightfully in the `direct_answer_to_user` field.

Return valid JSON with this exact shape:
{{
  "direct_answer_to_user": "Clear, direct paragraph directly answering the User question (or the off-topic rejection message)",
  "executive_summary": "2-3 sentence overview",
  "engagement_analysis": "clear explanation",
  "key_risk_factors": ["factor 1", "factor 2"],
  "personalized_strategies": ["strategy 1", "strategy 2", "strategy 3"],
  "industry_best_practices": ["practice 1", "practice 2"],
  "sources": ["https://..."],
  "disclaimers": ["ethical disclaimer 1", "UX disclaimer 2"],
  "confidence_level": "high" | "medium" | "low"
}}

Rules:
- Keep recommendations grounded in the player profile.
- Do not invent URLs or citations.
- Include ethical disclaimers about AI-generated predictions and player data privacy.
"""
