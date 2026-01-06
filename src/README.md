# `src/` - MLOps Pipeline Core

## Core Files

| File | Purpose |
|------|---------|
| `api.py` | FastAPI prediction server |
| `data.py` | Data download + cleaning |
| `model.py` | Model training + evaluation |
| `preprocess.py` | Scaling + encoding |

## Quick Start

```bash
# 1. Train model
python -m src.model

# 2. Start API
uvicorn src.api:app --reload --host 127.0.0.1 --port 8000
```
View on Docs: http://127.0.0.1:8000/docs

## API Endpoints
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/predict
```

POST Prediction:
```bash
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"age":50,"sex":1,"cp":2,"trestbps":120,"chol":220,"fbs":0,"restecg":1,"thalach":160,"exang":0,"oldpeak":1.0,"slope":2,"ca":0,"thal":3}'
```
## Test
```bash
pytest -q
```
## Run end to end pipeline
```bash
python -m src.pipeline
```