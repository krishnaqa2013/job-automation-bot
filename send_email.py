import os
import glob
import smtplib
from email.message import EmailMessage

EMAIL = os.environ["EMAIL_USER"]
PASSWORD = os.environ["EMAIL_PASS"]


def latest_file():
    files = sorted(glob.glob("QA_Jobs_*.xlsx"))
    return files[-1] if files else None


def send_email():
    file_path = latest_file()

    if not file_path:
        print("❌ No Excel file found")
        return

    msg = EmailMessage()

    msg["Subject"] = "📊 Daily QA Automation Jobs Report"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    msg.set_content("""
Daily QA Automation job report attached.

Includes:
- Senior QA roles
- Lead / Architect / SDET openings
- Hybrid Hyderabad + Remote India jobs
- Last 3 days postings
""")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=file_path
        )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email failed:", str(e))


if __name__ == "__main__":
    send_email()
