# scripts/scheduler.py
import schedule
import time
from datetime import datetime

def run_pipeline():
    print(f"\n⏰ Scheduled run triggered at {datetime.now()}")
    # Import here to avoid circular imports
    from scripts.ingestion      import load_retail_data
    from scripts.profiling      import profile_dataset
    from scripts.quality_checks import run_all_checks
    from scripts.scoring        import calculate_dq_score, print_scores
    from scripts.report_export  import export_to_excel
    from scripts.alerting       import send_alert

    df      = load_retail_data()
    profile = profile_dataset(df)
    checks  = run_all_checks(df)
    scores  = calculate_dq_score(df, profile, checks)
    print_scores(scores)

    out = f"reports/dq_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    export_to_excel(profile, checks, scores, out)
    send_alert(scores, threshold=80)

    print("✅ Scheduled run complete!\n")

# ── Schedule Options (uncomment one) ─────────────────────
schedule.every().day.at("08:00").do(run_pipeline)   # Daily 8AM
# schedule.every(6).hours.do(run_pipeline)           # Every 6 hours
#schedule.every(1).minutes.do(run_pipeline)         # Every minute (for testing)

print("⏳ Scheduler running... Press Ctrl+C to stop")
print(f"   Next run: {schedule.next_run()}\n")

while True:
    schedule.run_pending()
    time.sleep(60)