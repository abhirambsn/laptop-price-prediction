from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path
from utils import Predictor
import logging

log_path = Path(__file__).parent / 'logs' / 'app.log'
model_path = Path(__file__).parent.parent / 'models' / 'best_model.joblib'
preprocessor_path = Path(__file__).parent.parent / 'models' / 'preprocessor.joblib'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_hnd = logging.FileHandler(log_path)
file_hnd.setLevel(logging.INFO)
logger.addHandler(file_hnd)

app = Flask(__name__)
CORS(app)

base_path = "/api/v1"

@app.route(f"{base_path}/healthz", methods=["GET"])
def health():
    return jsonify({"status": "OK"}), 200

@app.route(f"{base_path}/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        logger.info(f"Received data: {data.values()}")
        predictor = Predictor(model_path, preprocessor_path)
        prediction = predictor.predict(data.values())
        logger.info(f"Prediction: {prediction}")
        return jsonify({"price": predictor.format_prediction(prediction)}), 200
    except Exception as e:
        logger.error(f"Failed to predict: {e}")
        return jsonify({"error": "Failed to predict"}), 500

if __name__ == "__main__":
    logger.info("Starting server...")
    app.run(host="0.0.0.0", port=6000, debug=True)