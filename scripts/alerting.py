# scripts/alerting.py
import smtplib
from email.mime.text     import MIMEText
from email.mime.multipart import MIMEMultipart
import json

def load_email_config(path="config/email_config.json"):
    with open(path) as f:
        return json.load(f)

def send_alert(scores, threshold=80):
    score = scores["overall_score"]

    if score >= threshold:
        print(f"✅ DQ Score {score}% is above threshold. No alert sent.")
        return

    cfg = load_email_config()
    msg = MIMEMultipart()
    msg["From"]    = cfg["sender"]
    msg["To"]      = cfg["receiver"]
    msg["Subject"] = f"⚠️ DQ Alert — Score Dropped to {score}%"

    body = f"""
    DATA QUALITY ALERT
    ══════════════════
    Overall Score : {score}%   (Threshold: {threshold}%)
    Completeness  : {scores['completeness']}%
    Validity      : {scores['validity']}%
    Uniqueness    : {scores['uniqueness']}%
    Grade         : {scores['grade']}

    ⚠️ Immediate review of the Retail Product dataset required.
    """
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(cfg["sender"], cfg["password"])
        server.send_message(msg)

    print(f"📧 Alert email sent! Score {score}% is below threshold {threshold}%")