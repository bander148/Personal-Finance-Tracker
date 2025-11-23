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
        if not transactions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No transactions found, create a new transaction first"
            )
        return [TransactionResponse.model_validate(trans) for trans in transactions]

    def get_transactions_by_category(self, category: str) -> List[TransactionResponse]:
        # Этот метод нужно пересмотреть - он ищет по имени категории, а не ID
        # Временно отключим его
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Method not implemented. Use get_transactions_by_ctg_id instead."
        )

    def get_transaction_by_id(self, id: int) -> TransactionResponse:
        transaction = self.repository.get_by_transaction_id(id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return TransactionResponse.model_validate(transaction)

    def get_transactions_by_ctg_id(self, category_id: int) -> List[TransactionResponse]:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        transactions = self.repository.get_by_category_id(category_id)
        return [TransactionResponse.model_validate(transaction) for transaction in transactions]

    def get_trans_by_date(self, date: date) -> List[TransactionResponse]:
        transactions = self.repository.get_by_date(date)
        if not transactions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No transactions found for this date"
            )
        return [TransactionResponse.model_validate(transaction) for transaction in transactions]

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