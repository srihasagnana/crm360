from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):
    customer_id:int
    product_id:int
    qty:int
    amount:float
    order_date:datetime
    status: Literal['Delivered','Cancelled','Pending']

class OrderUpdate(BaseModel):
    qty:int
    amount:float

class OrderOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_id:int
    customer_id: int
    product_id: int
    qty: int
    amount: float
    order_date: datetime
    status: Literal['Delivered', 'Cancelled', 'Pending']