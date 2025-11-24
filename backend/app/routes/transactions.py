from sqlalchemy.orm import Session
from ..schemas.transaction import TransactionCreate
from ..services.transaction_service import TransactionService
from ..database import get_db
from fastapi import APIRouter, Depends,Query,HTTPException
from datetime import date
router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"]
)

@router.get("")
async def get_all_transactions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_all_transactions(skip=skip, limit=limit)

@router.get("/{id}")
async def get_transaction(id: int, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.get_transaction_by_id(id)

@router.get("/category/{category_id}")
async def get_transactions_by_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_transactions_by_category_id(category_id)

@router.get("/date/{transaction_date}")
async def get_transactions_by_date(
    transaction_date: date,
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_transactions_by_date(transaction_date)

@router.get("/type/{transaction_type}")
async def get_transactions_by_type(
    transaction_type: str,
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_transactions_by_type(transaction_type)

@router.post("")
async def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.create_transaction(data)
@router.delete("/{id}")
async def delete_transaction(id: int, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.delete_transaction(id)