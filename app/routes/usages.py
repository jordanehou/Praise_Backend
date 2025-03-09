from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Usage
from ..schemas import UsageCreate, UsageUpdate, UsageResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/create", response_model=UsageResponse)
# def create_usage(usage: UsageCreate, db: Session = Depends(get_db)):
#     new_usage = Usage(**usage.dict())
#     db.add(new_usage)
#     db.commit()
#     db.refresh(new_usage)
#     return JSONResponse(content={"message": "Usage recorded successfully", "usage": new_usage}, status_code=201)

@router.post("/create", response_model=UsageResponse)
def create_usage(usage: UsageCreate, db: Session = Depends(get_db)):
    new_usage = Usage(**usage.dict())
    db.add(new_usage)
    db.commit()
    db.refresh(new_usage)  # Rafraîchir l'objet pour inclure les valeurs mises à jour
    return JSONResponse(content={"message": "Usage recorded successfully", "usage": jsonable_encoder(new_usage)}, status_code=201)  # Utiliser jsonable_encoder pour serialiser l'objet new_usage}, status_code=201)

@router.get("/list", response_model=list[UsageResponse])
def list_usages(db: Session = Depends(get_db)):
    usages = db.query(Usage).all()
    return JSONResponse(content={"usages": jsonable_encoder(usages)}, status_code=200)  # Utiliser jsonable_encoder pour serialiser l'objet usages}, status_code=200)

@router.get("/details/{usage_id}", response_model=UsageResponse)
def get_usage(usage_id: int, db: Session = Depends(get_db)):
    usage = db.query(Usage).filter(Usage.id == usage_id).first()
    if not usage:
        raise HTTPException(status_code=404, detail="Usage not found")
    return JSONResponse(content={"usage": jsonable_encoder(usage)}, status_code=200)  # Utiliser jsonable_encoder pour serialiser l'objet usage}, status_code=200)

# @router.put("/update/{usage_id}", response_model=UsageResponse)
# def update_usage(usage_id: int, usage_data: UsageUpdate, db: Session = Depends(get_db)):
#     usage = db.query(Usage).filter(Usage.id == usage_id).first()
#     if not usage:
#         raise HTTPException(status_code=404, detail="Usage not found")
#     for key, value in usage_data.dict().items():
#         setattr(usage, key, value)
#     db.commit()
#     return JSONResponse(content={"message": "Usage updated successfully", "usage": jsonable_encoder(usage)}, status_code=200)  # Utiliser jsonable_encoder pour serialiser l'objet usage}, status_code=200)


@router.put("/update/{usage_id}", response_model=UsageResponse)
def update_usage(usage_id: int, usage_data: UsageUpdate, db: Session = Depends(get_db)):
    usage = db.query(Usage).filter(Usage.id == usage_id).first()
    if not usage:
        raise HTTPException(status_code=404, detail="Usage not found")
    
    for key, value in usage_data.dict().items():
        setattr(usage, key, value)
    
    db.commit()
    
    return UsageResponse.from_orm(usage)

@router.delete("/delete/{usage_id}")
def delete_usage(usage_id: int, db: Session = Depends(get_db)):
    usage = db.query(Usage).filter(Usage.id == usage_id).first()
    if not usage:
        raise HTTPException(status_code=404, detail="Usage not found")
    db.delete(usage)
    db.commit()
    return JSONResponse(content={"message": "Usage deleted successfully", "usage": jsonable_encoder(usage)}, status_code=200)  # Utiliser jsonable_encoder pour serialiser l'objet usage}, status_code=200)
