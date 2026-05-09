from datetime import datetime
from numpy import double
from sqlalchemy import Integer, String, DateTime, Double
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped,mapped_column
from app.db.connection import Base

class Product(Base):
    __tablename__ = 'product'
    product_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,nullable=False)
    name:Mapped[str]=mapped_column(String(30),nullable=False,default="")
    category:Mapped[str]=mapped_column(ENUM('Software','Hardware'),nullable=False)
    unit_price:Mapped[double]=mapped_column(Double,nullable=False)
    cost:Mapped[float]=mapped_column(Double,nullable=False)
    stock_qty:Mapped[int]=mapped_column(Integer,nullable=False)