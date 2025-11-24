from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date
from sqlalchemy.orm import relationship
from ..database import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False, index=True)
    description = Column(String)
    created_at = Column(DateTime, nullable=False, index=True)
    date = Column(Date, index=True)
    type = Column(String, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    category = relationship("Category", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    def __repr__(self):
        return f"<Transaction(id={self.id}, name='{self.name}', amount={self.amount})>"