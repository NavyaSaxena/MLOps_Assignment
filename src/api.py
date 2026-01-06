from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(
    title="Heart Disease Prediction API", 
    version="1.0.0",
    description="API using a complete ML pipeline to predict heart disease presence."
)

# Loading COMPLETE pipeline (model + preprocessor)
print("Loading complete pipeline from artifacts/...")
pipeline = joblib.load("artifacts/heart_best_pipeline.pkl")
print("Pipeline loaded successfully! Ready for predictions.")

class PredictionRequest(BaseModel):
    age: float           # Age in years
    sex: int             # 0=Female, 1=Male
    cp: int              # Chest pain type (0-3)
    trestbps: float      # Resting blood pressure
    chol: float          # Serum cholesterol
    fbs: int             # Fasting blood sugar >120mg/dl (0/1)
    restecg: int         # Resting ECG results (0-2)
    thalach: float       # Maximum heart rate
    exang: int           # Exercise-induced angina (0/1)
    oldpeak: float       # ST depression
    slope: int           # Slope of peak exercise ST (0-2)
    ca: float            # Number of major vessels (0-3)
    thal: int            # Thalassemia (0-3)

@app.get("/")
async def root():
    """API Root - Health status"""
    return {
        "message": "Heart Disease Prediction API", 
        "status": "healthy", 
        "model": "Complete Pipeline (ROC-AUC: 0.963)",
        "docs": "/docs",
        "predict_sample": "/predict"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "OK", "pipeline_loaded": True, "ready_for_predictions": True}

@app.get("/predict")
async def predict_sample():
    """Sample prediction for testing"""
    sample_data = {
        "age": 63, "sex": 1, "cp": 1, "trestbps": 145, "chol": 233,
        "fbs": 1, "restecg": 2, "thalach": 150, "exang": 0, 
        "oldpeak": 2.3, "slope": 3, "ca": 0, "thal": 6
    }
    
    features_df = pd.DataFrame([sample_data])
    prediction = pipeline.predict(features_df)[0]
    probability = pipeline.predict_proba(features_df)[0]
    
    return {
        "sample_patient": "63yo male, chest pain, high BP, abnormal ECG",
        "prediction": int(prediction),
        "prediction_class": "Heart Disease" if prediction == 1 else "No Heart Disease",
        "confidence": round(float(probability[1] if prediction == 1 else probability[0]), 3),
        "probabilities": {
            "no_disease": round(float(probability[0]), 3),
            "disease": round(float(probability[1]), 3)
        }
    }

@app.post("/predict")
async def predict(request: PredictionRequest):
    """Predict heart disease for new patient"""
    try:
        # Create DataFrame (pipeline expects DataFrame input)
        features_df = pd.DataFrame([request.dict()])
        
        # Pipeline handles ALL preprocessing + prediction!
        prediction = pipeline.predict(features_df)[0]
        probability = pipeline.predict_proba(features_df)[0]
        
        return {
            "prediction": int(prediction),
            "prediction_class": "Heart Disease" if prediction == 1 else "No Heart Disease",
            "confidence": round(float(probability[1] if prediction == 1 else probability[0]), 3),
            "probabilities": {
                "no_disease": round(float(probability[0]), 3),
                "disease": round(float(probability[1]), 3)
            },
            "patient_features": request.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)