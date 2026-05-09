from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.schemas.interaction_schema import InteractionCreate, InteractionUpdate, InteractionOutput
from app.services.interaction_service import (
    create_interaction_service,
    get_interactions,
    get_interaction_by_id,
    update_interaction_service,
    delete_interaction_service
)

router = APIRouter(prefix="/interaction", tags=["interaction"])

@router.post("", response_model=InteractionOutput)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    return create_interaction_service(db, payload)

@router.get("/interactions", response_model=List[InteractionOutput])
def get_all_interactions(db: Session = Depends(get_db)):
    return get_interactions(db)

@router.get("/{interaction_id}", response_model=InteractionOutput)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    return get_interaction_by_id(db, interaction_id)

@router.put("/update/{interaction_id}", response_model=InteractionOutput)
def update_interaction(interaction_id: int, payload: InteractionUpdate, db: Session = Depends(get_db)):
    return update_interaction_service(db, interaction_id, payload)

@router.delete("/delete/{interaction_id}", response_model=InteractionOutput)
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    return delete_interaction_service(db, interaction_id)