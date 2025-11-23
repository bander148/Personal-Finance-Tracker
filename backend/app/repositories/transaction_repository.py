from datetime import date
from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from ..schemas.transaction import TransactionCreate
from typing import List, Optional
from datetime import datetime

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Transaction]:
        return self.db.query(Transaction).all()

    def get_by_date(self, tr_date: date) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.date == tr_date).all()

    def get_by_category_id(self, category_id: int) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.category_id == category_id).all()

    def get_by_transaction_id(self, transaction_id: int) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        # Простое создание без сложных преобразований
        db_transaction = Transaction(
            name=transaction.name,
            amount=transaction.amount,
            description=transaction.description,
            date=transaction.date,
            type=transaction.type.value,
            category_id=transaction.category_id,
            created_at=datetime.now()  # Автоматически устанавливаем текущее время
        )
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction