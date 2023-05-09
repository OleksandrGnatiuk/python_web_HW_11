from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactModel
from sqlalchemy import text


async def get_contacts(limit: int, offset: int, first_name: str, last_name: str, email: str, db: Session):
    first_name_query = db.query(Contact).filter(Contact.first_name == first_name)
    last_name_query = db.query(Contact).filter(Contact.last_name == last_name)
    email_query = db.query(Contact).filter(Contact.email == email)
    if first_name and last_name and email:
        return first_name_query.union(last_name_query).union(email_query).all()
    if first_name and last_name:
        return first_name_query.union(last_name_query).all()
    if first_name and email:
        return first_name_query.union(email_query).all()
    if last_name and email:
        return last_name_query.union(email_query).all()
    if first_name:
        return first_name_query.all()
    if last_name:
        return last_name_query.all()
    if email:
        return email_query.all()
    return db.query(Contact).limit(limit).offset(offset).all()


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def search_contacts_by_birthday(limit: int, offset: int, db: Session):
    raw_sql_select = """
    SELECT *
    FROM contacts
    WHERE (STRFTIME('%m-%d', birthday)
    BETWEEN STRFTIME('%m-%d', date('now')) AND STRFTIME('%m-%d', date('now','+7 days')));
    """
    contacts = db.execute(text(raw_sql_select)).all()
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
