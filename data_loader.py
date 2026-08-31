import os
import sys
import pandas as pd
import numpy as np

# Ensure proper console encoding on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_cache_decorator():
    try:
        import streamlit as st
        if hasattr(st, "runtime") and st.runtime.exists():
            return st.cache_data
    except Exception:
        pass
    return lambda f: f


DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "Algerian_forest_fires_dataset_UPDATE.csv")
if not os.path.exists(DATA_FILE_PATH):
    DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "Algerian_forest_fires_dataset_UPDATE.csv")


def load_and_clean_data(file_path: str = DATA_FILE_PATH) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")

    # Bejaia region partition (first 122 observations)
    df_bejaia = pd.read_csv(file_path, skiprows=1, nrows=122)
    df_bejaia.columns = df_bejaia.columns.str.strip()
    df_bejaia["Region"] = "Bejaia"

    # Sidi-Bel Abbes region partition (122 observations starting after second header)
    df_sidi = pd.read_csv(file_path, skiprows=126)
    df_sidi.columns = df_sidi.columns.str.strip()
    df_sidi["Region"] = "Sidi-Bel Abbes"

    df = pd.concat([df_bejaia, df_sidi], ignore_index=True)

    # Fix known UCI dataset delimiter anomaly at 14/07/2012 ('14.6 9' missing comma)
    mask_anomaly = (
        (df["day"].astype(str).str.strip() == "14") & 
        (df["month"].astype(str).str.strip() == "7") & 
        (df["Region"] == "Sidi-Bel Abbes")
    )
    if mask_anomaly.any():
        idx = df[mask_anomaly].index[0]
        df.at[idx, "DC"] = 14.6
        df.at[idx, "ISI"] = 9.0
        df.at[idx, "BUI"] = 12.5
        df.at[idx, "FWI"] = 10.4
        df.at[idx, "Classes"] = "fire"

    # Normalize class labels to binary target (1: fire, 0: not fire)
    df["Classes"] = df["Classes"].astype(str).str.strip().str.lower()
    df["Classes"] = df["Classes"].apply(lambda x: "fire" if "not" not in x and "fire" in x else "not fire")
    df["Fire_Label"] = (df["Classes"] == "fire").astype(int)

    numeric_cols = [
        "day", "month", "year", "Temperature", "RH", "Ws", 
        "Rain", "FFMC", "DMC", "DC", "ISI", "BUI", "FWI"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna().reset_index(drop=True)

    # Construct continuous timeline index
    df["Date"] = pd.to_datetime(
        df["year"].astype(int).astype(str) + "-" + 
        df["month"].astype(int).astype(str).str.zfill(2) + "-" + 
        df["day"].astype(int).astype(str).str.zfill(2)
    )
    
    month_names_vi = {6: "Tháng 6", 7: "Tháng 7", 8: "Tháng 8", 9: "Tháng 9"}
    df["Month_Name"] = df["month"].map(month_names_vi)

    return df


def get_feature_data(df: pd.DataFrame, feature_cols: list = None):
    from config import ALL_MODEL_FEATURES
    if feature_cols is None:
        feature_cols = ALL_MODEL_FEATURES
    return df[feature_cols].copy(), df["Fire_Label"].copy()


if __name__ == "__main__":
    data = load_and_clean_data()
    print("Dataset loaded successfully:", data.shape)
