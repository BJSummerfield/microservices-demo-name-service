from sqlalchemy.orm import Session
import models, schemas

def get_name(db: Session, name_id: str):
    return db.query(models.Name).filter(models.Name.id == name_id).first()

def get_names(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Name).offset(skip).limit(limit).all()

def create_name(db: Session, name: schemas.NameCreate):
    db_name = models.Name(id=name.id, name=name.name)
    db.add(db_name)
    db.commit()
    db.refresh(db_name)
    return db_name

def update_name(db: Session, name_id: str, name: schemas.NameUpdate):
    db_name = db.query(models.Name).filter(models.Name.id == name_id).first()
    db_name.name = name.name
    db.commit()
    db.refresh(db_name)
    return db_name

def delete_name(db: Session, name_id: str):
    db_name = db.query(models.Name).filter(models.Name.id == name_id).first()
    db.delete(db_name)
    db.commit()
    return db_name
