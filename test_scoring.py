from scripts.ingestion import load_retail_data
from scripts.profiling import profile_dataset
from scripts.quality_checks import run_all_checks
from scripts.scoring import calculate_dq_score, print_scores

df = load_retail_data()
profile = profile_dataset(df)
checks = run_all_checks(df)
scores = calculate_dq_score(df, profile, checks)
print_scores(scores)