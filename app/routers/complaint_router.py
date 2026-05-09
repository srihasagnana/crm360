from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.schemas.complaint_schema import ComplaintCreate, ComplaintUpdate, ComplaintOut
from app.services.complaint_service import (
    create_complaint_service,
    get_complaints,
    get_complaint_by_id,
    update_complaint_service,
    delete_complaint_service
)

router = APIRouter(prefix="/complaint", tags=["complaint"])

@router.post("", response_model=ComplaintOut)
def create_complaint(payload: ComplaintCreate, db: Session = Depends(get_db)):
    return create_complaint_service(db, payload)

@router.get("/complaints", response_model=List[ComplaintOut])
def get_all_complaints(db: Session = Depends(get_db)):
    return get_complaints(db)

@router.get("/{complaint_id}", response_model=ComplaintOut)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    return get_complaint_by_id(db, complaint_id)

@router.put("/update/{complaint_id}", response_model=ComplaintOut)
def update_complaint(complaint_id: int, payload: ComplaintUpdate, db: Session = Depends(get_db)):
    return update_complaint_service(db, complaint_id, payload)

@router.delete("/delete/{complaint_id}", response_model=ComplaintOut)
def delete_complaint(complaint_id: int, db: Session = Depends(get_db)):
    return delete_complaint_service(db, complaint_id)