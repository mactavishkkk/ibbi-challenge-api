from sqlalchemy.orm import Session
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import models, schemas

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    product = models.Product(**product.dict())

    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if product:
        product.name = product_update.name
        product.description = product_update.description
        product.value = product_update.value
        product.dolarValue = product_update.dolarValue
        product.image = product_update.image
        product.quantity = product_update.quantity
        product.status = product_update.status
        product.category_id = product_update.category_id
        db.commit()
        db.refresh(product)

    return product

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if product:
        db.delete(product)
        db.commit()
        
    return product