from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional

from backend.app.schemas.category import CategoryResponse


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"
    transfer = "transfer"
class TransactionBase(BaseModel):
    amount: float
    name: str
    description: Optional[str] = None
    date: Optional[date] = None
    type: TransactionType
    category_id: int
    created_at: datetime

class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    name: str = Field(...)
    description: Optional[str] = Field(None, min_length=3, max_length=300)
    date: Optional[date] = Field(default_factory=date.today)
    type: TransactionType = Field(...)
    category_id: int = Field(...)

class TransactionResponse(BaseModel):
    id: int
    amount: float
    name: str
    description: Optional[str]
    date: Optional[date]
    type: TransactionType
    category_id: int
    created_at: datetime
    category: CategoryResponse
    class Config:
        from_attributes = True


