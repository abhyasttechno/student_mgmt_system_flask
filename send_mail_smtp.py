import smtplib
from email.mime.text import MIMEText
import secrets

from exchangelib import Credentials, Account, Message, DELEGATE

# Set up your credentials
email = 'sidaxn321@outlook.com'
password = 'Ilovesid@12'

credentials = Credentials(email, password)

# Create an account instance
account = Account(email, credentials=credentials, autodiscover=True, access_type=DELEGATE)

# Send an email
def send_reset_token_email(recipient_email):
    # Generate token
    token = generate_reset_token()

    m = Message(
        account=account,
        folder=account.sent,
        subject='Password Reset Request',
        body = f"""Dear User,

        You've requested a password reset for the Student Management Portal.
        Click the link below to reset your password:

        http://localhost:8080/reset_password/{token}

        If you didn't request this, please ignore this email.

        Best regards,
        Student Management Team
        """,
        to_recipients=[recipient_email]
    )
    m.send_and_save()
    return token

def generate_reset_token():
    """Generate a unique reset token."""
    return secrets.token_urlsafe(20)  # 20-byte token


if __name__ == '__main__':
    send_reset_token_email("manu.siddhartha289@gmail.com")
    print("Token sent:")
