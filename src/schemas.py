from datetime import datetime, date
from typing import  Optional
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):

    name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: Optional[EmailStr]
    phone: str = Field(max_length=20)
    born_date: date
    

class ContactResponse(ContactModel):

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
