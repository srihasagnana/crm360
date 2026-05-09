from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from app.services.product_Service import (
    create_product_service,
    get_products,
    get_product_by_id,
    update_product_service,
    delete_product_service
)

router = APIRouter(prefix="/product", tags=["product"])

@router.post("", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return create_product_service(db, payload)

@router.get("/products", response_model=List[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    return get_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_by_id(db, product_id)

@router.put("/update/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    return update_product_service(db, product_id, payload)

@router.delete("/delete/{product_id}", response_model=ProductOut)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return delete_product_service(db, product_id)