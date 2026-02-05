import random
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

# =====================================
# LOAD ENV VARIABLES
# =====================================
load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASS")


# =====================================
# ⭐ GENERATE OTP
# =====================================
def generate_otp():
    return str(random.randint(100000, 999999))


# =====================================
# ⭐ SEND EMAIL OTP (REAL)
# =====================================
def send_email_otp(receiver_email, otp):

    subject = "AI Decision System OTP Verification"

    body = f"""
Hello,

Your OTP for verification is:

OTP: {otp}

⚠️ This OTP will expire in 5 minutes.
Do not share this OTP with anyone.

Thank You,
AI Decision System
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print("❌ Email OTP Error:", e)
        return False


# =====================================
# ⭐ MOBILE OTP SIMULATION
# =====================================
def send_mobile_otp(mobile, otp):

    # Simulation Only (For College Project)
    print(f"[SIMULATION] Mobile OTP for {mobile}: {otp}")

    return True
