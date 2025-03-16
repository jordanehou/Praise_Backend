# from sqlalchemy import Column, Integer, String
# from .database import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password_hash = Column(String)



from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user")
    
    categories = relationship("Category", back_populates="owner")
    # Relation avec Usage
    usages = relationship("Usage", back_populates="user")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="categories")
    products = relationship("Product", back_populates="category")

# class Product(Base):
#     __tablename__ = "products"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     description = Column(String)
#     category_id = Column(Integer, ForeignKey("categories.id"))
#     # delivery_id = Column(Integer, ForeignKey("deliveries.id"))  # 🚀 Ajout du champ supplier_id
#     quantity = Column(Integer, default=0)  # 🚀 Ajout du champ quantity
#     unit_price = Column(Float, default=0.0)  # 🚀 Ajout du champ unit_price
#     # image = Column(String)  # Changez cela en String pour stocker l'image en Base64
#     createdAt = Column(DateTime(timezone=True), server_default=func.now())  # Date de création
#     updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Date de mise à jour
    
    
#     category = relationship("Category", back_populates="products")
#     deliveries = relationship("Delivery", back_populates="product")
#     usages = relationship("Usage", back_populates="product")



class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    quantity = Column(Integer, default=0)  # Quantité disponible
    unit_price = Column(Float, default=0.0)  # Prix unitaire
    image_path = Column(String, nullable=True)  # Champ pour stocker le chemin de l'image
    createdAt = Column(DateTime(timezone=True), server_default=func.now())  # Date de création
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Date de mise à jour
    
    # Relations
    category = relationship("Category", back_populates="products")
    deliveries = relationship("Delivery", back_populates="product")
    usages = relationship("Usage", back_populates="product")

    # def __repr__(self):
    #     return f"<Product(id={self.id}, name={self.name}, category_id={self.category_id}, quantity={self.quantity}, unit_price={self.unit_price}, image_path={self.image_path})>"
    

# class Delivery(Base):
#     __tablename__ = "deliveries"
#     id = Column(Integer, primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey("products.id"))
#     structure_name = Column(String)
#     delivery_date = Column(DateTime)
#     quantity = Column(Integer)
#     amount_paid = Column(Float)
    
#     product = relationship("Product", back_populates="deliveries")

# class Usage(Base):
#     __tablename__ = "usages"
#     id = Column(Integer, primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey("products.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))
#     usage_date = Column(DateTime)
#     purpose = Column(String)
#     quantity_used = Column(Integer)
    
#     product = relationship("Product", back_populates="usages")
#     user = relationship("User")

class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    structure_name = Column(String)
    delivery_date = Column(DateTime, default=datetime.utcnow, nullable=False)  # Auto-rempli
    quantity = Column(Integer)
    amount_paid = Column(Float)
    
    product = relationship("Product", back_populates="deliveries")

class Usage(Base):
    __tablename__ = "usages"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    usage_date = Column(DateTime, default=datetime.utcnow, nullable=False)  # Auto-rempli
    purpose = Column(String)
    quantity_used = Column(Integer)
    
    product = relationship("Product", back_populates="usages")
    user = relationship("User", back_populates="usages")