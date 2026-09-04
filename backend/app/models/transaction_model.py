from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from app.core.database import Base

class TransactionRecord(Base):
    __tablename__ = "transactions"

    # Fixed: Changed primary_primary to primary_key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    merchant = Column(String)
    category = Column(String)
    location = Column(String)
    device_type = Column(String)
    
    # ML Scoring Outcomes
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False) # LOW, MEDIUM, HIGH
    is_flagged = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)