from datetime import date
from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from ..schemas.transaction import TransactionCreate
from typing import List, Optional

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Transaction]:
        return self.db.query(Transaction).all()

    def get_by_date(self, tr_date : date) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.date == tr_date).all()

    def get_by_category(self, category)-> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.category == category).all()

    def get_by_transaction_id(self, transaction_id : int) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        db_transaction = Transaction(**transaction.model_dump())
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction
    def get_transaction_by_category(self, category : str) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.category == category).all()