import os
import glob
import smtplib
from email.message import EmailMessage

def get_latest_file():
    files = sorted(glob.glob("QA_Jobs_*.xlsx"))
    return files[-1] if files else None

def send_email():
    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]
    receiver = sender  # sending to yourself

    file_path = get_latest_file()

    if not file_path:
        print("❌ No Excel file found to send.")
        return

    msg = EmailMessage()
    msg["Subject"] = "📊 Daily QA Jobs Report"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Attached is your latest QA jobs report.")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=file_path
        )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
            print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Email sending failed:", e)

if __name__ == "__main__":
    send_email()