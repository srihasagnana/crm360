from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderOutput
from app.services.order_service import (
    create_order_service,
    get_orders,
    get_order_by_id,
    update_order_service,
    delete_order_service
)

router = APIRouter(prefix="/order", tags=["order"])

@router.post("", response_model=OrderOutput)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return create_order_service(db, payload)

@router.get("/orders", response_model=List[OrderOutput])
def get_all_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.get("/{order_id}", response_model=OrderOutput)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return get_order_by_id(db, order_id)

@router.put("/update/{order_id}", response_model=OrderOutput)
def update_order(order_id: int, payload: OrderUpdate, db: Session = Depends(get_db)):
    return update_order_service(db, order_id, payload)

@router.delete("/delete/{order_id}", response_model=OrderOutput)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return delete_order_service(db, order_id)