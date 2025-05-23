from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_users(db: Session):
    result = db.execute(text(
        "SELECT id, username, email, is_admin FROM Users"
    )).mappings()
    return [dict(row) for row in result]

def get_by_id(db: Session, user_id: int):
    result = db.execute(
        text("SELECT id, username, email, is_admin FROM Users WHERE id = :id"),
        {"id": user_id}
    ).first()
    return dict(result) if result else None

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db.execute(
        text("""
            INSERT INTO Users (username, email, password_hash, is_admin, created_at)
            VALUES (:username, :email, :password_hash, :is_admin, :created_at)
        """),
        {
            "username": user.username,
            "email": user.email,
            "password_hash": hashed_password,
            "is_admin": user.is_admin,
            "created_at": datetime.utcnow().isoformat()
        }
    )
    db.commit()
    return {"message": "User created successfully"}

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    fields = []
    params = {"id": user_id}

    if user_data.username:
        fields.append("username = :username")
        params["username"] = user_data.username
    if user_data.email:
        fields.append("email = :email")
        params["email"] = user_data.email
    if user_data.password:
        fields.append("password_hash = :password_hash")
        params["password_hash"] = hash_password(user_data.password)
    if user_data.is_admin is not None:
        fields.append("is_admin = :is_admin")
        params["is_admin"] = user_data.is_admin

    if not fields:
        return {"message": "No data to update"}

    sql = f"UPDATE Users SET {', '.join(fields)} WHERE id = :id"
    db.execute(text(sql), params)
    db.commit()
    return {"message": "User updated successfully"}

def delete_user(db: Session, user_id: int):
    result = db.execute(
        text("DELETE FROM Users WHERE id = :id"),
        {"id": user_id}
    )
    db.commit()
    if result.rowcount:
        return {"message": "User deleted successfully"}
    else:
        return {"error": "User not found"}

def get_user_by_username(db: Session, username: str):
    result = db.execute(
        text("SELECT id, username, email, is_admin FROM Users WHERE username = :username"),
        {"username": username}
    ).first()
    return dict(result) if result else None

def get_user_by_email(db: Session, email: str):
    result = db.execute(
        text("SELECT id, username, email, is_admin FROM Users WHERE email = :email"),
        {"email": email}
    ).first()
    return dict(result) if result else None