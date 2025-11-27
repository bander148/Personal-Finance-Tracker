from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas.category import CategoryCreate
from ..models.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, cat_id: int,user_id:int) -> Optional[Category]:
        return self.db.query(Category).filter(
        Category.id == cat_id,or_(
                Category.user_id == user_id,
                Category.user_id.is_(None))
        ).first()

    def get_by_name(self, name: str, user_id:int) -> Optional[Category]:
        return self.db.query(Category).filter(
            Category.name == name, or_(
                Category.user_id == user_id,
                Category.user_id.is_(None))
        ).first()

    def create(self, data: CategoryCreate, user_id  : int = None) -> Category:
        category_db = Category(
            name=data.name,
            description=data.description,
            type=data.type.value,
            parent_id=data.parent_id,
            user_id=user_id
        )
        self.db.add(category_db)
        self.db.commit()
        self.db.refresh(category_db)
        return category_db

    def get_all_users_category(self, user_id : int) -> List[Category]:
        return self.db.query(Category).filter(or_(Category.user_id == user_id,Category.user_id.is_(None))).all()


