import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, roc_auc_score, RocCurveDisplay
)
import matplotlib.pyplot as plt
import joblib
import mlflow
import mlflow.sklearn
import os

from .data import load_and_prepare_data

def train_models():
    """Your exact Task 2 model training code"""
    
    # Load data (Task 1 output)
    df, num_cols, cat_cols = load_and_prepare_data()
    
    X = df.drop(columns=["target"])
    y = df["target"]

    # Your exact preprocessing pipeline
    numeric_features = num_cols
    categorical_features = ["sex","cp","fbs","restecg","exang","slope","ca","thal"]

    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Logistic Regression (your exact code)
    log_reg = LogisticRegression(max_iter=1000, solver="liblinear")
    log_clf = Pipeline([("preprocess", preprocessor), ("model", log_reg)])
    
    param_grid_log = {
        "model__C": [0.01, 0.1, 1, 10],
        "model__penalty": ["l1", "l2"]
    }
    grid_log = GridSearchCV(log_clf, param_grid_log, cv=cv, scoring="roc_auc", n_jobs=-1)
    grid_log.fit(X_train, y_train)
    best_log = grid_log.best_estimator_

    y_pred_log = best_log.predict(X_test)
    y_proba_log = best_log.predict_proba(X_test)[:, 1]
    log_metrics = {
        "accuracy": accuracy_score(y_test, y_pred_log),
        "precision": precision_score(y_test, y_pred_log),
        "recall": recall_score(y_test, y_pred_log),
        "roc_auc": roc_auc_score(y_test, y_proba_log),
    }

    # Random Forest (your exact code)
    rf = RandomForestClassifier(random_state=42)
    rf_clf = Pipeline([("preprocess", preprocessor), ("model", rf)])
    
    param_grid_rf = {
        "model__n_estimators": [100, 200],
        "model__max_depth": [None, 5, 10],
        "model__min_samples_split": [2, 5],
    }
    grid_rf = GridSearchCV(rf_clf, param_grid_rf, cv=cv, scoring="roc_auc", n_jobs=-1)
    grid_rf.fit(X_train, y_train)
    best_rf = grid_rf.best_estimator_

    y_pred_rf = best_rf.predict(X_test)
    y_proba_rf = best_rf.predict_proba(X_test)[:, 1]
    rf_metrics = {
        "accuracy": accuracy_score(y_test, y_pred_rf),
        "precision": precision_score(y_test, y_pred_rf),
        "recall": recall_score(y_test, y_pred_rf),
        "roc_auc": roc_auc_score(y_test, y_proba_rf),
    }

    # Auto-select best model (Task 4)
    if rf_metrics["roc_auc"] >= log_metrics["roc_auc"]:
        best_model, best_name = best_rf, "RandomForest"
        best_metrics = rf_metrics
    else:
        best_model, best_name = best_log, "LogisticRegression"
        best_metrics = log_metrics

    return {
        "best_model": best_model,
        "best_name": best_name,
        "best_metrics": best_metrics,
        "log_model": best_log,
        "log_metrics": log_metrics,
        "rf_model": best_rf,
        "rf_metrics": rf_metrics,
        "X_test": X_test,
        "y_test": y_test,
        "y_proba_log": y_proba_log,
        "y_proba_rf": y_proba_rf
    }

def log_mlflow_experiments(results):
    """Your exact Task 3 MLflow logging code"""
    
    mlflow.set_experiment("heart_disease_uci")
    
    # Logistic Regression run
    with mlflow.start_run(run_name="logistic_regression"):
        mlflow.log_param("model_type", "LogisticRegression")
        for m_name, m_val in results["log_metrics"].items():
            mlflow.log_metric(m_name, float(m_val))

        # ROC plot
        fig, ax = plt.subplots(figsize=(6,5))
        RocCurveDisplay.from_predictions(results["y_test"], results["y_proba_log"], name="Logistic Regression", ax=ax)
        plt.plot([0,1],[0,1],"k--", label="Random")
        plt.title("ROC curves")
        plt.legend()
        fig.savefig("roc_logreg.png")
        plt.close(fig)
        mlflow.log_artifact("roc_logreg.png")
        mlflow.sklearn.log_model(results["log_model"], artifact_path="model")

    # Random Forest run
    with mlflow.start_run(run_name="random_forest"):
        mlflow.log_param("model_type", "RandomForest")
        for m_name, m_val in results["rf_metrics"].items():
            mlflow.log_metric(m_name, float(m_val))

        fig, ax = plt.subplots(figsize=(6,5))
        RocCurveDisplay.from_predictions(results["y_test"], results["y_proba_rf"], name="Random Forest", ax=ax)
        plt.plot([0,1],[0,1],"k--", label="Random")
        plt.title("ROC curves")
        plt.legend()
        fig.savefig("roc_rf.png")
        plt.close(fig)
        mlflow.log_artifact("roc_rf.png")
        mlflow.sklearn.log_model(results["rf_model"], artifact_path="model")

def save_best_model(results, model_path="artifacts/heart_best_pipeline.pkl"):
    """Task 4 - Save final model"""
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(results["best_model"], model_path)
    print(f"Best model ({results['best_name']}) saved to {model_path}")
    return model_path