
from sqlalchemy.orm import Session
from datetime import date
from ..schemas.transaction import TransactionCreate, TransactionResponse
from ..repositories.transaction_repository import TransactionRepository
from ..repositories.category_repository import CategoryRepository
from typing import List
from fastapi import HTTPException, status


class TransactionService:
    def __init__(self, db: Session):
        self.repository = TransactionRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_all_transactions(self) -> List[TransactionResponse]:
        transactions = self.repository.get_all()
        return [TransactionResponse.model_validate(trans) for trans in transactions]

    def get_transaction_by_id(self, id: int) -> TransactionResponse:
        transaction = self.repository.get_by_transaction_id(id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return TransactionResponse.model_validate(transaction)

    def create(self, transaction: TransactionCreate) -> TransactionResponse:
        # Проверяем существование категории
        category = self.category_repository.get_by_id(transaction.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {transaction.category_id} not found"
            )

        # Создаем транзакцию
        db_transaction = self.repository.create_transaction(transaction)
        return TransactionResponse.model_validate(db_transaction)