import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
import uvicorn

from app.services.inference import inference_engine
from app.services.websocket_manager import ws_manager
from app.services.alert_service import alert_engine
from app.core.database import engine, Base, get_db
from app.models.transaction_model import TransactionRecord

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real-Time AI Fraud Detection Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransactionSchema(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float
    timestamp: str
    merchant: str
    category: str
    location: str
    device_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_id": "TXN_9876543",
                "customer_id": "CUST_00123",
                "amount": 1250.50,
                "timestamp": "2026-09-04 12:00:00",
                "merchant": "Crypto Exchange",
                "category": "electronics",
                "location": "Tokyo, JP",
                "device_type": "desktop"
            }
        }
    )

@app.get("/")
def health_check():
    return {"status": "online", "database": "connected"}

@app.post("/api/v1/predict")
async def analyze_transaction(
    txn: TransactionSchema, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    try:
        payload = txn.model_dump()
        result = inference_engine.predict(payload)
        full_analysis = {**payload, **result}
        
        db_record = TransactionRecord(
            transaction_id=result["transaction_id"],
            customer_id=result["customer_id"],
            amount=result["amount"],
            merchant=payload["merchant"],
            category=payload["category"],
            location=payload["location"],
            device_type=payload["device_type"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            is_flagged=result["is_flagged"]
        )
        db.add(db_record)
        db.commit()

        # Execute Alert Evaluation Asynchronously
        background_tasks.add_task(alert_engine.process_transaction_alert, full_analysis)

        # Broadcast real-time stream event to WebSocket subscribers
        await ws_manager.broadcast_transaction(full_analysis)
        
        return full_analysis
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/recent-transactions")
def get_recent_transactions(limit: int = 20, db: Session = Depends(get_db)):
    return db.query(TransactionRecord).order_by(TransactionRecord.id.desc()).limit(limit).all()

@app.websocket("/ws/transactions")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)