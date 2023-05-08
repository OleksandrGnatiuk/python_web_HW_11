from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactModel
from datetime import datetime, timedelta
from sqlalchemy import text

async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact

#
# async def find_contacts(db: Session):
#     contacts = db.query(Contact).filter_by().all()
#     return contacts


async def search_contacts_by_birthday(limit: int, offset: int, db: Session):
    sql_select = """
    select *
    from contacts
    WHERE (STRFTIME('%m-%d', birthday)
    between strftime('%m-%d', date('now')) and strftime('%m-%d', date('now','+7 days')));
    """
    contacts = db.execute(text(sql_select)).all()
    return contacts


async def create(body: ContactModel, db: Session = Depends(get_db)):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
