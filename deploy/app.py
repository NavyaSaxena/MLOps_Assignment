from flask import Flask, request, jsonify, Response
import joblib
import pandas as pd
import os
import logging, time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUESTS = Counter('api_requests_total', 'Total number of requests', ['endpoint'])
LATENCY = Histogram('api_requests_latency_ms', 'Request latency (ms)', ['endpoint'])

app = Flask(__name__)

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
    )

# Load trained pipeline (includes preprocessing)

#model = joblib.load("models/heart_disease_model.pkl")
model = joblib.load("models/heart_best_pipeline.pkl")

# Define feature columns in the same order as training
feature_columns = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

@app.before_request
def before_request():
    REQUESTS.labels(endpoint=request.endpoint).inc()
    request.start_time = time.time()
    app.logger.info(f"Incoming request: {request.method} {request.path}")

@app.after_request
def after_request(response):
    if hasattr(request, 'start_time'):
        LATENCY.labels(endpoint=request.endpoint).observe((time.time() - request.start_time) * 1000)
    app.logger.info(f"Response status: {response.status_code}")
    return response

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Convert input JSON to DataFrame
    features_df = pd.DataFrame([data], columns=feature_columns)

    # Make prediction
    prediction = model.predict(features_df)[0]
    confidence = model.predict_proba(features_df)[0][1]

    return jsonify({
        "prediction": int(prediction),
        "confidence": round(float(confidence), 3)
    })

@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)