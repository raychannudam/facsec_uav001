from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
import os

conf = ConnectionConfig(
   MAIL_USERNAME=os.getenv("EMAIL_USER"),
   MAIL_PASSWORD=os.getenv("EMAIL_PASSWORD"),
   MAIL_FROM=os.getenv("EMAIL_FROM"),
   MAIL_PORT=os.getenv("MAIL_PORT", 587),
   MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
   MAIL_STARTTLS=True,
   MAIL_SSL_TLS=False
)

class MailService:
    @staticmethod
    async def send_email(email: str, code: str, subject: str = "Your Validation Code"):
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            body=f"Your validation code is: {code}",
            subtype="plain"
        )
        fm = FastMail(conf)
        await fm.send_message(message)