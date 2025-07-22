import smtplib
from email.message import EmailMessage

def send_email_alert(subject, body):
    sender = "your_email@gmail.com"
    password = "your_app_password"
    receiver = "ravindranaik7672@gmail.com"  # Replace with your actual email

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
            print("Email alert sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)
