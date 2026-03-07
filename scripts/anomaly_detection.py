# scripts/anomaly_detection.py
import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df, numeric_cols=None, contamination=0.05):
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=["int64","float64"]).columns.tolist()

    clean = df[numeric_cols].dropna()
    model = IsolationForest(contamination=contamination, random_state=42)
    preds = model.fit_predict(clean)

    df = df.copy()
    df["anomaly_flag"]  = 0
    df.loc[clean.index, "anomaly_flag"] = preds
    df["is_anomaly"]    = df["anomaly_flag"] == -1

    total    = len(df)
    anomalies= int(df["is_anomaly"].sum())

    print(f"🔍 Anomaly Detection Complete")
    print(f"   Total rows    : {total}")
    print(f"   Anomalies found: {anomalies} ({round(anomalies/total*100,1)}%)")

    return df, anomalies

if __name__ == "__main__":
    from ingestion import load_retail_data
    df, count = detect_anomalies(load_retail_data())
    print(df[df["is_anomaly"] == True].head())