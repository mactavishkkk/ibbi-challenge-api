from sqlalchemy.orm import Session
from .. import models, schemas

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, description=category.description)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category