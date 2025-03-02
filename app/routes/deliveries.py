from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Delivery
from ..schemas import DeliveryCreate, DeliveryUpdate, DeliveryResponse
from fastapi.responses import JSONResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=DeliveryResponse)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    new_delivery = Delivery(**delivery.dict())
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    return JSONResponse(content={"message": "Delivery created successfully", "delivery": new_delivery}, status_code=201)

@router.get("/", response_model=list[DeliveryResponse])
def list_deliveries(db: Session = Depends(get_db)):
    deliveries = db.query(Delivery).all()
    return JSONResponse(content={"deliveries": deliveries}, status_code=200)

@router.get("/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return JSONResponse(content={"delivery": delivery}, status_code=200)

@router.put("/{delivery_id}", response_model=DeliveryResponse)
def update_delivery(delivery_id: int, delivery_data: DeliveryUpdate, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    for key, value in delivery_data.dict().items():
        setattr(delivery, key, value)
    db.commit()
    return JSONResponse(content={"message": "Delivery updated successfully", "delivery": delivery}, status_code=200)

@router.delete("/delete/{delivery_id}")
def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    db.delete(delivery)
    db.commit()
    return JSONResponse(content={"message": "Delivery deleted successfully"}, status_code=200)
