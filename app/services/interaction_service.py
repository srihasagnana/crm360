from sqlalchemy.orm import Session
from app.models.interaction_model import Interation
from app.schemas.interaction_schema import InteractionCreate, InteractionUpdate

def create_interaction_service(db: Session, interaction: InteractionCreate):
    obj = Interation(
        customer_id=interaction.customer_id,
        type=interaction.type,
        channel=interaction.channel,
        outcome=interaction.outcome,
        interaction_date=interaction.interaction_date
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_interaction_service(db: Session, interaction_id: int, interaction: InteractionUpdate):
    obj = db.get(Interation, interaction_id)
    if not obj:
        return None
    obj.customer_id = interaction.customer_id
    obj.type = interaction.type
    db.commit()
    db.refresh(obj)
    return obj

def delete_interaction_service(db: Session, interaction_id: int):
    obj = db.get(Interation, interaction_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def get_interaction_by_id(db: Session, interaction_id: int):
    return db.get(Interation, interaction_id)

def get_interactions(db: Session):
    return db.query(Interation).all()