from typing import List

from fastapi import HTTPException
from app.models.customer_model import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate, CustomerDelete
from sqlalchemy.orm import Session

def create_customer(db:Session,customer:CustomerCreate)->Customer:
    obj=Customer(
        name=customer.name,
        email=customer.email,
        city=customer.city,
        state=customer.state,
        segment=customer.segment,
        doj=customer.doj,
        annual_spend=customer.annual_spend,
        churn=customer.churn,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_customer_by_id(db:Session,customer_id:int):
    return db.get(Customer,customer_id)

def get_customers(db:Session):
    return db.query(Customer).all()

def update_customer(db:Session,customer:CustomerUpdate,customer_id:int)->Customer:
    obj=db.get(Customer,customer_id)
    obj.name = customer.name
    obj.email = customer.email
    obj.city = customer.city
    obj.state = customer.state
    db.commit()
    db.refresh(obj)
    return obj

def delete_customer(db:Session,customer_id:int,customer:CustomerDelete):
    obj = db.get(customer_id)
    obj.delete()
    db.delete(obj)
    db.commit()
    return "customer deleted"