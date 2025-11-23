from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"
    transfer = "transfer"


# Максимально простые схемы без Field
class TransactionCreate(BaseModel):
    amount: float
    name: str
    description: Optional[str] = None
    date: Optional[date] = None
    type: TransactionType
    category_id: int


class TransactionResponse(BaseModel):
    id: int
    amount: float
    name: str
    description: Optional[str]
    date: Optional[date]
    type: TransactionType
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True
