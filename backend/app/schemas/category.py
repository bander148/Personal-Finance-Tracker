from typing import Optional
from pydantic import BaseModel,Field, field_validator,ConfigDict
from enum import Enum


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class CategoryCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Category name"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Category description"
    )
    type: CategoryType = Field(..., description="Category type")
    parent_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="Parent category ID"
    )

    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Category name cannot be empty')
        return v.strip()
    user_id : int = Field(gt=0, description="User ID")


class CategoryResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    id: int = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")
    description: Optional[str] = Field(default=None, description="Category description")
    type: CategoryType = Field(..., description="Category type")
    parent_id: Optional[int] = Field(default=None, description="Parent category ID")
