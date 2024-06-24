from sqlalchemy.orm import Session
from typing import Optional
from fastapi import UploadFile
import sys, os
import hashlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import models, schemas

UPLOAD_DIR = 'app/uploads/images'
DEFAULT_IMAGE_PATH = 'app/assets/product-default-image.png'

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def get_products(db: Session, skip: int = 0, limit: int = 50, category_id: Optional[int] = None, description: Optional[str] = None):
    query = db.query(models.Product)

    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)

    if description is not None:
        query = query.filter(models.Product.description.ilike(f'%{description}%'))

    return query.offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate, file: Optional[UploadFile] = None):
    image_hash = None
    
    if file:
        content = file.file.read()
        image_hash = hashlib.sha256(content).hexdigest()
        file_path = os.path.join(UPLOAD_DIR, image_hash)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(file_path, "wb") as image_file:
            image_file.write(content)
    else:
        with open(DEFAULT_IMAGE_PATH, "rb") as default_image_file:
            default_image_content = default_image_file.read()
            image_hash = hashlib.sha256(default_image_content).hexdigest()
            file_path = os.path.join(UPLOAD_DIR, image_hash)
            with open(file_path, "wb") as image_file:
                image_file.write(default_image_content)

    status = calculate_status(product.quantity)

    product = models.Product(
        name=product.name,
        description=product.description,
        value=product.value,
        dolarValue=product.dolarValue,
        image=image_hash,
        quantity=product.quantity,
        status=status,
        category_id=product.category_id
    )

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

def calculate_status(quantity: int) -> str:
    suggested_quantity = 10

    if quantity < suggested_quantity:
        return "red"
    elif quantity - suggested_quantity <= 5:
        return "yellow"
    else:
        return "green"