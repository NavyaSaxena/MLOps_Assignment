import pandas as pd


def make_binary_target(df: pd.DataFrame, target_col: str = "num") -> pd.DataFrame:
    if target_col not in df.columns:
        raise KeyError(f"Missing target column: {target_col}")
    out = df.copy()
    out["target"] = (out[target_col] > 0).astype(int)
    return out