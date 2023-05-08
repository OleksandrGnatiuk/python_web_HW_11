from typing import Optional

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    first_name: str = Field('Taras', min_length=3, max_length=16)
    last_name: str = Field('Shevchenko', min_length=3, max_length=16)
    email: EmailStr
    phone_number: str = Field('+380671112233', min_length=9, max_length=16)
    birthday: str = Field('1814-03-09')
    additional_data: str


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str = Field('Taras', min_length=3, max_length=16)
    last_name: str = Field('Shevchenko', min_length=3, max_length=16)
    email: EmailStr
    phone_number: str = Field('+380671112233', min_length=9, max_length=16)
    birthday: str = Field('1814-03-09')
    additional_data: str

    class Config:
        orm_mode = True
