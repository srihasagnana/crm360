from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict


class InteractionCreate(BaseModel):
    customer_id:int
    type:Literal['Call', 'Email', 'Meeting']
    channel:Literal['WhatsApp',"Phone",'Email']
    outcome:Literal['Positive','Negative','Neutral']
    interaction_date:datetime

class InteractionUpdate(BaseModel):
    customer_id:int
    type:Literal['Call', 'Email', 'Meeting']

class InteractionDelete(BaseModel):
    customer_id:int

class InteractionOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    customer_id:int
    type: Literal['Call', 'Email', 'Meeting']
    channel: Literal['WhatsApp', "Phone", 'Email']
    outcome: Literal['Positive', 'Negative', 'Neutral']
    interaction_date: datetime