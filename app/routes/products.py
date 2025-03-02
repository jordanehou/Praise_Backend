from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..database import SessionLocal
from ..models import Product
from ..schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return JSONResponse(content={
        "message": "Product created successfully",
        "product": {"id": new_product.id, "name": new_product.name, "category_id": new_product.category_id}
    }, status_code=201)

@router.get("/list", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return JSONResponse(content={
        "products": [{"id": p.id, "name": p.name, "category_id": p.category_id} for p in products]
    }, status_code=200)

# @router.get("/detail/{product_id}", response_model=ProductResponse)
# def get_product(product_id: int, db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return JSONResponse(content={
#         "product": {"id": product.id, "name": product.name, "category_id": product.category_id}
#     }, status_code=200)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Inclure les livraisons associées
    deliveries = db.query(Delivery).filter(Delivery.product_id == product_id).all()

    return JSONResponse(
        content={
            "product": {
                "id": product.id,
                "name": product.name,
                "category_id": product.category_id,
                "quantity": product.quantity,
                "unit_price": product.unit_price,
                "description": product.description,
                "deliveries": [
                    {
                        "id": d.id,
                        "structure_name": d.structure_name,
                        "delivery_date": d.delivery_date.strftime("%Y-%m-%d"),
                        "quantity": d.quantity,
                        "amount_paid": d.amount_paid
                    }
                    for d in deliveries
                ]
            }
        },
        status_code=200
    )

@router.put("/update/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)

    return JSONResponse(content={
        "message": "Product updated successfully",
        "product": {"id": product.id, "name": product.name, "category_id": product.category_id}
    }, status_code=200)

@router.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return JSONResponse(content={"message": "Product deleted successfully"}, status_code=200)
