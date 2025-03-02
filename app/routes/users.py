from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User
from ..schemas import UserCreate, UserUpdate, UserResponse
from ..auth import get_password_hash, verify_password, create_access_token
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import timedelta


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Permet d'actualiser l'objet avec l'ID généré
        
        # Convertir en UserResponse (Pydantic)
        return UserResponse(id=new_user.id, username=new_user.username, email=new_user.email)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


class LoginRequest(BaseModel):
    username: str
    password: str


# @router.post("/login")
# def login(user_data: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == user_data.username).first()
#     if not user or not verify_password(user_data.password, user.password_hash):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     # token = create_access_token({"sub": user.username})
#     ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Par exemple, un token valide pendant 30 minutes
#     token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     token = create_access_token({"sub": user.username}, token_expires)
#     return JSONResponse(content={"access_token": token, "token_type": "bearer"}, status_code=200)

@router.post("/login")
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Générer un token valide pendant 30 minutes
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": user.username, "email": user.email, "role": user.role}, token_expires)

    # Retourner le token et les infos utilisateur
    return JSONResponse(content={
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }, status_code=200)


@router.get("/list", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    
    # Convertir chaque objet User en UserResponse
    return [UserResponse(id=user.id, username=user.username, email=user.email) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(id=user.id, username=user.username, email=user.email)


@router.put("/update/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)

    return UserResponse(id=user.id, username=user.username, email=user.email)
