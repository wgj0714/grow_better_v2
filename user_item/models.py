from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base, engine
import uuid
import database

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True) 
    title = Column(String, index=True)
    description  = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email =  Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    
    items = relationship("Item", back_populates="owner")

# class Plant(Base):
#     pass 

# class Comments(Base):
#     pass


# Create all tables in the database
Base.metadata.create_all(bind=engine)