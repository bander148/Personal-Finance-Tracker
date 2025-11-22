from unicodedata import category

from ..schemas.category import CategoryResponse,CategoryCreate
from sqlalchemy.orm import Session
from typing import List
from ..repositories.category_repository import CategoryRepository
from ..schemas.category import CategoryResponse, CategoryCreate
from fastapi import HTTPException, status

class CategoryService:

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_all_categories(self) -> List[CategoryResponse]:
        categories= self.repository.get_all()
        return [CategoryResponse.model_dump(cat) for cat in categories]

    def get_category_by_id(self, category_id: int) -> CategoryResponse:
        category = self.repository.get_by_id(category_id)
        if category:
            return CategoryResponse.model_dump(category)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Category with id {category_id} not found'
        )

    def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        existing_category = self.repository.get_by_name(category_data.name)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория '{category_data.name}' уже существует"
            )
        category = self.repository.create(category_data)
        return CategoryResponse.model_validate(category)