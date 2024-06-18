from sqlalchemy.orm import Session

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import models, schemas

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, description=category.description)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

def update_category(db: Session, category_id: int, category_update: schemas.CategoryUpdate):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if category:
        category.name = category_update.name
        category.description = category_update.description
        db.commit()
        db.refresh(category)

    return category

def delete_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if category:
        db.delete(category)
        db.commit()
        
    return category