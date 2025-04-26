import pandas as pd
import smtplib
from email.message import EmailMessage

# Constants
RESULT_FILE = '../data/combined_detection_results_large.csv'
USER_EMAIL = 'bobtestemail30@gmail.com'
SYSTEM_EMAIL = 'phishingnotifier@gmail.com'
APP_PASSWORD = 'goli mhiy mppl zsvy'

def send_email_notification(sender, subject):
    msg = EmailMessage()
    msg['Subject'] = "Phishing Alert - Suspicious Email Detected"
    msg['From'] = SYSTEM_EMAIL
    msg['To'] = USER_EMAIL

    msg.set_content(f"""
The system detected a potential phishing email sent to you.

 Sender: {sender}
 Subject: {subject}

Please be careful and do not click on any links in the email.
    """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SYSTEM_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
            print("Notification emails have been sent")
    except Exception as e:
        print("Email was not sent:", e)

def notify_if_phishing():
    df = pd.read_csv(RESULT_FILE)

    match = df[(df['receiver'] == USER_EMAIL) & (df['Result'] == 'Phishing')]

    if not match.empty:
        row = match.iloc[0]
        send_email_notification(row['sender'], row['subject'])
    else:
        print("No phishing emails were detected for", USER_EMAIL)

if __name__ == "__main__":
    notify_if_phishing()