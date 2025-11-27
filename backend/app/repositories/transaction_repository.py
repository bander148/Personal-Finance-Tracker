from datetime import date
from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from ..schemas.transaction import TransactionCreate, TransactionResponse
from typing import List, Optional
from datetime import datetime

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self,id: int,skip: int = 0, limit: int = 100) -> List[TransactionResponse]:
        return self.db.query(Transaction).filter(Transaction.user_id == id).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Transaction]:
        return self.db.query(Transaction).offset(skip).limit(limit).all()

    def get_by_date(self, tr_date: date) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.date == tr_date).all()

    def get_by_date_range(self, start_date: date, end_date: date) -> List[Transaction]:
        return self.db.query(Transaction).filter(
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).all()

    def get_by_category_id(self, category_id: int) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.category_id == category_id).all()

    def get_by_transaction_id_and_user(self, transaction_id: int,user_id : int) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id,Transaction.user.id == user_id).first()

    def get_by_type(self, transaction_type: str) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.type == transaction_type).all()

    def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        transaction_data = transaction.model_dump()
        if 'created_at' not in transaction_data:
            transaction_data['created_at'] = date.today()
        db_transaction = Transaction(**transaction_data)
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    def delete_transaction(self, transaction_id: int,user_id : int) -> bool:
        db_transaction = self.get_by_transaction_id_and_user(transaction_id,user_id)
        if  not db_transaction:
            return False
        self.db.delete(db_transaction)
        self.db.commit()
        return True