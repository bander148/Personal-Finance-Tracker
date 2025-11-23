from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas.category import CategoryCreate
from ..models.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == name).first()

    def get_all(self) -> List[Category]:
        return self.db.query(Category).all()

    def create(self, data: CategoryCreate) -> Category:
        category_db = Category(
            name=data.name,
            description=data.description,
            type=data.type.value,
            parent_id=data.parent_id
        )
        self.db.add(category_db)
        self.db.commit()
        self.db.refresh(category_db)
        return category_db