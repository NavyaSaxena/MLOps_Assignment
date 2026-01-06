import pandas as pd
import numpy as np
import os
from ucimlrepo import fetch_ucirepo

def ensure_dirs():
    """Creating data directories"""
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

def download_raw_data():
    """Downloading raw UCI Heart Disease dataset"""
    ensure_dirs()
    
    heart = fetch_ucirepo(id=45)
    raw_df = heart.data.original
    
    # Save raw data
    raw_path = "data/raw/heart_disease_uci.csv"
    raw_df.to_csv(raw_path, index=False)
    print(f"Raw data saved: {raw_path}")
    return raw_df

# def load_and_prepare_data():
    """Exact Task 1 data loading and cleaning from your notebook"""
    
    # Loading UCI Heart Disease dataset
    heart = fetch_ucirepo(id=45)

    # Use only the 14 standard attributes (your exact code)
    cols_14 = [
        "age","sex","cp","trestbps","chol","fbs","restecg",
        "thalach","exang","oldpeak","slope","ca","thal","num"
    ]
    df = heart.data.original[cols_14].copy()

    # Handle missing values (your exact code)
    num_cols = ["age","trestbps","chol","thalach","oldpeak","ca"]
    cat_cols = ["sex","cp","fbs","restecg","exang","slope","thal","num"]

    for col in num_cols:
        df[col] = df[col].fillna(df[col].mean())

    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Convert target 'num' to binary
    df["target"] = (df["num"] > 0).astype(int)
    df.drop(columns=["num"], inplace=True)

    return df, num_cols, cat_cols

def load_and_prepare_data(use_cached=True):
    """Load + clean data (Task 1)"""
    ensure_dirs()
    
    raw_path = "data/raw/heart_disease_uci.csv"
    processed_path = "data/processed/heart_disease_cleaned.csv"
    
    # Download if no raw data
    if not os.path.exists(raw_path):
        print("Downloading raw data...")
        raw_df = download_raw_data()
    else:
        print("Loading cached raw data...")
        raw_df = pd.read_csv(raw_path)
    
    # Use only 14 standard attributes
    cols_14 = [
        "age","sex","cp","trestbps","chol","fbs","restecg",
        "thalach","exang","oldpeak","slope","ca","thal","num"
    ]
    df = raw_df[cols_14].copy()
    
    # Handle missing values
    num_cols = ["age","trestbps","chol","thalach","oldpeak","ca"]
    cat_cols = ["sex","cp","fbs","restecg","exang","slope","thal","num"]
    
    for col in num_cols:
        df[col] = df[col].fillna(df[col].mean())
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])
    
    # Convert target 'num' to binary
    df["target"] = (df["num"] > 0).astype(int)
    df.drop(columns=["num"], inplace=True)
    
    # Cache cleaned data
    if not os.path.exists(processed_path):
        df.to_csv(processed_path, index=False)
        print(f"Cleaned data saved: {processed_path}")
    else:
        print(f"Using cached cleaned data: {processed_path}")
    
    return df, num_cols, cat_cols[:-1]  # Remove 'num' from cat_cols

if __name__ == "__main__":
    df, num_cols, cat_cols = load_and_prepare_data()
    print("Data shape:", df.shape)
    print("Target balance:\n", df["target"].value_counts(normalize=True))
    df["target"].value_counts(normalize=True)
    print("\n✅ Data pipeline complete!")