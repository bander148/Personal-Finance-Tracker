from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)
    type = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    transactions = relationship("Transaction", back_populates="category")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"