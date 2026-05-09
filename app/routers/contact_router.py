from typing import List

from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.schemas.contact_schema import ContactCreate, ContactOut
from app.services.contact_service import create_contact, get_contacts, get_contact_by_id

router = APIRouter(prefix="/contact",tags=["contact"])

@router.post("",response_model=ContactOut)
def contact_create(payload:ContactCreate,db:Session=Depends(get_db)):
    return create_contact(db,payload)

@router.get("/contacts",response_model=List[ContactOut])
def contact_get(db:Session=Depends(get_db)):
    return get_contacts(db)

@router.get("/contact/{contact_id}",response_model=ContactOut)
def contact_get_id(contact_id:int,db:Session=Depends(get_db)):
    return get_contact_by_id(db,contact_id)
