# # FastAPI application (main.py)
# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from .database import SessionLocal, engine
# from .models import Base, User
# from .auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
# from datetime import timedelta
# from pydantic import BaseModel
# from .schemas import UserResponse

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# # Dépendance de base de données
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # # # Endpoint d'inscription
# # # @app.post("/register")
# # # def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
# # #     user = User(username=username, email=email, password_hash=get_password_hash(password))
# # #     db.add(user)
# # #     db.commit()
# # #     return {"message": "Utilisateur créé avec succès"}


# # class UserCreate(BaseModel):
# #     username: str
# #     email: str
# #     password: str

# # @app.post("/register")
# # def register(user: UserCreate, db: Session = Depends(get_db)):
# #     new_user = User(username=user.username, email=user.email, password_hash=get_password_hash(user.password))
# #     db.add(new_user)
# #     db.commit()
# #     return {"message": "Utilisateur créé avec succès"}

# # # Endpoint de connexion
# # # @app.post("/login")
# # # def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
# # #     user = db.query(User).filter(User.username == form_data.username).first()
# # #     if not user or not verify_password(form_data.password, user.password_hash):
# # #         raise HTTPException(status_code=400, detail="Nom d'utilisateur ou mot de passe incorrect")
    
# # #     access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
# # #     return {"access_token": access_token, "token_type": "bearer"}

# # from pydantic import BaseModel

# # class LoginRequest(BaseModel):
# #     username: str
# #     password: str

# # @app.post("/login")
# # def login(user: LoginRequest, db: Session = Depends(get_db)):
# #     user_in_db = db.query(User).filter(User.username == user.username).first()
# #     if not user_in_db or not verify_password(user.password, user_in_db.password_hash):
# #         raise HTTPException(status_code=400, detail="Nom d'utilisateur ou mot de passe incorrect")
    
# #     access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
# #     return {"access_token": access_token, "token_type": "bearer"}


# # # Endpoint de test de connexion
# # @app.get("/users/me")
# # def read_users_me(token: str = Depends(oauth2_scheme)):
# #     return {"token": token}


# # # Dependency to get the database session
# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# # @app.get("/list-user", response_model=list[UserResponse])
# # def list_users(db: Session = Depends(get_db)):
# #     users = db.query(User).all()
# #     return users


# from fastapi import FastAPI
# from .routes import users, categories, products, deliveries, usages
# from .database import engine
# from .models import Base

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(categories.router, prefix="/categories", tags=["Categories"])
# app.include_router(products.router, prefix="/products", tags=["Products"])
# app.include_router(deliveries.router, prefix="/deliveries", tags=["Deliveries"])
# app.include_router(usages.router, prefix="/usages", tags=["Usages"])


# # from fastapi import FastAPI
# # from .routes import users, categories, products, deliveries, usages

# # app = FastAPI()

# # app.include_router(users.router, prefix="/users", tags=["Users"])
# # app.include_router(categories.router, prefix="/categories", tags=["Categories"])
# # app.include_router(products.router, prefix="/products", tags=["Products"])
# # app.include_router(deliveries.router, prefix="/deliveries", tags=["Deliveries"])
# # app.include_router(usages.router, prefix="/usages", tags=["Usages"])

from fastapi import FastAPI
from .database import engine, SessionLocal
from .models import Base
from .routes import users, categories, products, deliveries, usages, images
#from .routes.image import router as image_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

# Initialisation de l'application FastAPI
app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines (tu peux mettre "http://localhost:3000" si tu veux être plus strict)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)


# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Inclusion des routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(deliveries.router, prefix="/deliveries", tags=["Deliveries"])
app.include_router(usages.router, prefix="/usages", tags=["Usages"])
# Inclure les routes d'images
app.include_router(images.router)
