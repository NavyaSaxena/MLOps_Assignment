# Docker Run Guide (Task 6)

## Prerequisites
- Install Docker
- Install curl for testing API calls (most systems already have it)

## Steps to run
1. Pull the Docker image from Docker Hub:
 $ docker pull 2024aa05228/heart-disease-api:v1

2. Run the API container locally:
 $ docker run -d -p 5001:5001 2024aa05228/heart-disease-api:v1

This will start the API on [**http://127.0.0.1:5001**](http://127.0.0.1:5001)

3. Test the `/predict` endpoint with a sample request:

 $ curl -X POST http://127.0.0.1:5001/predict
-H "Content-Type: application/json"
-d '{
"age": 55,
"sex": 1,
"cp": 2,
"trestbps": 140,
"chol": 250,
"fbs": 0,
"restecg": 1,
"thalach": 150,
"exang": 0,
"oldpeak": 1.5,
"slope": 2,
"ca": 0,
"thal": 2
}'

The API will return a JSON response with the prediction and confidence.