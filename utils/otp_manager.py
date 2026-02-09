import random
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# =====================================
# OTP GENERATION
# =====================================
def generate_otp():
    return str(random.randint(100000, 999999))


# =====================================
# SEND OTP VIA EMAIL
# =====================================
def send_email_otp(to_email, otp):
    try:
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")

        if not sender_email or not sender_password:
            print("Email credentials not found in .env")
            return False

        msg = MIMEText(f"Your OTP is: {otp}")
        msg["Subject"] = "Your OTP Verification Code"
        msg["From"] = sender_email
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print("Email OTP Error:", e)
        return False


# =====================================
# DUMMY MOBILE OTP (DISABLED FOR NOW)
# =====================================
def send_mobile_otp(mobile, otp):
    # Not implemented (future feature)
    print(f"[DEBUG] OTP {otp} sent to mobile {mobile}")
    return True
