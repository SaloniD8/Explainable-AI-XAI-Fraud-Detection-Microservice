from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from xai_engine import evaluate_transaction
import uvicorn

app = FastAPI(title="Explainable AI Fraud Detection Service")

class TransactionRequest(BaseModel):
    id: Optional[int] = None
    userId: Optional[str] = None
    amount: float
    location: Optional[str] = None
    timestamp: Optional[str] = None
    distanceToPrevious: float
    isFraud: Optional[bool] = None
    xaiExplanation: Optional[str] = None

@app.post("/evaluate-fraud")
def evaluate_fraud(transaction: TransactionRequest):
    result = evaluate_transaction(transaction.amount, transaction.distanceToPrevious)
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
