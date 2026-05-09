from sqlalchemy import Double
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped,mapped_column

from app.db.connection import Base

class Contact(Base):
    __tablename__ =  'contact'

    contact_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,nullable=False)
    customer_id:Mapped[int]=mapped_column(Integer,ForeignKey('customer.customer_id'))
    phone:Mapped[int]=mapped_column(Integer)
    whatsapp:Mapped[int]=mapped_column(Integer)
    preferred_channel:Mapped[str]=mapped_column(ENUM("WhatsApp","Phone","Email"),nullable=False)
    last_contact:Mapped[float]=mapped_column(Double)