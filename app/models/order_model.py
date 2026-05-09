from datetime import datetime
from numpy import double
from sqlalchemy import Integer, String, DateTime, Double, ForeignKey
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped,mapped_column
from app.db.connection import Base

class Order(Base):
    __tablename__ = 'order'
    order_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,nullable=False)
    customer_id:Mapped[int]=mapped_column(Integer,ForeignKey('customer.customer_id'),nullable=False)
    product_id:Mapped[int]=mapped_column(Integer,ForeignKey('product.product_id'),nullable=False)
    qty:Mapped[int]=mapped_column(Integer,nullable=False,default=0)
    amount:Mapped[float]=mapped_column(Double,nullable=False)
    order_date:Mapped[datetime]=mapped_column(DateTime,nullable=False,default=datetime.now())
    status:Mapped[str]=mapped_column(ENUM('Delivered','Cancelled','Pending'),nullable=False)