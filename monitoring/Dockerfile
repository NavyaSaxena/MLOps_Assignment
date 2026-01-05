# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements (create a requirements.txt in Colab if not already)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code
COPY /app .

# Copy the trained model
COPY models/ models/

# Expose the port your Flask app runs on
EXPOSE 5001

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Command to run the Flask app
CMD ["flask", "run", "--port=5001"]

