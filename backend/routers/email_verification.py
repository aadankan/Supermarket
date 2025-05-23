from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from schemas.email_verification import EmailSchema, TokenSchema
from crud import email_verification as crud_ver
from models.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send-verification")
async def send_verification(data: EmailSchema, db: Session = Depends(get_db)):
    await crud_ver.send_verification(data.email, db)
    return {"message": "Verification email sent"}

@router.get("/verify-token")
def verify_token(token: str = Query(...), db: Session = Depends(get_db)):
    email = crud_ver.confirm_user_email(db, token)
    return {"message": "Email verified", "email": email}

@router.post("/check-email-confirmed")
def check_email_confirmed(data: EmailSchema, db: Session = Depends(get_db)):
    verified = crud_ver.is_email_verified(db, data.email)
    return {"emailConfirmed": verified}

@router.post("/resend-verification")
async def resend_verification(data: EmailSchema, db: Session = Depends(get_db)):
    await crud_ver.send_verification_email(data.email, db)
    return {"message": "Verification email resent"}
