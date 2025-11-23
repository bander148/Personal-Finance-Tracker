from sqlalchemy.orm import Session
from ..repositories.transaction_repository import TransactionRepository
from ..schemas.transaction import TransactionResponse,TransactionCreate
from ..services.transaction_service import TransactionService
from ...database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.get("")
async def get_all_categories(db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.get_all_transactions()

@router.get("/{id}")
async def get_transaction(id: int, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.get_transaction_by_id(id)

@router.post("/create")
async def create_transaction(data : TransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.create(data)

