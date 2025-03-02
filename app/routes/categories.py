from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..schemas import CategoryCreate, CategoryResponse
from ..database import SessionLocal
from ..models import Category  # Import du modèle

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(title=category.title)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return JSONResponse(content={
        "message": "Category created",
        "category": {"id": new_category.id, "title": new_category.title}
    }, status_code=201)

@router.get("/list", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return JSONResponse(content={
        "categories": [{"id": cat.id, "title": cat.title} for cat in categories]
    }, status_code=200)

@router.get("/detail/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return JSONResponse(content={
        "category": {"id": category.id, "title": category.title}
    }, status_code=200)

@router.delete("/delete/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return JSONResponse(content={"message": "Category deleted"}, status_code=200)
