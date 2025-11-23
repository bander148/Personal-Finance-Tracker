from typing import Optional
from pydantic import BaseModel
from enum import Enum


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: CategoryType
    parent_id: Optional[int] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type: CategoryType
    parent_id: Optional[int]

    class Config:
        from_attributes = True