from sqlalchemy.orm import Session
from typing import List
from ..repositories.category_repository import CategoryRepository
from ..schemas.category import CategoryResponse, CategoryCreate
from fastapi import HTTPException, status

class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_all_user_categories(self,user_id : int) -> List[CategoryResponse]:
        categories = self.repository.get_all_users_category(user_id)
        return [CategoryResponse.model_validate(cat) for cat in categories]

    def get_user_category_by_id(self, category_id: int,user_id:int) -> CategoryResponse:
        category = self.repository.get_user_category_by_id(category_id,user_id)
        if category:
            return CategoryResponse.model_validate(category)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Category with id {category_id} not found'
        )

    def create_category(self, category_data: CategoryCreate,user_id : int) -> CategoryResponse:
        existing_category = self.repository.get_user_cat_by_name_cat(category_data.name, user_id)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category '{category_data.name}' already exists"
            )
        if category_data.parent_id:
            parent = self.repository.get_system_category_by_id(category_data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parent category with id {category_data.parent_id} not found"
                )
        category = self.repository.create(category_data,user_id)
        return CategoryResponse.model_validate(category)