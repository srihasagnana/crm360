from sqlalchemy.orm import Session
from app.models.complaint_model import Complaint
from app.schemas.complaint_schema import ComplaintCreate, ComplaintUpdate

def create_complaint_service(db: Session, complaint: ComplaintCreate):
    obj = Complaint(
        customer_id=complaint.customer_id,
        category=complaint.category,
        severity=complaint.severity,
        raised_date=complaint.raised_date,
        resolved_date=complaint.resolved_date
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_complaint_service(db: Session, complaint_id: int, complaint: ComplaintUpdate):
    obj = db.get(Complaint, complaint_id)
    if not obj:
        return None
    obj.customer_id = complaint.customer_id
    obj.category = complaint.category
    obj.resolved_date = complaint.resolved_date
    db.commit()
    db.refresh(obj)
    return obj

def delete_complaint_service(db: Session, complaint_id: int):
    obj = db.get(Complaint, complaint_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def get_complaint_by_id(db: Session, complaint_id: int):
    return db.get(Complaint, complaint_id)

def get_complaints(db: Session):
    return db.query(Complaint).all()