from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Double, ForeignKey
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped,mapped_column
from app.db.connection import Base

class Interation(Base):
    __tablename__ = 'interation'
    interaction_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,nullable=False)
    customer_id:Mapped[int]=mapped_column(Integer,ForeignKey('customer.customer_id'),nullable=False)
    type:Mapped[str]=mapped_column(ENUM('Call', 'Email', 'Meeting'),nullable=False)
    channel:Mapped[str]=mapped_column(ENUM('WhatsApp',"Phone",'Email'),nullable=False)
    outcome:Mapped[str]=mapped_column(ENUM('Positive',"Negative",'Neutral'),nullable=False)
    interaction_date:Mapped[datetime]=mapped_column(DateTime,nullable=False,default=datetime.now())