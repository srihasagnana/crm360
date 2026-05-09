from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Double, ForeignKey
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped,mapped_column
from app.db.connection import Base

class Complaint(Base):
    __tablename__ = 'complaint'
    complaint_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,nullable=False)
    customer_id:Mapped[int]=mapped_column(Integer,ForeignKey('customer.customer_id'),nullable=False)
    category:Mapped[str]=mapped_column(ENUM('Product','Delivery','Service'),nullable=False)
    severity:Mapped[str]=mapped_column(ENUM('Low','Medium','High'),nullable=False)
    raised_date:Mapped[datetime]=mapped_column(DateTime,nullable=False,default=datetime.now())
    resolved_date:Mapped[datetime]=mapped_column(DateTime,nullable=False,default=datetime.now())
