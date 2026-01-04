import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo

def load_and_prepare_data():
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

if __name__ == "__main__":
    df, num_cols, cat_cols = load_and_prepare_data()
    print("Data shape:", df.shape)
    print("Target balance:\n", df["target"].value_counts(normalize=True))