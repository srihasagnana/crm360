from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.contact_model import Contact
from app.schemas.contact_schema import ContactCreate, ContactUpdate


def create_contact(db:Session,contact:ContactCreate)->Contact:
    obj=Contact(
        customer_id=contact.customer_id,
        phone=contact.phone,
        whatsapp=contact.whatsapp,
        preferred_channel=contact.preferred_channel,
        last_contact=contact.last_contact
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_contact(db:Session,contact:ContactUpdate,contact_id:int)->Contact:
    obj=contact.get(contact_id)
    obj.last_contact=contact.last_contact
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_contact_by_id(db:Session,contact_id:int)->Contact:
    return db.query(Contact).get(contact_id)

def get_contacts(db:Session)->List[Contact]:
    return db.query(Contact).all()