# Task 8: Monitoring & Logging (Prometheus + Grafana)

## Overview
Complete monitoring stack for the heart disease prediction API with:
- **API metrics** exposed via `/metrics` endpoint
- **Prometheus** for metrics collection
- **Grafana** for visualization and dashboards

## Prerequisites
- Docker and Docker Compose
- API image: `2023ac05057/heart-disease-api:v3`

## Setup Instructions

1. Pull Docker Image
  docker pull 2023ac05057/heart-disease-api:v3

2. Start Monitoring Stack
  cd monitoring
  docker-compose up -d

3. Access Dashboards
|Service   |        URL          |Credentials
|API	   |http://localhost:5001|/predict endpoint
|Prometheus|http://localhost:9090|	-
|Grafana   |http://localhost:3000|admin/admin

4. Verify Monitoring
Test API:
curl -X POST http://localhost:5001/predict \
-H "Content-Type: application/json" \
-d '{"age":55,"sex":1,"cp":2,"trestbps":140,"chol":250,"fbs":0,"restecg":1,"thalach":150,"exang":0,"oldpeak":1.5,"slope":2,"ca":0,"thal":2}'
Check Prometheus targets: http://localhost:9090/targets
→ Verify heart-disease-api shows UP

Grafana dashboards: http://localhost:3000
→ Prometheus datasource auto-configured → API metrics visible

5. Stop Stack

docker-compose down
