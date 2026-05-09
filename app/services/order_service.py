from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.schemas.order_schema import OrderCreate, OrderUpdate

def create_order_service(db: Session, order: OrderCreate):
    obj = Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        qty=order.qty,
        amount=order.amount,
        order_date=order.order_date,
        status=order.status
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_order_service(db: Session, order_id: int, order: OrderUpdate):
    obj = db.get(Order, order_id)
    if not obj:
        return None
    obj.qty = order.qty
    obj.amount = order.amount
    db.commit()
    db.refresh(obj)
    return obj

def delete_order_service(db: Session, order_id: int):
    obj = db.get(Order, order_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def get_order_by_id(db: Session, order_id: int):
    return db.get(Order, order_id)

def get_orders(db: Session):
    return db.query(Order).all()