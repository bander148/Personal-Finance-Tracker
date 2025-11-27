from ..dependencies.auth import get_current_user
from ..schemas.category import CategoryCreate
from ..database import get_db
from ..services.category_service import CategoryService
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .auth import get_current_user
from ..models.user import User

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"]
)

@router.get("")
async def get_categories(user_data : User = Depends(get_current_user),db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_all_user_categories(user_data.id)

@router.get("/{category_id}")
async def get_categories_user(category_id:int,db: Session = Depends(get_db),user_data : User = Depends(get_current_user)):
    service = CategoryService(db)
    return service.get_user_category_by_id(category_id,user_data.id)

@router.post("/create")
async def create_category(data : CategoryCreate, db: Session = Depends(get_db),user_data : User = Depends(get_current_user)):
    service = CategoryService(db)
    return service.create_category(data,user_data.id)