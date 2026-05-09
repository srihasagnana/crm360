from sqlalchemy.orm import Session
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

def create_product_service(db: Session, product: ProductCreate):
    obj = Product(
        name=product.name,
        category=product.category,
        unit_price=product.unit_price,
        cost=product.cost,
        stock_qty=product.stock_qty
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_product_service(db: Session, product_id: int, product: ProductUpdate):
    obj = db.get(Product, product_id)
    if not obj:
        return None
    obj.unit_price = product.unit_price
    obj.cost = product.cost
    obj.stock_qty = product.stock_qty
    db.commit()
    db.refresh(obj)
    return obj

def delete_product_service(db: Session, product_id: int):
    obj = db.get(Product, product_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def get_product_by_id(db: Session, product_id: int):
    return db.get(Product, product_id)

def get_products(db: Session):
    return db.query(Product).all()