from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.schemas.customer_schema import CustomerOut, CustomerCreate, CustomerUpdate, CustomerDelete
from app.services.customer_service import create_customer, get_customers, get_customer_by_id, update_customer, \
    delete_customer

router=APIRouter(prefix="/customer",tags=["customer"])

@router.post("",response_model=CustomerOut)
def customer_create(payload:CustomerCreate,db:Session=Depends(get_db)):
    return create_customer(db,payload)

@router.get("/customers",response_model=List[CustomerOut])
def customer_get(db:Session=Depends(get_db)):
    return get_customers(db)

@router.get("/customer/{customer_id}",response_model=CustomerOut)
def customer_by_id(customer_id: int,db:Session=Depends(get_db)):
    return get_customer_by_id(db,customer_id)

@router.put("/customer/update",response_model=CustomerOut)
def customer_update(payload:CustomerUpdate,customer_id:int,db:Session=Depends(get_db)):
    return update_customer(db,payload,customer_id)

@router.delete("/customer/delete",response_model=CustomerOut)
def customer_delete(payload:CustomerDelete,customer_id:int,db:Session=Depends(get_db)):
    return delete_customer(db,customer_id,payload)