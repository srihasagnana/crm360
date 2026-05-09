from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict


class ComplaintCreate(BaseModel):
    customer_id:int
    category:Literal['Product','Delivery','Service']
    severity:Literal['Low','Medium','High']
    raised_date:datetime
    resolved_date:datetime

class ComplaintUpdate(BaseModel):
    complaint_id:int
    resolved_date:datetime

class ComplaintDelete(BaseModel):
    complaint_id:int

class ComplaintOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    complaint_id:int
    category:str
    severity: Literal['Low', 'Medium', 'High']
    raised_date: datetime
    resolved_date: datetime