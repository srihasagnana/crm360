from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict

class DealCreate(BaseModel):
    customer_id: int
    stage: Literal['Qualified','Lost','Negotiation','Won','Proposal','Lead']
    value: float
    created_date: datetime
    closed_date: datetime
    deal_owner: str

class DealUpdate(BaseModel):
    customer_id: int
    deal_owner: str

class DealDelete(BaseModel):
    customer_id: int
    deal_owner: str

class DealOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    deal_id: int
    customer_id: int
    stage: Literal['Qualified','Lost','Negotiation','Won','Proposal','Lead']
    value: float
    created_date: datetime
    closed_date: datetime
    deal_owner: str