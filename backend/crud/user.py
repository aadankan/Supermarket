from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from datetime import datetime
from models.user import User as UserModel
from crud.address import create_address
from crud.address import create_address, update_address, get_default_address
from schemas.address import AddressCreate, AddressUpdate
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
    ).mappings().first()
    return dict(result) if result else None

def create_user(db: Session, user: UserCreate):
    existing = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = UserModel(email=user.email, email_confirmed=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    fields = []
    params = {"id": user_id}

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # Aktualizacja pól użytkownika
    if user_data.username:
        fields.append("username = :username")
        params["username"] = user_data.username
    if user_data.password:
        fields.append("password_hash = :password_hash")
        params["password_hash"] = hash_password(user_data.password)
    if user_data.firstName:
        fields.append("first_name = :firstName")
        params["firstName"] = user_data.firstName
    if user_data.lastName:
        fields.append("last_name = :lastName")
        params["lastName"] = user_data.lastName
    if user_data.phoneNumber:
        fields.append("phone_number = :phoneNumber")
        params["phoneNumber"] = user_data.phoneNumber

    # Adres — sprawdź czy istnieje domyślny
    existing_address = get_default_address(db, user_id)

    if any([user_data.street, user_data.city, user_data.postalCode, user_data.country]):
        if existing_address:
            # Aktualizacja istniejącego adresu
            address_update = AddressUpdate(
                street=user_data.street or existing_address["street"],
                city=user_data.city or existing_address["city"],
                postal_code=user_data.postalCode or existing_address["postal_code"],
                country=user_data.country or existing_address["country"]
            )
            update_address(db, existing_address["id"], address_update)
        else:
            # Tworzenie nowego adresu domyślnego
            address_create = AddressCreate(
                user_id=user_id,
                street=user_data.street or "",
                city=user_data.city or "",
                postal_code=user_data.postalCode or "",
                country=user_data.country or "",
                is_default=True,
                created_at=datetime.utcnow().isoformat()
            )
            new_address = create_address(db, address_create)
            # Aktualizuj default_address_id w Users
            db.execute(
                text("UPDATE Users SET default_address_id = :address_id WHERE id = :user_id"),
                {"address_id": new_address["address_id"], "user_id": user_id}
            )

    # Jeśli były zmiany użytkownika — wykonaj zapytanie SQL
    if fields:
        sql = f"UPDATE Users SET {', '.join(fields)} WHERE id = :id"
        db.execute(text(sql), params)

    db.commit()
    return {"message": "User and address updated successfully"}


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
    ).mappings().first()
    return dict(result) if result else None