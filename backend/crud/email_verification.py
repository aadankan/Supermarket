from models.user import User
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config

from models.email_verification import EmailVerification
from schemas.email_verification import EmailSchema

SECRET_KEY = config("JWT_SECRET")
ALGORITHM = "HS256"

conf = ConnectionConfig(
    MAIL_USERNAME=config("MAIL_USERNAME"),
    MAIL_PASSWORD=config("MAIL_PASSWORD"),
    MAIL_FROM=config("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

def generate_verification_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

async def send_verification(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = generate_verification_token(email)

    existing = db.query(EmailVerification).filter(EmailVerification.email == user.email).first()
    if existing:
        existing.token = token
        existing.is_verified = False
    else:
        new_entry = EmailVerification(email=user.email, token=token)
        db.add(new_entry)

    db.commit()

    link = f"http://localhost:8000/email-verification/verify-token?token={token}"
    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"Click here to verify your email: <a href='{link}'>{link}</a>",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)


def confirm_user_email(db: Session, token: str):
    email = verify_token(token)

    entry = db.query(EmailVerification).filter(EmailVerification.email == email).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Verification entry not found")
    if entry.is_verified:
        return entry.email

    entry.is_verified = True
    db.commit()
    return email

def is_email_verified(db: Session, email: str) -> bool:
    entry = db.query(EmailVerification).filter(EmailVerification.email == email).first()
    return entry.is_verified if entry else False
