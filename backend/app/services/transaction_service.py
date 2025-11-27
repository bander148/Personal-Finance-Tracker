
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

    def get_all_transactions(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TransactionResponse]:
        transactions = self.repository.get_by_user_id(skip=skip, limit=limit)
        return [TransactionResponse.model_validate(trans) for trans in transactions]

    def get_transaction_by_id(self, transaction_id: int,user_id : int) -> TransactionResponse:
        transaction = self.repository.get_by_transaction_id_and_user(transaction_id,user_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return TransactionResponse.model_validate(transaction)

    def get_transactions_by_date(self, transaction_date: date) -> List[TransactionResponse]:
        transactions = self.repository.get_by_date(transaction_date)
        return [TransactionResponse.model_validate(trans) for trans in transactions]

    def get_transactions_by_category_id(self, category_id: int) -> List[TransactionResponse]:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )

        transactions = self.repository.get_by_category_id(category_id)
        return [TransactionResponse.model_validate(trans) for trans in transactions]

    def get_transactions_by_date_range(
            self,
            start_date: date,
            end_date: date
    ) -> List[TransactionResponse]:
        transactions = self.repository.get_by_date_range(start_date, end_date)
        return [TransactionResponse.model_validate(trans) for trans in transactions]

    def get_transactions_by_type(self, transaction_type: str) -> List[TransactionResponse]:
        transactions = self.repository.get_by_type(transaction_type)
        return [TransactionResponse.model_validate(trans) for trans in transactions]

    def create_transaction(self, transaction: TransactionCreate,user_id: int) -> TransactionResponse:
        category = self.category_repository.get_by_id(transaction.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {transaction.category_id} not found"
            )
        transaction_data = transaction.model_dump()
        transaction_data['user_id'] = user_id
        db_transaction = self.repository.create_transaction(transaction)
        return TransactionResponse.model_validate(db_transaction)

    def delete_transaction(self, transaction_id: int,user_id: int) -> dict:
        success = self.repository.delete_transaction(transaction_id,user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return {"message": "Transaction deleted successfully"}