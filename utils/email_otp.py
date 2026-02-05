import smtplib
import random
from email.mime.text import MIMEText


# ⭐ Replace with your Gmail
SENDER_EMAIL = "YOUR_GMAIL@gmail.com"

# ⭐ Replace with Gmail App Password (NOT normal password)
APP_PASSWORD = "YOUR_APP_PASSWORD"


# -------- GENERATE OTP --------
def generate_otp():
    return str(random.randint(100000, 999999))


# -------- SEND EMAIL OTP --------
def send_email_otp(receiver_email, otp):

    subject = "AI Decision System OTP Verification"
    body = f"""
Hello,

Your OTP for AI Decision System verification is:

OTP: {otp}

Do not share this OTP with anyone.

Thank You
AI Decision System
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print("Email OTP Error:", e)
        return False
