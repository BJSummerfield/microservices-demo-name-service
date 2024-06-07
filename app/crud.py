from sqlalchemy.orm import Session
from .models import Name
from .schemas import NameCreate, NameUpdate

def get_name(db: Session, name_id: str):
    return db.query(Name).filter(Name.id == name_id).first()

def create_name(db: Session, name: NameCreate):
    db_name = Name(id=name.id, name=name.name)
    db.add(db_name)
    db.commit()
    db.refresh(db_name)
    return db_name

def update_name(db: Session, name_id: str, name: NameUpdate):
    db_name = get_name(db, name_id)
    if db_name:
        db_name.name = name.name
        db.commit()
        db.refresh(db_name)
        return db_name
    return None

def delete_name(db: Session, name_id: str):
    db_name = get_name(db, name_id)
    if db_name:
        db.delete(db_name)
        db.commit()
        return db_name
    return None

