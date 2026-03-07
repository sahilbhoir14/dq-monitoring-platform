# scripts/scoring.py
from datetime import datetime

def calculate_dq_score(df, profile, check_results):

    # 1. Completeness
    total_cells = df.shape[0] * df.shape[1]
    null_cells  = sum(v["null_count"] for v in profile.values())
    completeness = round((1 - null_cells / total_cells) * 100, 2)

    # 2. Validity
    passed   = sum(1 for r in check_results.values() if r["passed"])
    validity = round(passed / len(check_results) * 100, 2)

    # 3. Uniqueness (based on Product_ID)
    if "Product_ID" in df.columns:
        dups       = df["Product_ID"].duplicated().sum()
        uniqueness = round((1 - dups / len(df)) * 100, 2)
    else:
        uniqueness = 100.0

    # 4. Consistency (no mixed types per column)
    consistent  = sum(1 for col in df.columns if df[col].apply(type).nunique() == 1)
    consistency = round(consistent / len(df.columns) * 100, 2)

    # Overall weighted score
    overall = round(
        0.30 * completeness +
        0.25 * validity     +
        0.25 * uniqueness   +
        0.20 * consistency,
        2
    )

    scores = {
        "run_datetime":  datetime.now().strftime("%Y-%m-%d %H:%M"),
        "completeness":  completeness,
        "validity":      validity,
        "uniqueness":    uniqueness,
        "consistency":   consistency,
        "overall_score": overall,
        "grade":         get_grade(overall)
    }
    return scores

def get_grade(score):
    if score >= 90: return "A — Excellent"
    if score >= 75: return "B — Good"
    if score >= 60: return "C — Needs Work"
    return              "D — Critical"

def print_scores(scores):
    print(f"\n{'='*40}")
    print(f"  DQ SCORECARD")
    print(f"{'='*40}")
    print(f"  Completeness : {scores['completeness']}%")
    print(f"  Validity     : {scores['validity']}%")
    print(f"  Uniqueness   : {scores['uniqueness']}%")
    print(f"  Consistency  : {scores['consistency']}%")
    print(f"{'─'*40}")
    print(f"  OVERALL SCORE: {scores['overall_score']}%")
    print(f"  GRADE        : {scores['grade']}")
    print(f"{'='*40}\n")