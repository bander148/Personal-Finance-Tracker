
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index=True,unique=True,nullable=False,gt=0)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False,index=True)
    created_at = Column(DateTime, nullable=False)
    name = Column(String(100), nullable=False, index=True,default="User")
    transactions = relationship("Transaction", back_populates="user")