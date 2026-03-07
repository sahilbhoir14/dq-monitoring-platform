# main.py — Full Week 2 pipeline
from scripts.ingestion      import load_retail_data, get_dataset_info
from scripts.profiling      import profile_dataset, print_profile
from scripts.quality_checks import run_all_checks, print_check_results
from scripts.scoring        import calculate_dq_score, print_scores
from scripts.report_export  import export_to_excel
import pandas as pd
from datetime import datetime

def log_score(scores):
    row  = pd.DataFrame([scores])
    path = "data/logs/dq_score_history.csv"
    try:
        hist = pd.read_csv(path)
        hist = pd.concat([hist, row], ignore_index=True)
    except FileNotFoundError:
        hist = row
    hist.to_csv(path, index=False)

def run_pipeline():
    print("\n" + "="*50)
    print("  DQ PIPELINE — RETAIL PRODUCT DATASET")
    print("="*50)

    df      = load_retail_data()
    info    = get_dataset_info(df)
    print(f"\n📥 Loaded : {info['total_rows']} rows × {info['total_columns']} cols")

    profile = profile_dataset(df)
    print(f"🔬 Profiled: {len(profile)} columns")

    results = run_all_checks(df)
    print_check_results(results)

    scores  = calculate_dq_score(df, profile, results)
    print_scores(scores)

    out = f"reports/dq_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    export_to_excel(profile, results, scores, out)

    log_score(scores)
    print("📝 Score history updated\n")
    print("✅ Pipeline Complete!\n")

if __name__ == "__main__":
    run_pipeline()