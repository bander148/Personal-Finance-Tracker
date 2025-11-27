from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate
from passlib.context import CryptContext
from ..models.user import User
pwd_context = CryptContext(schemes = ['sha256_crypt'], deprecated = 'auto',bcrypt__max_password_length=72)

class UserRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_by_email(self, email : str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, id : int) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()

    def create_user(self, user_data: UserCreate) -> User:
        if self.get_by_email(user_data.email):
            raise ValueError("User with this email already exists")
        password = user_data.password
        if len(password.encode('utf-8')) > 72:
            password = password[:50]
        hashed_password = pwd_context.hash(password)
        db_user = User(
            email = user_data.email,
            hashed_password= hashed_password,
            name = user_data.name,
            created_at = datetime.utcnow(),
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate(self, email : str, password : str) -> Optional[User]:
        user = self.get_by_email(email)
        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
        return user
