from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional
from ..schemas.category import CategoryResponse

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"
    transfer = "transfer"



class TransactionCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    amount: float = Field(..., gt=0, description="transaction amount")
    name: str = Field(..., min_length=1, max_length=100, description="Transaction name")
    description: Optional[str] = None
    date: str = Field(default=None, description="Transaction date")
    type: TransactionType = Field(..., description="Transaction type")
    category_id: int = Field(..., gt=0, description="Transaction category ID")


class TransactionResponse(BaseModel):
    id: int = Field(..., description="Transaction ID")
    amount: float = Field(..., description="Transaction amount")
    name: str = Field(..., description="Transaction name")
    description: Optional[str] = Field(default=None, description="Transaction description")
    date: Optional[date] = None
    type: TransactionType = Field(..., description="Transaction type")
    category_id: int = Field(..., description="Transaction category ID")
    created_at: datetime = Field(..., description="Transaction created at")
    category: CategoryResponse = Field(..., description="Transaction category")

    class Config:
        from_attributes = True
