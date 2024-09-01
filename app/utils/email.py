
def send_verification_email(email: str, token: str):
    verification_url = f"http://localhost:8000/verify?token={token}"
    subject = "Verify Your Email"
    body = f"Please click the following link to verify your email: {verification_url}"
    print(f"Simulated sending email to {email}:")
    print(f"Subject: {subject}")
    print(f"Body: {body}")