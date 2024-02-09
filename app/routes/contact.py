# routes/contact.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal, engine
from ..models.contact import Contact
from ..schemas.contact import ContactCreate

router = APIRouter()

# Залежність для отримання сесії бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contacts/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/contacts/", response_model=List[Contact])
def read_contacts(q: str = None, db: Session = Depends(get_db)):
    if q:
        contacts = db.query(Contact).filter(Contact.name.contains(q)).all()
    else:
        contacts = db.query(Contact).all()
    return contacts

# Інші маршрути...
