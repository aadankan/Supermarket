from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


# To verify the password, you can use the following function
# TODO: Implement a function to verify the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_users(db: Session):
    result = db.execute(text("SELECT id, name, email, is_admin FROM users")).mappings()
    return [dict(row) for row in result]


def get_by_id(db: Session, user_id: int):
    result = db.execute(
        text("SELECT id, name, email, is_admin FROM users WHERE id = :id"),
        {"id": user_id}
    ).first()
    return dict(result) if result else None

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db.execute(
        text("INSERT INTO users (name, email, password_hash) VALUES (:name, :email, :password)"),
        {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "is_admin": user.is_admin
        }
    )
    db.commit()
    return {"message": "User created successfully"}

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    fields = []
    params = {"id": user_id}

    if user_data.name:
        fields.append("name = :name")
        params["name"] = user_data.name
    if user_data.email:
        fields.append("email = :email")
        params["email"] = user_data.email
    if user_data.password:
        fields.append("password_hash = :password")
        params["password"] = user_data.password
    if user_data.is_admin is not None:
        fields.append("is_admin = :is_admin")
        params["is_admin"] = user_data.is_admin

    if not fields:
        return {"message": "No data to update"}

    sql = f"UPDATE users SET {', '.join(fields)} WHERE id = :id"
    db.execute(text(sql), params)
    db.commit()
    return {"message": "User updated successfully"}

def delete_user(db: Session, user_id: int):
    result = db.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
    db.commit()
    if result.rowcount:
        return {"message": "User deleted successfully"}
    else:
        return {"error": "User not found"}
