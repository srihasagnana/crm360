from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict


class ContactCreate(BaseModel):
    customer_id:int
    phone:Optional[int]
    whatsapp:Optional[int]
    preferred_channel:Literal["WhatsApp","Phone","Email"]
    last_contact:Optional[datetime]

class ContactUpdate(BaseModel):
    last_contact:Optional[datetime]

class ContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    contact_id: int
    customer_id: int
    phone: int
    whatsapp: int
    preferred_channel: Literal["WhatsApp","Phone","Email"]
    last_contact: datetime