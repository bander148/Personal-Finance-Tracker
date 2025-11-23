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
    amount: float = Field(..., description="Transaction amount", gt=0)
    name : str = Field(..., description="Transaction name")
    description : Optional[str] = Field(None, description="Transaction description",min_length=3,max_length=300)
    date : Optional[date] = Field(None, description="Transaction date")
    type : TransactionType = Field(..., description="Transaction type")
    category_id : int = Field(..., description="Transaction category id")
    created_at : datetime = Field(..., description="Transaction created at")


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    name: str = Field(...)
    description: Optional[str] = Field(None, min_length=3, max_length=300)
    date: Optional[date] = Field(default_factory=date.today)
    type: TransactionType = Field(...)
    category_id: int = Field(...)

class TransactionResponse(TransactionBase):
    id: int = Field(..., description="Transaction ID")
    category: CategoryResponse = Field(...)
    created_at: datetime = Field(..., description="Transaction created at")
    class Config:
        from_attributes = True


