from typing import Literal
from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name:str
    category:Literal['Software','Hardware']
    unit_price:float
    cost:float
    stock_qty:int

class ProductUpdate(BaseModel):
    unit_price:float
    cost:float
    stock_qty:int

class ProductDelete(BaseModel):
    name:str
    product_id:int

class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name:str
    category: Literal['Software', 'Hardware']
    unit_price: float
    cost: float
    stock_qty: int