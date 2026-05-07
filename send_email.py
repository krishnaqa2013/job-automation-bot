import os
import glob
import smtplib
from email.message import EmailMessage

EMAIL = os.environ["EMAIL_USER"]
PASSWORD = os.environ["EMAIL_PASS"]

files = glob.glob("QA_Jobs_*.xlsx")

print("Found files:", files)

if not files:
    print("❌ No Excel file found")
    exit()

latest_file = sorted(files)[-1]

msg = EmailMessage()

msg["Subject"] = "QA Jobs Report"
msg["From"] = EMAIL
msg["To"] = EMAIL

msg.set_content("Attached QA jobs report.")

with open(latest_file, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="application",
        subtype="octet-stream",
        filename=latest_file
    )

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

    print("✅ Email sent successfully")

except Exception as e:
    print("❌ Email failed")
    print(e)
