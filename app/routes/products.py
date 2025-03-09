from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..database import SessionLocal
from ..models import Product, Delivery
from ..schemas import ProductCreate, ProductUpdate, ProductResponse
import base64
import os

router = APIRouter()

# def convert_image_to_base64(image_file: UploadFile) -> str:
#     return base64.b64encode(image_file.file.read()).decode('utf-8')

def convert_image_to_base64(image_path: str) -> str:
    if not os.path.isfile(image_path):
        raise FileNotFoundError("Image file not found.")
    
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
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

# @router.post("/create", response_model=ProductResponse)
# async def create_product(product: ProductCreate, image: UploadFile = File(...), db: Session = Depends(get_db)):
#     # Vérifications pour l'image (type et taille)
#     if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
#         raise HTTPException(status_code=400, detail="Invalid image format.")
    
#     if image.size > 1 * 1024 * 1024:  # 1 Mo
#         raise HTTPException(status_code=400, detail="Image size exceeds 1 MB.")

#     image_data = await image.read()

#     new_product = Product(
#         name=product.name,
#         description=product.description,
#         price=product.price,
#         image=image_data  # Stocker l'image
#     )
    
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)

#     return JSONResponse(content={
#         "message": "Product created successfully",
#         "product": jsonable_encoder(new_product)
#     }, status_code=201)


# @router.post("/create", response_model=ProductResponse)
# async def create_product(
#     product: ProductCreate,  # Utiliser le modèle qui inclut l'image
#     db: Session = Depends(get_db)
# ):
#     # Vérifie si le fichier existe
#     if not os.path.isfile(product.image):
#         raise HTTPException(status_code=404, detail="Image file not found.")
    
#     # Convertir l'image en Base64
#     image_data = convert_image_to_base64(product.image)

#     new_product = Product(
#         name=product.name,
#         description=product.description,
#         category_id=product.category_id,
#         quantity=product.quantity,
#         unit_price=product.unit_price,
#         image=image_data  # Stocker l'image en Base64
#     )
    
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)

#     return JSONResponse(content={
#         "message": "Product created successfully",
#         "product": jsonable_encoder(new_product)
#     }, status_code=201)

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/listcategory/{category_id}", response_model=list[ProductResponse])
def list_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_id == category_id).all()
    
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this category")
    
    return JSONResponse(
        content={
            "category_id": category_id,
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "category_id": p.category_id,
                    "quantity": p.quantity,
                    "unit_price": p.unit_price,
                    "description": p.description,
                    "deliveries": [
                        {
                            "id": d.id,
                            "structure_name": d.structure_name,
                            "delivery_date": d.delivery_date.strftime("%Y-%m-%d"),
                            "quantity": d.quantity,
                            "amount_paid": d.amount_paid
                        }
                        for d in db.query(Delivery).filter(Delivery.product_id == p.id).all()
                    ]
                }
                for p in products
            ]
        },
        status_code=200
    )


@router.get("/detail/{product_id}", response_model=ProductResponse)
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

# @router.put("/update/{product_id}", response_model=ProductResponse)
# async def update_product(product_id: int, product_data: ProductUpdate, image: UploadFile = File(None), db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     if image:
#         # Vérifications pour l'image (type et taille)
#         if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
#             raise HTTPException(status_code=400, detail="Invalid image format.")
        
#         if image.size > 1 * 1024 * 1024:  # 1 Mo
#             raise HTTPException(status_code=400, detail="Image size exceeds 1 MB.")

#         image_data = await image.read()
#         product.image = image_data  # Mettre à jour l'image

#     for key, value in product_data.dict(exclude_unset=True).items():
#         setattr(product, key, value)
    
#     db.commit()
#     db.refresh(product)

#     return JSONResponse(content={
#         "message": "Product updated successfully",
#         "product": product
#     }, status_code=200)



# @router.put("/update/{product_id}", response_model=ProductResponse)
# async def update_product(
#     product_id: int,
#     product_update: ProductUpdate,
#     db: Session = Depends(get_db)
# ):
#     # Rechercher le produit dans la base de données
#     product = db.query(Product).filter(Product.id == product_id).first()
    
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found.")

#     # Mettre à jour les champs si fournis
#     if product_update.name is not None:
#         product.name = product_update.name
#     if product_update.description is not None:
#         product.description = product_update.description
#     if product_update.category_id is not None:
#         product.category_id = product_update.category_id
#     if product_update.quantity is not None:
#         product.quantity = product_update.quantity
#     if product_update.unit_price is not None:
#         product.unit_price = product_update.unit_price
#     if product_update.image is not None:
#         # Convertir l'image en Base64 si une nouvelle image est fournie
#         product.image = convert_image_to_base64(product_update.image)

#     db.commit()
#     db.refresh(product)

#     return JSONResponse(content={
#         "message": "Product updated successfully",
#         "product": jsonable_encoder(product)
#     }, status_code=200)


@router.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return JSONResponse(content={"message": "Product deleted successfully"}, status_code=200)
