# from pydantic import BaseModel

# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: str

#     class Config:
#         from_attributes = True

# Schémas (schemas.py)
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Optional[str] = "user"  # Ajout du rôle avec une valeur par défaut

    class Config:
        from_attributes = True  # Permet de convertir un objet SQLAlchemy en Pydantic

class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None

# class ProductCreate(ProductBase):
#     category_id: int

# class ProductUpdate(BaseModel):
#     name: Optional[str] = None
#     category_id: Optional[int] = None
#     supplier_id: Optional[int] = None
#     quantity: Optional[int] = None
#     unit_price: Optional[float] = None

# class ProductResponse(ProductBase):
#     id: int
#     category_id: int

#     class Config:
#         from_attributes = True


# ======== DELIVERY SCHEMAS ========
class DeliveryCreate(BaseModel):
    product_id: int
    structure_name: str
    delivery_date: datetime  # Format: YYYY-MM-DD
    quantity: int
    amount_paid: float

class DeliveryUpdate(BaseModel):
    product_id: Optional[int] = None
    supplier_id: Optional[int] = None
    quantity_delivered: Optional[int] = None
    delivery_date: Optional[str] = None

class DeliveryResponse(DeliveryCreate):  # ✅ Définir DeliveryResponse avant ProductResponse
    id: int

    class Config:
        orm_mode = True

class UsageBase(BaseModel):
    usage_date: datetime
    purpose: str
    quantity_used: int


# ======== PRODUCT SCHEMAS ========
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    quantity: int
    unit_price: float
    #image: Optional[bytes] = None  # Champ pour l'image en binaire
    # image: Optional[str] = None
    


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    description: Optional[str] = None
    # image: Optional[str] = None  # Image peut aussi être optionnelle


class ProductResponse(ProductCreate):
    id: int
    deliveries: List[DeliveryResponse] = []  # Ajouter les livraisons associées
    description: Optional[str] = None
    price: int
    createdAt: datetime
    updatedAt: datetime


    class Config:
        orm_mode = True


# ======== USAGE SCHEMAS ========
class UsageCreate(BaseModel):
    product_id: int
    user_id: int
    quantity_used: int
    usage_date: datetime  # Format: YYYY-MM-DD
    purpose: str

class UsageUpdate(BaseModel):
    product_id: Optional[int] = None
    user_id: Optional[int] = None
    quantity_used: Optional[int] = None
    usage_date: Optional[datetime] = None
    purpose: Optional[str] = None

class UsageResponse(UsageCreate):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True