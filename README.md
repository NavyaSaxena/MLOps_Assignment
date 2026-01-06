# MLOps Assignment: Heart Disease Prediction Pipeline

**Complete MLOps implementation for UCI Heart Disease dataset** following 5 tasks from problem statement.

## Tasks Implemented

| Task | Deliverables |
|------|--------------|
| **Task 1** | EDA + Data Cleaning (`data/raw/`, `data/processed/`, `src/data.py`) |
| **Task 2** | Feature Engineering + 2 Models (`src/model.py`, `artifacts/`) |
| **Task 3** | Model Training Pipeline (`src/pipeline.py`, `src/train.py`) |
| **Task 4** | **REST API** (FastAPI `src/api.py` + Flask `deploy/app.py`) |
| **Task 5** | **Production Deployment** (Docker, MLflow, Monitoring) |

## Technologies & Frameworks

ML: scikit-learn, pandas, numpy
MLOps: MLflow (tracking), joblib (serialization)
API: FastAPI (dev), Flask + Prometheus (prod)
Container: Docker + Gunicorn
Data: UCI ML Repository (ucimlrepo)
Env: Conda (environment.yml)
CI/CD: GitHub Actions
Testing: pytest

## Quick Start (All Platforms)

### **Prerequisites**
```bash
git clone <repo>
cd MLOps_Assignment
```
1. Environment Setup
bash
# Conda (Recommended)
conda env create -f environment.yml
conda activate heart-disease-mlops

# OR Pip (Linux/Mac/Windows)
pip install -r requirements.txt

2. Data Pipeline
```bash
python -m src/data
```
It creates: data/raw/heart_disease_uci.csv + data/processed/heart_disease_cleaned.csv

3. Train Model
```bash
python -m src/model
```
It creates: artifacts/heart_best_pipeline.pkl

4. Start API Server
Development (FastAPI - All platforms):

```bash
uvicorn src.api:app --reload --host 127.0.0.1 --port 8000
Docs: http://127.0.0.1:8000/docs
```

Production (Flask - All platforms):
```bash
gunicorn deploy/app.py:app -w 4 --bind 0.0.0.0:5001
```
5. Test API
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"age":50,"sex":1,"cp":2,"trestbps":120,"chol":220,"fbs":0,"restecg":1,"thalach":160,"exang":0,"oldpeak":1.0,"slope":2,"ca":0,"thal":3}'
```
# Docker (Linux/Mac/Windows)
```bash
# Build
docker build -t heart-disease-mlops .
```
# Run API
docker run -p 8000:8000 heart-disease-mlops uvicorn src.api:app --host 0.0.0.0

# Key Artifacts
text
data/              ← Cleaned datasets
artifacts/         ← Trained models (heart_best_pipeline.pkl)
src/               ← Source code
deploy/            ← Production deployment
notebooks/         ← EDA notebooks
tests/             ← Unit tests

# Usage
EDA: `jupyter notebook notebooks/01eda.ipynb`

Train: `python -m src.model`

Predict: FastAPI `/docs` or Flask `/predict`

Deploy: Docker or Gunicorn

MLOps pipeline `python -m src.pipeline`