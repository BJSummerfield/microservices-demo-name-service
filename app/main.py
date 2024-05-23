import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.post("/names/", response_model=schemas.Name)
def create_name(name: schemas.NameCreate, db: Session = Depends(database.get_db)):
    if not name.id:
        raise HTTPException(status_code=422, detail="ID must be provided")

    db_name = models.Name(id=str(name.id), name=name.name)
    db.add(db_name)
    db.commit()
    db.refresh(db_name)
    logger.info(f"Created name {db_name.id}")
    return db_name

@app.get("/names/", response_model=list[schemas.Name])
def read_names(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    names = db.query(models.Name).offset(skip).limit(limit).all()
    return names

@app.get("/name/{name_id}", response_model=schemas.Name)
def read_name(name_id: str, db: Session = Depends(database.get_db)):
    name = db.query(models.Name).filter(models.Name.id == name_id).first()
    if name is None:
        raise HTTPException(status_code=404, detail="name not found")
    return name

@app.put("/names/{name_id}", response_model=schemas.Name)
def update_name(name_id: str, name: schemas.NameCreate, db: Session = Depends(database.get_db)):
    db_name = db.query(models.Name).filter(models.Name.id == name_id).first()
    if db_name is None:
        raise HTTPException(status_code=404, detail="name not found")
    db_name.name = name.name
    db.commit()
    db.refresh(db_name)
    return db_name

@app.delete("/names/{name_id}", response_model=schemas.Name)
def delete_name(name_id: str, db: Session = Depends(database.get_db)):
    db_name = db.query(models.Name).filter(models.Name.id == name_id).first()
    if db_name is None:
        raise HTTPException(status_code=404, detail="name not found")
    db.delete(db_name)
    db.commit()
    return db_name
