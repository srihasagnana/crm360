from sqlalchemy.orm import Session
from app.models.deal_model import Deal
from app.schemas.deal_schema import DealCreate, DealUpdate

def create_deal_service(db: Session, deal: DealCreate):
    obj = Deal(
        customer_id=deal.customer_id,
        stage=deal.stage,
        value=deal.value,
        created_date=deal.created_date,
        closed_date=deal.closed_date,
        deal_owner=deal.deal_owner
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_deal_service(db: Session, deal_id: int, deal: DealUpdate):
    obj = db.get(Deal, deal_id)
    if not obj:
        return None
    obj.customer_id = deal.customer_id
    obj.deal_owner = deal.deal_owner
    db.commit()
    db.refresh(obj)
    return obj

def delete_deal_service(db: Session, deal_id: int):
    obj = db.get(Deal, deal_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def get_deal_by_id(db: Session, deal_id: int):
    return db.get(Deal, deal_id)

def get_deals(db: Session):
    return db.query(Deal).all()