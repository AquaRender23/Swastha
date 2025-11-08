import smtplib
from email.message import EmailMessage

EMAIL = 'your_gmail_address@gmail.com'        # Replace with your Gmail address
PASSWORD = 'your_generated_app_password'      # Replace with your Google App Password

msg = EmailMessage()
msg['Subject'] = "Test Email from Flask App"
msg['From'] = EMAIL
msg['To'] = EMAIL  # send test email to yourself
msg.set_content("This is a test email to verify SMTP setup.")

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)
    print("SMTP test email sent successfully!")
except Exception as e:
    print("SMTP test failed:", e)
