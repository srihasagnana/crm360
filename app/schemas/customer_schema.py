from typing import Optional
from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime

class CustomerCreate(BaseModel):
    name:str
    email:Optional[str]
    city:str
    state:str
    segment:str
    doj:datetime
    annual_spend:float
    churn:str

class CustomerUpdate(BaseModel):
    name:str
    email:Optional[str]
    city:str
    state:str

class CustomerDelete(BaseModel):
    annual_spend:float
    churn:str

class CustomerOut(BaseModel):
    model_config =ConfigDict(from_attributes=True)
    customer_id: int
    email: str
    city: str
    state: str
    segment: str
    doj: datetime
    annual_spend: float
    churn: str