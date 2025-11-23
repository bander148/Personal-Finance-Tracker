from sqlalchemy.orm import Session
from typing import List,Optional
from ..schemas.category import CategoryCreate
from ..models.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == name).first()

    def get_all(self, limit : int = 100, skip : int = 0 , sorted_by : str = "id" , sort_order : str = "asc") -> List[Category]:
        if hasattr(Category, sorted_by):
            if sort_order == "asc":
                return self.db.query(Category).offset(skip).limit(limit).order_by(getattr(Category,sorted_by).asc()).all()
            elif sort_order == "desc":
                return self.db.query(Category).offset(skip).limit(limit).order_by(getattr(Category, sorted_by).desc()).all()
            else :
                raise ValueError("Invalid sort order")
        else :
            raise ValueError(f"Field '{sorted_by}' does not exist in Category model. Available fields: id, name")
    def create(self, data: CategoryCreate) -> Category:
        category_db = Category(
            name=data.name,
            description=data.description,
            icon_url=str(data.icon_url) if data.icon_url else None,
            type=data.type.value,
            parent_id=data.parent_id
        )
        self.db.add(category_db)
        self.db.commit()
        self.db.refresh(category_db)
        return category_db