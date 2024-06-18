from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database
from auth import get_current_user

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import services.product_service as product_service

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    products = product_service.get_products(db, skip=skip, limit=limit)

    return products

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    product = product_service.get_product_by_id(db, product_id=product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    return product_service.create_product(db=db, product=product)

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    product = product_service.update_product(db, product_id, product_update)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.delete("/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    product = product_service.delete_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product
