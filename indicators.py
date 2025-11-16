# indicators.py
import pandas as pd

def compute_zscore(df):
    return (df - df.mean()) / df.std()

def add_credit_ratio(df):
    if "HYG" in df.columns and "LQD" in df.columns:
        df["HYG/LQD"] = df["HYG"] / df["LQD"]
    return df

def compute_stress_score(z):
    z = z.copy()

    needed = ["^VIX", "^VIX3M", "^VIX6M", "HYG/LQD", "^TNX", "UUP", "EEM"]
    z = z[[c for c in needed if c in z.columns]].dropna()

    MSS_raw = (
        0.30 * z["^VIX"] +
        0.15 * z["^VIX3M"] +
        0.10 * z["^VIX6M"] +
        0.25 * z["HYG/LQD"] +
        0.15 * z["^TNX"] +
        0.05 * z["UUP"] -
        0.10 * z["EEM"]
    )

    MSS = 50 + 10 * MSS_raw
    return MSS.to_frame("Stress Score")
