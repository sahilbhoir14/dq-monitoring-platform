# scripts/quality_checks.py
import pandas as pd
import json

def check_nulls(df, columns):
    results = {}
    for col in columns:
        if col not in df.columns:
            continue
        n = int(df[col].isnull().sum())
        results[f"null_{col}"] = {
            "column": col, "rule": "No Nulls",
            "failed_count": n,
            "passed": n == 0,
            "status": "✅ PASS" if n == 0 else "❌ FAIL"
        }
    return results

def check_duplicates(df, column):
    if column not in df.columns:
        return {}
    d = int(df[column].duplicated().sum())
    return {f"dup_{column}": {
        "column": column, "rule": "No Duplicates",
        "failed_count": d,
        "passed": d == 0,
        "status": "✅ PASS" if d == 0 else "❌ FAIL"
    }}

def check_value_range(df, column, min_val, max_val):
    if column not in df.columns:
        return {}
    v = int(((df[column] < min_val) | (df[column] > max_val)).sum())
    return {f"range_{column}": {
        "column": column, "rule": f"Range [{min_val}–{max_val}]",
        "failed_count": v,
        "passed": v == 0,
        "status": "✅ PASS" if v == 0 else "❌ FAIL"
    }}

def check_no_negatives(df, columns):
    results = {}
    for col in columns:
        if col not in df.columns:
            continue
        n = int((df[col] < 0).sum())
        results[f"neg_{col}"] = {
            "column": col, "rule": "No Negatives",
            "failed_count": n,
            "passed": n == 0,
            "status": "✅ PASS" if n == 0 else "❌ FAIL"
        }
    return results

def check_date_format(df, column, fmt):
    if column not in df.columns:
        return {}
    def bad(v):
        try: pd.to_datetime(v, format=fmt); return False
        except: return True
    n = int(df[column].dropna().apply(bad).sum())
    return {f"date_{column}": {
        "column": column, "rule": f"Date Format {fmt}",
        "failed_count": n,
        "passed": n == 0,
        "status": "✅ PASS" if n == 0 else "❌ FAIL"
    }}

def run_all_checks(df, config_path="config/rules_config.json"):
    with open(config_path) as f:
        config = json.load(f)

    all_results = {}

    for rule in config["rules"]:
        r = rule["rule"]

        if r == "no_nulls":
            all_results.update(check_nulls(df, rule["columns"]))

        elif r == "no_duplicates":
            all_results.update(check_duplicates(df, rule["column"]))

        elif r == "value_range":
            all_results.update(check_value_range(
                df, rule["column"], rule["min"], rule["max"]))

        elif r == "no_negatives":
            all_results.update(check_no_negatives(df, rule["columns"]))

        elif r == "date_format":
            all_results.update(check_date_format(
                df, rule["column"], rule["format"]))

    return all_results

def print_check_results(results):
    print(f"\n{'='*55}")
    print(f"  QUALITY CHECK RESULTS — {len(results)} checks")
    print(f"{'='*55}")
    passed = sum(1 for r in results.values() if r["passed"])
    print(f"  ✅ Passed: {passed}  |  ❌ Failed: {len(results)-passed}\n")
    for key, r in results.items():
        print(f"  {r['status']}  {r['column']:20s}  {r['rule']:25s}  Failed: {r['failed_count']}")

if __name__ == "__main__":
    from ingestion import load_retail_data
    df = load_retail_data()
    results = run_all_checks(df)
    print_check_results(results)