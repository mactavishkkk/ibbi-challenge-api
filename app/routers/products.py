from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, database
from auth import get_current_user

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import services.product_service as product_service

router = APIRouter()
UPLOAD_DIR = "app/uploads/images"

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, category_id: Optional[int] = None, description: Optional[str] = None, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    products = product_service.get_products(db, skip=skip, limit=limit, category_id=category_id, description=description)

    if not products:
        raise HTTPException(status_code=404, detail="Products not found")
    
    return products

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    product = product_service.get_product_by_id(db, product_id=product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.get("/images/{image_hash}")
async def get_image(image_hash: str):
    image_path = os.path.join(UPLOAD_DIR, image_hash)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    media_type = "image/jpeg" if image_path.endswith(".jpg") else "image/png"

    return FileResponse(image_path, media_type=media_type)

@router.post("/", response_model=schemas.Product)
def create_product(
    name: str = Form(...), description: str = Form(...), value: float = Form(...),
    dolarValue: float = Form(...), quantity: int = Form(...), status: str = Form(...),
    image: str = Form(...), category_id: int = Form(...), file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db), auth: dict = Depends(get_current_user)
):
    product_create = schemas.ProductCreate(
        name=name,
        description=description,
        value=value,
        dolarValue=dolarValue,
        image=image,
        quantity=quantity,
        status=status,
        category_id=category_id
    )
    
    return product_service.create_product(db=db, product=product_create, file=file)

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
