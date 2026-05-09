from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Double
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped,mapped_column
from app.db.connection import Base

class Customer(Base):
    __tablename__ = 'customer'
    customer_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,nullable=False)
    name:Mapped[str]=mapped_column(String(30),nullable=False)
    email:Mapped[str]=mapped_column(String(30))
    city:Mapped[str]=mapped_column(String(30),nullable=False)
    state:Mapped[str]=mapped_column(String(30),nullable=False)
    segment:Mapped[str]=mapped_column(String(30),nullable=False)
    doj:Mapped[datetime]=mapped_column(DateTime,nullable=False,default=datetime.now())
    annual_spend:Mapped[float]=mapped_column(Double,nullable=False,default=0)
    churn:Mapped[str]=mapped_column(ENUM('0','1'),nullable=False,default=0)