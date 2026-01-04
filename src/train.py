#!/usr/bin/env python3
"""
Run full training pipeline: Tasks 2, 3, 4
Usage: python src/train.py
"""

from .model import train_models, log_mlflow_experiments, save_best_model

def main():
    print("Starting MLOps Heart Disease Pipeline...")
    
    # Task 2: Train models
    results = train_models()
    
    # Task 3: Log to MLflow
    log_mlflow_experiments(results)
    
    # Task 4: Save best model
    model_path = save_best_model(results)
    
    # Summary table (your exact metrics table)
    import pandas as pd
    metrics_df = pd.DataFrame([results["log_metrics"], results["rf_metrics"]],
                            index=["LogisticRegression","RandomForest"])
    print("\nFinal Metrics:")
    print(metrics_df)
    
    print(f"\n✅ Pipeline complete. Best model: {results['best_name']}")

if __name__ == "__main__":
    main()