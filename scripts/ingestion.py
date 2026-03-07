# scripts/ingestion.py
import pandas as pd
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

def load_retail_data(filepath="data/raw/synthetic_dataset.csv"):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath)
    logging.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df

def get_dataset_info(df):
    info = {
        "total_rows":    len(df),
        "total_columns": len(df.columns),
        "columns":       list(df.columns),
        "dtypes":        df.dtypes.astype(str).to_dict(),
        "null_summary":  df.isnull().sum().to_dict(),
        "memory_kb":     round(df.memory_usage(deep=True).sum() / 1024, 1)
    }
    return info

# Test it
if __name__ == "__main__":
    df   = load_retail_data()
    info = get_dataset_info(df)
    for k, v in info.items():
        print(f"{k}: {v}")