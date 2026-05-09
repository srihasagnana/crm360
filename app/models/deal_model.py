from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Double, ForeignKey
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped,mapped_column
from app.db.connection import Base

class Deal(Base):
    __tablename__ = 'deal'
    deal_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,nullable=False)
    customer_id:Mapped[int]=mapped_column(Integer,ForeignKey('customer.customer_id'),nullable=False)
    stage:Mapped[str]=mapped_column(ENUM('Qualified','Lost','Negotiation','Won','Proposal','Lead'),nullable=False)
    value:Mapped[float]=mapped_column(Double,nullable=False)
    created_date:Mapped[datetime]=mapped_column(DateTime,nullable=False,default=datetime.now)
    closed_date:Mapped[datetime]=mapped_column(DateTime,nullable=False,default=datetime.now)
    deal_owner:Mapped[str]=mapped_column(String(30),nullable=False)
