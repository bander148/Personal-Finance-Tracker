from ..schemas.category import CategoryCreate
from ..database import get_db
from ..services.category_service import CategoryService
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/api/categories",
    tags=["categories"]
)

@router.get("")
async def get_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_all_categories()

@router.get("/{category_id}")
async def get_category(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_category_by_id(category_id)

@router.post("/create")
async def create_category(data : CategoryCreate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create_category(data)