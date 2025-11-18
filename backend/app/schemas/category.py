from typing import Optional

from pydantic import AnyUrl, BaseModel, Field
from enum import Enum

class CategoryType(str,Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class CategoryBase(BaseModel):
    name: str = Field(..., description = "Category name" , min_length=3, max_length=200)
    description : Optional[str] = Field(None, description = "Category description" )
    icon_url: Optional[AnyUrl] = Field(None, description = "Category icon url")
    type: CategoryType = Field(..., description = "Category type")
    parent_id: Optional[int] = Field(None, description="Parent category ID")



class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id : int = Field(...,description='Unique category identifier')
    class Config:
        from_attributes = True