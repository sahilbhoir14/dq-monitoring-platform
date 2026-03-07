# scripts/profiling.py
import pandas as pd
import numpy as np

def detect_outliers(series):
    """IQR method to count outliers"""
    series = series.dropna()
    Q1  = series.quantile(0.25)
    Q3  = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return int(((series < lower) | (series > upper)).sum())

def profile_dataset(df):
    profile = {}

    for col in df.columns:
        col_profile = {
            "null_count":      int(df[col].isnull().sum()),
            "null_pct":        round(df[col].isnull().mean() * 100, 2),
            "unique_values":   int(df[col].nunique()),
            "duplicate_count": int(df[col].duplicated().sum()),
            "data_type":       str(df[col].dtype),
            "sample_values":   df[col].dropna().head(3).tolist()
        }

        if df[col].dtype in ['int64', 'float64']:
            col_profile.update({
                "min":           float(df[col].min()),
                "max":           float(df[col].max()),
                "mean":          round(float(df[col].mean()), 2),
                "median":        float(df[col].median()),
                "std_dev":       round(float(df[col].std()), 2),
                "outlier_count": detect_outliers(df[col])
            })

        elif df[col].dtype == 'object':
            col_profile.update({
                "most_common":   df[col].mode()[0] if not df[col].mode().empty else None,
                "empty_strings": int((df[col] == "").sum())
            })

        profile[col] = col_profile

    return profile

def print_profile(profile):
    print(f"\n{'='*60}")
    print(f"  DATA PROFILING REPORT — {len(profile)} columns")
    print(f"{'='*60}")
    for col, stats in profile.items():
        print(f"\n📌 {col}")
        for k, v in stats.items():
            print(f"   {k:20s}: {v}")

if __name__ == "__main__":
    from ingestion import load_retail_data
    df      = load_retail_data()
    profile = profile_dataset(df)
    print_profile(profile)