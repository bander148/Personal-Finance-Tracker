from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from .category import CategoryResponse


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"
    transfer = "transfer"


# Упрощенные схемы без Field в аннотациях
class TransactionBase(BaseModel):
    amount: float
    name: str
    description: Optional[str] = None
    date: Optional[date] = None
    type: TransactionType
    category_id: int
    created_at: datetime


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount")
    name: str = Field(..., min_length=1, description="Transaction name")
    description: Optional[str] = Field(None, min_length=3, max_length=300, description="Transaction description")
    date: Optional[date] = Field(default_factory=date.today, description="Transaction date")
    type: TransactionType = Field(..., description="Transaction type")
    category_id: int = Field(..., description="Transaction category ID")


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

