from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.schemas.deal_schema import DealCreate, DealUpdate, DealOut
from app.services.deal_service import (
    create_deal_service,
    get_deals,
    get_deal_by_id,
    update_deal_service,
    delete_deal_service
)

router = APIRouter(prefix="/deal", tags=["deal"])

@router.post("", response_model=DealOut)
def create_deal(payload: DealCreate, db: Session = Depends(get_db)):
    return create_deal_service(db, payload)

@router.get("/deals", response_model=List[DealOut])
def get_all_deals(db: Session = Depends(get_db)):
    return get_deals(db)

@router.get("/{deal_id}", response_model=DealOut)
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    return get_deal_by_id(db, deal_id)

@router.put("/update/{deal_id}", response_model=DealOut)
def update_deal(deal_id: int, payload: DealUpdate, db: Session = Depends(get_db)):
    return update_deal_service(db, deal_id, payload)

@router.delete("/delete/{deal_id}", response_model=DealOut)
def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    return delete_deal_service(db, deal_id)