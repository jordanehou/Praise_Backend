from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Delivery
from ..schemas import DeliveryCreate, DeliveryUpdate, DeliveryResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/create", response_model=DeliveryResponse)
# def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
#     new_delivery = Delivery(**delivery.dict())
#     db.add(new_delivery)
#     db.commit()
#     db.refresh(new_delivery)
#     return JSONResponse(content={"message": "Delivery created successfully", "delivery": new_delivery}, status_code=201)

@router.post("/create", response_model=DeliveryResponse)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    # Conversion de delivery_date si ce n'est pas un datetime
    if isinstance(delivery.delivery_date, str):
        try:
            delivery_date = datetime.strptime(delivery.delivery_date, "%Y/%m/%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY/MM/DD.")
    else:
        delivery_date = delivery.delivery_date

    new_delivery = Delivery(
        product_id=delivery.product_id,
        structure_name=delivery.structure_name,
        delivery_date=delivery_date,
        quantity=delivery.quantity,
        amount_paid=delivery.amount_paid
    )

    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)

    # return JSONResponse(content={"message": "Delivery created successfully", "delivery": new_delivery}, status_code=201)
    # return JSONResponse(content={"message": "Delivery created successfully", "delivery": new_delivery.__dict__}, status_code=201)
    return JSONResponse(
    content={"message": "Delivery created successfully", "delivery": jsonable_encoder(new_delivery)},
    status_code=201
)


# @router.get("/list", response_model=list[DeliveryResponse])
# def list_deliveries(db: Session = Depends(get_db)):
#     deliveries = db.query(Delivery).all()
#     return JSONResponse(content={"deliveries": deliveries}, status_code=200)

@router.get("/list", response_model=list[DeliveryResponse])
def list_deliveries(db: Session = Depends(get_db)):
    deliveries = db.query(Delivery).all()
    # Convertir chaque objet Delivery en un format JSON compatible
    return JSONResponse(content={"deliveries": jsonable_encoder(deliveries)}, status_code=200)

@router.get("/details/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return JSONResponse(content={"delivery": jsonable_encoder(delivery)}, status_code=200)

# @router.put("/update/{delivery_id}", response_model=DeliveryResponse)
# def update_delivery(delivery_id: int, delivery_data: DeliveryUpdate, db: Session = Depends(get_db)):
#     delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
#     if not delivery:
#         raise HTTPException(status_code=404, detail="Delivery not found")
#     for key, value in delivery_data.dict().items():
#         setattr(delivery, key, value)
#     db.commit()
#     # return JSONResponse(content={"message": "Delivery updated successfully", "delivery": delivery}, status_code=200)
#     return JSONResponse(
#     content={"message": "Delivery created successfully", "delivery": jsonable_encoder(new_delivery)},
#     status_code=201
# )

# @router.put("/update/{delivery_id}", response_model=DeliveryResponse)
# def update_delivery(delivery_id: int, delivery_data: DeliveryUpdate, db: Session = Depends(get_db)):
#     delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
#     if not delivery:
#         raise HTTPException(status_code=404, detail="Delivery not found")
    
#     # Vérifie et convertit delivery_date si nécessaire
#     if isinstance(delivery_data.delivery_date, str):
#         try:
#             delivery_data.delivery_date = datetime.fromisoformat(delivery_data.delivery_date)
#         except ValueError:
#             raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DDTHH:MM:SS.")

#     for key, value in delivery_data.dict().items():
#         setattr(delivery, key, value)
#     db.commit()
#     # return JSONResponse(content={"message": "Delivery updated successfully", "delivery": delivery}, status_code=200)
#     # return JSONResponse(content={"message": "Delivery updated successfully", "delivery": delivery}, status_code=200)
#     return JSONResponse(
#     content={"message": "Delivery created successfully", "delivery": jsonable_encoder(delivery)},
#     status_code=201
# )


@router.put("/update/{delivery_id}", response_model=DeliveryResponse)
def update_delivery(delivery_id: int, delivery_data: DeliveryUpdate, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    # Vérifie et convertit delivery_date si nécessaire
    if isinstance(delivery_data.delivery_date, str):
        try:
            delivery_data.delivery_date = datetime.fromisoformat(delivery_data.delivery_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DDTHH:MM:SS.")

    for key, value in delivery_data.dict().items():
        setattr(delivery, key, value)
    
    db.commit()
    db.refresh(delivery)  # Rafraîchir l'objet pour obtenir les valeurs mises à jour

    return JSONResponse(
    content={"message": "Delivery updated successfully", "delivery": jsonable_encoder(delivery)},
    status_code=200
)

@router.delete("/delete/{delivery_id}")
def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    db.delete(delivery)
    db.commit()
    return JSONResponse(content={"message": "Delivery deleted successfully"}, status_code=200)
