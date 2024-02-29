from typing import List
from datetime import datetime, timedelta
from collections import defaultdict

from sqlalchemy import and_, or_, extract
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session, name: str = None, last_name: str = None, email: str = None) -> List[Contact]:

    queries = []

    if name:
        queries.append(Contact.name == name)
    if last_name:
        queries.append(Contact.last_name == last_name)
    if email:
        queries.append(Contact.email == email)

    contacts = db.query(Contact).filter(and_(*queries)).all()
    return contacts


async def get_contacts_birthdays(db: Session) -> List[Contact]:

    today = datetime.now().date()
    last_day = today + timedelta(days=7)

    dates = db.query(Contact).filter(or_
                                        (and_(extract('month', Contact.born_date) == last_day.month,
                                               extract('day', Contact.born_date) <= last_day.day),

                                        and_(extract('month', Contact.born_date) == today.month,
                                               extract('day', Contact.born_date) >= today.day))).all()

    return dates


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:

    contact = Contact(name = body.name, last_name = body.last_name, email = body.email, phone = body.phone, born_date = body.born_date)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:

    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.born_date = body.born_date
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact | None:

    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
