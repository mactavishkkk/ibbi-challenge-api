from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import services.category_service as category_service, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    categories = category_service.get_categories(db, skip=skip, limit=limit)
    
    return categories

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    category = category_service.get_category_by_id(db, category_id=category_id)

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    return category_service.create_category(db=db, category=category)

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category_update: schemas.CategoryUpdate, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    category = category_service.update_category(db, category_id, category_update)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(category_id: int, db: Session = Depends(get_db), auth: dict = Depends(get_current_user)):
    category = category_service.delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category