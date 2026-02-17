"""
Flask REST API for Player Churn Prediction.
Provides endpoints for predictions and model info.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.ml.predict import predict_single, load_model
from backend.ml.train import run_training_pipeline

app = Flask(__name__)
CORS(app)  # Allow frontend to call API


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Player Churn Prediction API is running"})


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Predict churn for a single player.

    Expects JSON body:
    {
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
        "AchievementsUnlocked": 15
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        required_fields = [
            "Age", "Gender", "Location", "GameGenre", "PlayTimeHours",
            "InGamePurchases", "GameDifficulty", "SessionsPerWeek",
            "AvgSessionDurationMinutes", "PlayerLevel", "AchievementsUnlocked"
        ]
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        result = predict_single(data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/train", methods=["POST"])
def train():
    """Trigger model retraining."""
    try:
        run_training_pipeline()
        return jsonify({"status": "ok", "message": "Model retrained successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/model/info", methods=["GET"])
def model_info():
    """Get model metadata."""
    try:
        model, scaler, label_encoders, feature_names = load_model()
        return jsonify({
            "model_type": type(model).__name__,
            "n_features": len(feature_names),
            "features": feature_names,
            "categorical_mappings": {
                col: list(le.classes_) for col, le in label_encoders.items()
            },
        })
    except Exception as e:
        return jsonify({"error": f"Model not trained yet: {str(e)}"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
